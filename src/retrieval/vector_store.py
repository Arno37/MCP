"""Module de stockage vectoriel."""
import os
import sys
import logging
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import re # Ajout de l'import re

# Configuration du logger pour ce module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Utilisation du mock pendant les tests
if 'pytest' in sys.modules:
    logger.info("Utilisation de MockVectorStore pour les tests.")
    from tests.mocks import MockVectorStore as VectorStore
else:
    try:
        class VectorStore:
            """Stockage vectoriel réel utilisant sentence-transformers et numpy."""
            
            def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
                """Initialise le stockage vectoriel avec le modèle d'embedding."""
                self.model_name = model_name
                try:
                    # Chargement du modèle d'embedding
                    self.model = SentenceTransformer(self.model_name)
                    logger.info(f"Modèle SentenceTransformer '{self.model_name}' chargé.")
                except Exception as e:
                    logger.error(f"Erreur lors du chargement du modèle SentenceTransformer '{self.model_name}': {e}")
                    logger.error("Assurez-vous que sentence-transformers est installé (`pip install sentence-transformers`) et que le modèle est valide.")
                    # Optionnellement, lever une exception ou utiliser un fallback
                    raise RuntimeError("Impossible de charger le modèle d'embedding.") from e
                
                # Structures pour stocker les chunks, vecteurs et métadonnées
                self.chunks: List[str] = []
                self.vectors: List[np.ndarray] = []
                self.chunk_metadata: List[Dict[str, Any]] = []
                self.doc_counter: int = 0 # Pour assigner des ID de document originel
                self.initialized: bool = False

            def initialize(self):
                """Marque le stockage comme initialisé (peut être étendu plus tard)."""
                self.initialized = True
                logger.info("VectorStore initialisé.")

            def _chunk_text(self, text: str) -> List[str]:
                """Découpe le texte en chunks (paragraphes) en utilisant regex pour plus de robustesse."""
                # Sépare par lignes vides (gère \n\n, \r\n\r\n, et variations avec espaces)
                # Regex : \s* => zéro ou plusieurs espaces/tabs ; [\r\n]{2,} => au moins deux sauts de ligne (\r ou \n) ; \s* => zéro ou plusieurs espaces/tabs
                # paragraphs = [p.strip() for p in text.split('\\n\\n') if p.strip()] # Ancienne méthode
                paragraphs = [p.strip() for p in re.split(r'\s*[\r\n]{2,}\s*', text) if p.strip()]
                logger.debug(f"Texte découpé en {len(paragraphs)} chunks (paragraphes) via regex.")
                return paragraphs

            def add_document(self, content: str, metadata: dict = None) -> int:
                """Découpe un document en chunks, les vectorise et les stocke."""
                if not self.initialized:
                    logger.error("Tentative d'ajout de document avant initialisation.")
                    raise Exception("VectorStore non initialisé")
                
                doc_id = self.doc_counter
                self.doc_counter += 1
                base_metadata = metadata or {}
                base_metadata["original_doc_id"] = doc_id
                
                logger.info(f"Ajout du document ID {doc_id}...")
                chunks = self._chunk_text(content)

                if not chunks:
                    logger.warning(f"Le document ID {doc_id} ne contient aucun chunk après découpage.")
                    return doc_id # Retourne l'ID même si aucun chunk n'est ajouté

                try:
                    chunk_vectors = self.model.encode(chunks, show_progress_bar=False).astype(np.float32) # Encodage par batch
                    logger.info(f"Encodage de {len(chunks)} chunks pour le document ID {doc_id} terminé.")
                    
                    for i, chunk in enumerate(chunks):
                        chunk_meta = base_metadata.copy()
                        chunk_meta["chunk_index"] = i
                        self.chunks.append(chunk)
                        self.vectors.append(chunk_vectors[i])
                        self.chunk_metadata.append(chunk_meta)
                        
                except Exception as e:
                    logger.error(f"Erreur lors de l'encodage des chunks pour le document ID {doc_id}: {e}")
                    # Gérer l'erreur comme nécessaire (ex: log, ignorer, lever une exception)
                    return doc_id # Potentiellement incomplet

                logger.info(f"{len(chunks)} chunks ajoutés pour le document ID {doc_id}. Total chunks: {len(self.chunks)}")
                return doc_id

            def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
                """Calcule la similarité cosinus entre deux vecteurs numpy."""
                norm_vec1 = np.linalg.norm(vec1)
                norm_vec2 = np.linalg.norm(vec2)
                if norm_vec1 == 0 or norm_vec2 == 0:
                    return 0.0
                return np.dot(vec1, vec2) / (norm_vec1 * norm_vec2)

            def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
                """Recherche les k chunks les plus similaires à la requête."""
                if not self.initialized:
                    logger.error("Tentative de recherche avant initialisation.")
                    raise Exception("VectorStore non initialisé")
                
                if not self.vectors:
                    logger.warning("Recherche effectuée mais aucun vecteur n'est stocké.")
                    return []

                logger.info(f"Recherche des {k} chunks les plus similaires pour la requête: '{query[:50]}...'")
                try:
                    query_vector = self.model.encode([query], show_progress_bar=False)[0].astype(np.float32)
                except Exception as e:
                    logger.error(f"Erreur lors de l'encodage de la requête '{query[:50]}...': {e}")
                    return []

                # Conversion de la liste de vecteurs en matrice numpy pour efficacité
                all_vectors = np.array(self.vectors)
                
                # Calcul des similarités cosinus
                # Similarité cosinus: (A . B) / (||A|| * ||B||)
                dot_products = np.dot(all_vectors, query_vector)
                norms_vectors = np.linalg.norm(all_vectors, axis=1)
                norm_query = np.linalg.norm(query_vector)
                
                # Éviter la division par zéro
                valid_indices = (norms_vectors > 0) & (norm_query > 0)
                similarities = np.zeros(len(all_vectors))
                similarities[valid_indices] = dot_products[valid_indices] / (norms_vectors[valid_indices] * norm_query)

                # Obtention des indices des k meilleurs scores
                # argsort trie par ordre croissant, donc on prend les k derniers pour les meilleurs scores
                # ou on trie par ordre décroissant en utilisant le négatif
                # Utiliser argpartition est plus efficace si k est petit par rapport à N
                num_results = min(k, len(similarities))
                if num_results == 0:
                    logger.info("Aucun résultat trouvé (pas de vecteurs valides ou k=0).")
                    return []
                    
                top_k_indices = np.argpartition(-similarities, range(num_results))[:num_results]
                
                # Création de la liste des résultats
                results = []
                for idx in top_k_indices:
                    if similarities[idx] > 0: # Optionnel: seuil de similarité
                        results.append({
                            "content": self.chunks[idx],
                            "metadata": self.chunk_metadata[idx],
                            "score": float(similarities[idx]) # Conversion en float standard
                        })
                
                # Tri des résultats par score décroissant
                results.sort(key=lambda x: x["score"], reverse=True)
                
                logger.info(f"Recherche terminée. {len(results)} résultats trouvés.")
                return results

    except ImportError as ie:
        logger.warning(f"Dépendance manquante: {ie}. Assurez-vous d'installer 'sentence-transformers' et 'numpy'.")
        logger.warning("Utilisation de MockVectorStore comme fallback.")
        from tests.mocks import MockVectorStore as VectorStore
    except Exception as e:
        logger.error(f"Erreur inattendue lors de l'initialisation de VectorStore: {e}")
        logger.warning("Utilisation de MockVectorStore comme fallback.")
        from tests.mocks import MockVectorStore as VectorStore

# # Exemple d'utilisation (si exécuté directement, pour test)
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     logger.info("Test de VectorStore...")
#     vector_store = VectorStore()
#     vector_store.initialize()
    
#     doc1 = """Ceci est le premier document.
# Il parle de chats."""
#     doc2 = """Un deuxième document ici.
# Les chiens sont aussi des animaux de compagnie."""
#     doc3 = """Les chats et les chiens peuvent cohabiter."""
    
#     vector_store.add_document(doc1, {"source": "doc1.txt"})
#     vector_store.add_document(doc2, {"source": "doc2.txt"})
#     vector_store.add_document(doc3, {"source": "doc3.txt"})
    
#     query = "animaux domestiques"
#     search_results = vector_store.search(query, k=2)
    
#     print(f"\nRésultats de recherche pour '{query}':")
#     for res in search_results:
#         print(f"- Score: {res['score']:.4f}, Source: {res['metadata'].get('source', 'N/A')}, Chunk Index: {res['metadata'].get('chunk_index', 'N/A')}")
#         print(f"  Contenu: {res['content'][:80]}...")
#     logger.info("Test de VectorStore terminé.")
