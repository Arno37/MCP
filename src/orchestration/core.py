from typing import List, Dict, Any, Optional
from src.retrieval.vector_store import VectorStore
from .flow_manager import FlowManager
from src.generation.generator import generate_response_ollama
import logging
from datetime import datetime
import threading
import os
import requests # Assurer que requests est importé

class Orchestrator:
    """Orchestrateur principal qui gère les flux entre les composants."""
    
    def __init__(self):
        """Initialise l'orchestrateur avec ses composants."""
        self.retrieval = VectorStore()
        self.retrieval.initialize()
        self.flow_manager = FlowManager()
        self.logger = self._setup_logger()
        self.processing_thread = None
        self.is_running = False
        
    def _setup_logger(self) -> logging.Logger:
        """Configure le système de logging."""
        logger = logging.getLogger('Orchestrator')
        logger.setLevel(logging.INFO)
        
        # Handler pour la console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Format du log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        return logger
    
    def start_processing(self):
        """Démarre le traitement des requêtes en arrière-plan."""
        self.is_running = True
        self.processing_thread = threading.Thread(target=self._process_queue)
        self.processing_thread.start()
        self.logger.info("Traitement des requêtes démarré")
    
    def stop_processing(self):
        """Arrête le traitement des requêtes."""
        self.is_running = False
        if self.processing_thread:
            self.processing_thread.join()
        self.logger.info("Traitement des requêtes arrêté")
    
    def _process_queue(self):
        """Traite les requêtes en file d'attente."""
        while self.is_running:
            request = self.flow_manager.get_next_request()
            if request:
                self.logger.info(f"Traitement de la requête: {request.request_id}")
                result = self._process_single_request(request)
                self.logger.info(f"Requête {request.request_id} traitée")
    
    def _process_single_request(self, request: Any) -> Dict[str, Any]:
        """Traite une seule requête."""
        try:
            self.logger.info(f"Nouvelle requête reçue: {request.query}")
            start_time = datetime.now()
            
            # 1. Recherche locale des chunks pertinents
            self.logger.info("Recherche locale des chunks pertinents...")
            retrieved_chunks = self.retrieval.search(request.query, k=3) # Récupère les 3 chunks locaux les plus similaires
            self.logger.info(f"{len(retrieved_chunks)} chunks locaux trouvés.")
            processing_time_retrieval = (datetime.now() - start_time).total_seconds()
            
            # 2. Recherche Externe via MCP (Appel Simulé)
            self.logger.info("Recherche externe via MCP (SIMULÉE - aucun appel réel)...")
            start_time_mcp = datetime.now()
            web_search_results = []
            # mcp_local_url = "http://localhost:8000/" # URL Supprimée car simulation
            
            try:
                # ---- SIMULATION de l'appel MCP (retour vide) ----
                self.logger.info("Simulation d'un appel MCP (retourne une liste vide).")
                brave_search_response = {"results": []} 
                # ---- Fin de la simulation ----
                                
                # Formatage des résultats (ne fera rien car la liste est vide)
                if brave_search_response and "results" in brave_search_response:
                    self.logger.info(f"Réponse (simulée) reçue: {len(brave_search_response['results'])} résultats.")
                    for result in brave_search_response["results"]:
                        web_search_results.append({
                            "content": f"Titre: {result.get('title', '')}\nSnippet: {result.get('description', '')}",
                            "metadata": {"source": "Simulated-BraveSearch", "url": result.get('url')}
                        })
                else:
                     self.logger.warning("Réponse simulée vide ou format inattendu.")

            # Gestion d'erreur minimale pour la simulation (ne devrait pas se produire)
            except Exception as mcp_e:
                self.logger.error(f"Erreur inattendue pendant la simulation MCP: {mcp_e}")
                web_search_results = []
                
            processing_time_mcp = (datetime.now() - start_time_mcp).total_seconds()

            # 3. Combinaison des contextes local et externe
            combined_context = retrieved_chunks + web_search_results 
            # Note: On pourrait trier ou filtrer `combined_context` davantage ici si besoin
            
            if not combined_context:
                 self.logger.warning("Aucun contexte (local ou externe) trouvé.")
                 # Retourner un statut spécifique ou gérer comme no_results locaux
                 return {
                     "request_id": request.request_id,
                     "status": "no_context",
                     "message": "Aucun contexte pertinent trouvé (local ou externe)",
                     "retrieved_chunks": [],
                     "web_search_results": []
                 }

            # 4. Génération de la réponse finale via LLM (Ollama)
            self.logger.info(f"Génération de la réponse basée sur {len(combined_context)} éléments de contexte.")
            start_time_generation = datetime.now()
            # Passer le contexte combiné au générateur
            generated_answer = generate_response_ollama(request.query, combined_context) 
            processing_time_generation = (datetime.now() - start_time_generation).total_seconds()
            
            # Calcul du temps total
            processing_time_total = processing_time_retrieval + processing_time_mcp + processing_time_generation
            
            response = {
                "request_id": request.request_id,
                "status": "success",
                "query": request.query,
                "processing_time_retrieval": processing_time_retrieval,
                "processing_time_mcp": processing_time_mcp, # Ajout du temps MCP
                "processing_time_generation": processing_time_generation,
                "processing_time_total": processing_time_total, 
                "retrieved_chunks": retrieved_chunks, 
                "web_search_results": web_search_results, # Ajout des résultats web
                "generated_answer": generated_answer, # Réponse du LLM basée sur contexte combiné
                "metadata": {
                    "total_local_chunks_found": len(retrieved_chunks),
                    "total_web_results_found": len(web_search_results),
                    "priority": request.priority
                }
            }
            
            self.logger.info(f"Requête traitée en {processing_time_total:.2f} secondes")
            return response
            
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement de la requête {request.request_id}: {str(e)}")
            return {
                "request_id": request.request_id,
                "status": "error",
                "message": str(e),
                "retrieved_chunks": [],
                "web_search_results": [] # Ajout pour cohérence
            }
    
    def submit_request(self, query: str, priority: int = 1, metadata: Dict[str, Any] = None) -> str:
        """
        Soumet une nouvelle requête pour traitement.
        
        Args:
            query: La requête à traiter
            priority: Priorité de la requête (1 = normal, 2 = élevée, 3 = urgente)
            metadata: Métadonnées supplémentaires
            
        Returns:
            ID de la requête
        """
        request_id = self.flow_manager.add_request(query, priority, metadata)
        self.logger.info(f"Nouvelle requête soumise: {request_id}")
        return request_id
    
    def get_system_status(self) -> Dict[str, Any]:
        """Retourne l'état actuel du système."""
        queue_status = self.flow_manager.get_queue_status()
        
        return {
            "status": "operational",
            "components": {
                "retrieval": {
                    "status": "active",
                    "documents_count": len(self.retrieval.documents_metadata)
                },
                "flow_manager": {
                    "status": "active",
                    "queue_size": queue_status["queue_size"]
                }
            },
            "timestamp": datetime.now().isoformat()
        }

    def process_query(self, question: str, local_only: bool = False):
        # ... (début du code) ...

        # Étape de décision : Appeler les MCPs ?
        should_call_mcp = False # Par défaut
        if not local_only:
            # Mettez ici votre logique actuelle pour décider si un MCP est nécessaire
            # Par exemple:
            # if analyse_question_pour_mcp(question):
            #    should_call_mcp = True
            pass # Remplacez "pass" par votre logique

        if should_call_mcp:
            # Appeler les MCPs et potentiellement le RAG local
            # results_mcp = call_mcp_orchestrator(...)
            # results_local = call_rag_local(...) # Optionnel si MCP suffit
            # combined_results = combine(results_mcp, results_local)
            pass # Remplacez par votre logique d'appel MCP + RAG
        else:
            # Forcer l'appel RAG local seul
            # results_local = call_rag_local(question)
            # combined_results = results_local # Ou formater si nécessaire
            pass # Remplacez par votre logique d'appel RAG local seul

        # Générer la réponse finale basée sur combined_results
        # final_response = generate_response(combined_results, question)
        # return final_response
        return "Logique à implémenter" # Placeholder

# Exemple d'utilisation
if __name__ == "__main__":
    # Création de l'orchestrateur
    orchestrator = Orchestrator()

    # Lecture et ajout du README.md au VectorStore (simulé)
    readme_path = "README.md" 
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
        doc_id = orchestrator.retrieval.add_document(
            content=readme_content, 
            metadata={"source": readme_path}
        )
        orchestrator.logger.info(f"Document '{readme_path}' ajouté au VectorStore avec ID: {doc_id}")
    except FileNotFoundError:
        orchestrator.logger.warning(f"Le fichier '{readme_path}' n'a pas été trouvé.")
    except Exception as e:
        orchestrator.logger.error(f"Erreur lors de la lecture ou de l'ajout de '{readme_path}': {e}")
    
    # Définition des requêtes
    requests_to_process = [
        ("En tenant compte du contexte du projet (décrit dans le README), quelles sont les dernières avancées générales dans les systèmes RAG mentionnées sur le web ?", 1),
        ("Comparer les objectifs du stage définis localement avec les offres de stage similaires trouvées en ligne pour l'intégration MCP.", 3),
        ("Quelles sont les technologies spécifiques mentionnées dans le document local, et existe-t-il des alternatives plus récentes ou populaires d'après une recherche web ?", 2)
    ]
    
    print("=== Test de l'Orchestrator (Traitement direct) ===")
    
    # Traitement direct des requêtes et affichage des réponses
    for i, (query, priority) in enumerate(requests_to_process):
        print(f"\\n--- Traitement de la requête {i+1} ---")
        print(f"Question: {query}")
        
        # Création d'un objet request simplifié
        mock_request = type('obj', (object,), {
            'request_id': f'direct_{i+1}', 
            'query': query, 
            'priority': priority
        })() 
        
        # Appel direct de la fonction de traitement
        result = orchestrator._process_single_request(mock_request)
        
        # Affichage de la réponse générée et des chunks trouvés
        if result["status"] == "success":
            print(f"\\n===== Réponse Générée par le LLM =====\n{result.get('generated_answer', 'Pas de réponse générée.')}\n=======================================")
            # Affichage optionnel des sources utilisées
            print("\nSources Locales Utilisées (Chunks):")
            for chunk in result.get('retrieved_chunks', []):
                print(f"  - Score: {chunk.get('score', 'N/A'):.4f}, Source: {chunk['metadata'].get('source', 'N/A')}, Chunk Idx: {chunk['metadata'].get('chunk_index', 'N/A')}")
            print("\nSources Web Utilisées (Brave Search):")
            for web_res in result.get('web_search_results', []):
                 print(f"  - Source: {web_res['metadata'].get('source')}, URL: {web_res['metadata'].get('url')}")
                 print(f"    Contenu: {web_res['content'][:150]}...") 
            print(f"\n(Temps total: {result.get('processing_time_total', 0):.2f}s = Recherche Locale {result.get('processing_time_retrieval', 0):.2f}s + Recherche Web {result.get('processing_time_mcp', 0):.2f}s + Génération {result.get('processing_time_generation', 0):.2f}s)")
        elif result["status"] == "no_results" or result["status"] == "no_context":
            print(f"Réponse: {result.get('message', 'Aucun résultat trouvé.')}")
        else:
            print(f"Erreur lors du traitement: {result.get('message', 'Erreur inconnue')}")

    print("\\n=== Fin du test ===")
    
    # # Démarrage du traitement (Supprimé pour l'exécution directe)
    # orchestrator.start_processing()
    
    # # Soumission de quelques requêtes (Supprimé pour l'exécution directe)
    # requests = [
    #    ("Quel est le contexte du projet ?", 1),
    #     ("Quels sont les objectifs du stage ?", 3),
    #     ("Quelles technologies sont envisagées ?", 2)
    # ]
    
    # print("=== Test de l'Orchestrator ===")
    
    # # Soumission des requêtes (Supprimé pour l'exécution directe)
    # for query, priority in requests:
    #     request_id = orchestrator.submit_request(query, priority)
    #     print(f"Requête soumise: {request_id} (priorité: {priority})")
    
    # # Attente du traitement (Supprimé pour l'exécution directe)
    # import time
    # time.sleep(2)
    
    # # Arrêt du traitement (Supprimé pour l'exécution directe)
    # orchestrator.stop_processing()
    
    # # État final du système (Supprimé car non pertinent pour l'exécution directe)
    # status = orchestrator.get_system_status()
    # print("\nStatut final du système:")
    # print(f"Status global: {status['status']}")
    # print(f"Nombre de documents: {status['components']['retrieval']['documents_count']}")
    # print(f"Taille de la file: {status['components']['flow_manager']['queue_size']}") 