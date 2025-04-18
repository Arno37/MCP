from typing import List, Dict, Any, Optional
from queue import PriorityQueue
from dataclasses import dataclass, field
from datetime import datetime
import threading
import logging

@dataclass(order=True)
class PrioritizedRequest:
    """Classe pour gérer les requêtes prioritaires."""
    priority: int
    timestamp: datetime = field(default_factory=datetime.now)
    request_id: str = field(default="")
    query: str = field(default="")
    metadata: Dict[str, Any] = field(default_factory=dict)

class FlowManager:
    """Gère le flux des requêtes avec priorisation et routage."""
    
    def __init__(self):
        """Initialise le gestionnaire de flux."""
        self.request_queue = PriorityQueue()
        self.logger = self._setup_logger()
        self.request_counter = 0
        self.lock = threading.Lock()
        
    def _setup_logger(self) -> logging.Logger:
        """Configure le système de logging."""
        logger = logging.getLogger('FlowManager')
        logger.setLevel(logging.INFO)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        return logger
    
    def add_request(self, query: str, priority: int = 1, metadata: Dict[str, Any] = None) -> str:
        """
        Ajoute une requête à la file d'attente.
        
        Args:
            query: La requête à traiter
            priority: Priorité de la requête (1 = normal, 2 = élevée, 3 = urgente)
            metadata: Métadonnées supplémentaires
            
        Returns:
            ID de la requête
        """
        with self.lock:
            self.request_counter += 1
            request_id = f"REQ_{self.request_counter}"
        
        request = PrioritizedRequest(
            priority=priority,
            request_id=request_id,
            query=query,
            metadata=metadata or {}
        )
        
        self.request_queue.put((-priority, request))  # Négatif pour que la priorité la plus élevée sorte en premier
        self.logger.info(f"Nouvelle requête ajoutée: {request_id} (priorité: {priority})")
        
        return request_id
    
    def get_next_request(self) -> Optional[PrioritizedRequest]:
        """
        Récupère la prochaine requête à traiter.
        
        Returns:
            La prochaine requête prioritaire ou None si la file est vide
        """
        try:
            _, request = self.request_queue.get_nowait()
            self.logger.info(f"Requête récupérée: {request.request_id}")
            return request
        except:
            return None
    
    def get_queue_status(self) -> Dict[str, Any]:
        """
        Retourne l'état actuel de la file d'attente.
        
        Returns:
            Dict contenant les statistiques de la file
        """
        return {
            "queue_size": self.request_queue.qsize(),
            "timestamp": datetime.now().isoformat()
        }

# Exemple d'utilisation
if __name__ == "__main__":
    # Création du gestionnaire de flux
    flow_manager = FlowManager()
    
    # Ajout de quelques requêtes avec différentes priorités
    requests = [
        ("Où est le chat ?", 1),
        ("Urgent: Où est le chat ?", 3),
        ("Question sur le chat", 2)
    ]
    
    print("=== Test du Flow Manager ===")
    
    # Ajout des requêtes
    for query, priority in requests:
        request_id = flow_manager.add_request(query, priority)
        print(f"Requête ajoutée: {request_id} (priorité: {priority})")
    
    # Récupération des requêtes dans l'ordre de priorité
    print("\nRécupération des requêtes:")
    while True:
        request = flow_manager.get_next_request()
        if request is None:
            break
        print(f"\nRequête traitée: {request.request_id}")
        print(f"Query: {request.query}")
        print(f"Priorité: {request.priority}")
    
    # État final de la file
    status = flow_manager.get_queue_status()
    print(f"\nTaille finale de la file: {status['queue_size']}") 