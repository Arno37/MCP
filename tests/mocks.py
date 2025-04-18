"""Mocks pour les tests."""

class MockVectorStore:
    """Mock du VectorStore pour les tests."""
    
    def __init__(self):
        self.documents_metadata = ["doc1", "doc2"]
        self.initialized = False
        self.documents = [
            {
                "content": "Ceci est un test de document",
                "file_name": "test1.txt",
                "metadata": {"type": "test"}
            },
            {
                "content": "Un autre document de test",
                "file_name": "test2.txt",
                "metadata": {"type": "test"}
            }
        ]
    
    def initialize(self):
        """Initialise le mock."""
        self.initialized = True
    
    def search(self, query: str, k: int = 5):
        """Mock de la recherche."""
        if not self.initialized:
            raise Exception("VectorStore non initialisé")
            
        # Simulation d'une recherche basique
        results = []
        for doc in self.documents:
            if query.lower() in doc["content"].lower():
                results.append({
                    "document": doc,
                    "score": 0.8
                })
        
        return results[:k]
    
    def add_document(self, content: str, metadata: dict = None):
        """Mock de l'ajout de document."""
        if not self.initialized:
            raise Exception("VectorStore non initialisé")
            
        new_doc = {
            "content": content,
            "file_name": metadata.get("file_name", "new_doc.txt"),
            "metadata": metadata or {}
        }
        self.documents.append(new_doc)
        return len(self.documents) - 1
    
    def get_document_count(self):
        """Retourne le nombre de documents."""
        return len(self.documents) 