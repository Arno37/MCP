import unittest
import time
from unittest.mock import patch
from src.orchestration.core import Orchestrator
from src.orchestration.flow_manager import FlowManager
from tests.mocks import MockVectorStore

class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        """Initialisation avant chaque test."""
        # Patch de l'import du VectorStore
        self.patcher = patch('src.orchestration.core.VectorStore', MockVectorStore)
        self.patcher.start()
        
        self.orchestrator = Orchestrator()
    
    def tearDown(self):
        """Nettoyage après chaque test."""
        self.patcher.stop()
    
    def test_flow_manager_prioritization(self):
        """Teste la priorisation des requêtes."""
        # Création d'un FlowManager
        flow_manager = FlowManager()
        
        # Ajout de requêtes avec différentes priorités
        requests = [
            ("Requête normale", 1),
            ("Requête urgente", 3),
            ("Requête importante", 2)
        ]
        
        # Soumission des requêtes
        for query, priority in requests:
            flow_manager.add_request(query, priority)
        
        # Vérification de l'ordre de traitement
        expected_order = [3, 2, 1]  # Ordre des priorités attendu
        for expected_priority in expected_order:
            request = flow_manager.get_next_request()
            self.assertIsNotNone(request)
            self.assertEqual(request.priority, expected_priority)
    
    def test_orchestrator_processing(self):
        """Teste le traitement des requêtes par l'orchestrateur."""
        # Démarrage du traitement
        self.orchestrator.start_processing()
        
        # Soumission de requêtes
        request_ids = []
        for i in range(3):
            request_id = self.orchestrator.submit_request(
                f"Test requête {i}",
                priority=1
            )
            request_ids.append(request_id)
        
        # Attente du traitement
        time.sleep(1)
        
        # Vérification du statut
        status = self.orchestrator.get_system_status()
        self.assertEqual(status["status"], "operational")
        
        # Arrêt du traitement
        self.orchestrator.stop_processing()
    
    def test_system_status(self):
        """Teste la récupération du statut du système."""
        status = self.orchestrator.get_system_status()
        
        # Vérification des champs essentiels
        self.assertIn("status", status)
        self.assertIn("components", status)
        self.assertIn("retrieval", status["components"])
        self.assertIn("flow_manager", status["components"])
        
        # Vérification des valeurs
        self.assertEqual(status["status"], "operational")
        self.assertEqual(status["components"]["retrieval"]["status"], "active")
        self.assertEqual(len(status["components"]["retrieval"]["documents_count"]), 2)
    
    def test_error_handling(self):
        """Teste la gestion des erreurs."""
        # Test avec une requête vide
        request_id = self.orchestrator.submit_request("")
        
        # Vérification que le système reste opérationnel
        status = self.orchestrator.get_system_status()
        self.assertEqual(status["status"], "operational")
    
    def test_document_search(self):
        """Teste la recherche de documents."""
        # Ajout d'un document
        doc_id = self.orchestrator.retrieval.add_document(
            "Ceci est un nouveau document",
            {"file_name": "new.txt"}
        )
        
        # Recherche du document
        results = self.orchestrator.retrieval.search("nouveau")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["document"]["file_name"], "new.txt")

if __name__ == "__main__":
    unittest.main() 