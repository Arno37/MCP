from typing import List, Dict, Any, Optional
from src.retrieval.vector_store import VectorStore
from .flow_manager import FlowManager
import logging
from datetime import datetime
import threading

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
            
            # 1. Recherche des documents pertinents
            self.logger.info("Recherche des documents pertinents...")
            results = self.retrieval.search(request.query)
            
            if not results:
                self.logger.warning("Aucun document pertinent trouvé")
                return {
                    "request_id": request.request_id,
                    "status": "no_results",
                    "message": "Aucun document pertinent trouvé",
                    "results": []
                }
            
            # 2. Préparation de la réponse
            processing_time = (datetime.now() - start_time).total_seconds()
            
            response = {
                "request_id": request.request_id,
                "status": "success",
                "query": request.query,
                "processing_time": processing_time,
                "results": results,
                "metadata": {
                    "total_results": len(results),
                    "priority": request.priority
                }
            }
            
            self.logger.info(f"Requête traitée en {processing_time:.2f} secondes")
            return response
            
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement de la requête {request.request_id}: {str(e)}")
            return {
                "request_id": request.request_id,
                "status": "error",
                "message": str(e),
                "results": []
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

# Exemple d'utilisation
if __name__ == "__main__":
    # Création de l'orchestrateur
    orchestrator = Orchestrator()
    
    # Démarrage du traitement
    orchestrator.start_processing()
    
    # Soumission de quelques requêtes
    requests = [
        ("Où est le chat ?", 1),
        ("Urgent: Où est le chat ?", 3),
        ("Question sur le chat", 2)
    ]
    
    print("=== Test de l'Orchestrator ===")
    
    # Soumission des requêtes
    for query, priority in requests:
        request_id = orchestrator.submit_request(query, priority)
        print(f"Requête soumise: {request_id} (priorité: {priority})")
    
    # Attente du traitement
    import time
    time.sleep(2)
    
    # Arrêt du traitement
    orchestrator.stop_processing()
    
    # État final du système
    status = orchestrator.get_system_status()
    print("\nStatut final du système:")
    print(f"Status global: {status['status']}")
    print(f"Nombre de documents: {status['components']['retrieval']['documents_count']}")
    print(f"Taille de la file: {status['components']['flow_manager']['queue_size']}") 