# scripts/visualize_chunks.py

import os
import sys
import logging

# Ajout du chemin src au PYTHONPATH pour trouver les modules locaux
# Cela suppose que le script est exécuté depuis la racine du projet (MCP)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Configuration basique du logging pour ce script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Importation nécessaire *après* avoir modifié le path
try:
    from src.retrieval.vector_store import VectorStore
except ImportError as e:
    logging.error(f"Erreur d'importation: {e}")
    logging.error("Assurez-vous que le script est exécuté depuis la racine du projet ('MCP')")
    logging.error("Vérifiez aussi que l'environnement virtuel est activé et les dépendances installées.")
    sys.exit(1)

# --- Configuration ---
SOURCE_FILE_PATH = "README.md" # Chemin vers le document à découper
OUTPUT_CHUNKS_FILE = "chunks_output.txt" # Fichier de sortie pour les chunks
# -------------------

def main():
    logging.info(f"Début du script de visualisation des chunks pour: {SOURCE_FILE_PATH}")

    # Vérifier si le fichier source existe
    if not os.path.exists(SOURCE_FILE_PATH):
        logging.error(f"Le fichier source '{SOURCE_FILE_PATH}' n'a pas été trouvé.")
        logging.error("Assurez-vous que le chemin est correct et que le script est lancé depuis la racine du projet.")
        return

    # Lire le contenu du fichier source
    try:
        with open(SOURCE_FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        logging.info(f"Contenu de '{SOURCE_FILE_PATH}' lu avec succès.")
    except Exception as e:
        logging.error(f"Erreur lors de la lecture de '{SOURCE_FILE_PATH}': {e}")
        return

    # Instancier VectorStore (juste pour utiliser sa méthode _chunk_text)
    # Note: Ceci va charger le modèle sentence-transformer, ce qui n'est pas strictement nécessaire
    # pour le chunking seul, mais c'est le moyen le plus simple de réutiliser la logique existante.
    # Une optimisation serait d'extraire _chunk_text dans un utilitaire séparé.
    try:
        # On peut initialiser sans logger le chargement du modèle ici si on ajuste le logger de VectorStore
        temp_vector_store = VectorStore() 
        # Pas besoin de l'initialiser ou d'ajouter des documents ici
    except Exception as e:
        logging.error(f"Erreur lors de l'instanciation de VectorStore: {e}")
        logging.error("Cela peut être dû à un problème de chargement du modèle sentence-transformer.")
        return

    # Découper le contenu en chunks
    try:
        chunks = temp_vector_store._chunk_text(content)
        logging.info(f"Document découpé en {len(chunks)} chunks.")
    except Exception as e:
        logging.error(f"Erreur lors du découpage du texte: {e}")
        return

    # Sauvegarder les chunks dans le fichier de sortie
    try:
        with open(OUTPUT_CHUNKS_FILE, 'w', encoding='utf-8') as f:
            logging.info(f"Sauvegarde des chunks dans le fichier: {OUTPUT_CHUNKS_FILE}")
            for idx, chunk_content in enumerate(chunks):
                f.write(f"--- Chunk {idx} ---\n")
                f.write(chunk_content)
                f.write("\n\n") # Ajoute deux sauts de ligne entre les chunks pour lisibilité
        logging.info(f"Chunks sauvegardés avec succès dans {OUTPUT_CHUNKS_FILE}")
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde des chunks dans {OUTPUT_CHUNKS_FILE}: {e}")

if __name__ == "__main__":
    main() 