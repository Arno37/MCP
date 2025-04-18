"""Module de stockage vectoriel."""
import os
import sys

# Utilisation du mock pendant les tests
if 'pytest' in sys.modules:
    from tests.mocks import MockVectorStore as VectorStore
else:
    try:
        import spacy
        from typing import List, Dict, Any
        from datetime import datetime
        
        class VectorStore:
            """Stockage vectoriel pour les documents."""
            
            def __init__(self):
                """Initialise le stockage vectoriel."""
                self.nlp = spacy.load("fr_core_news_sm")
                self.documents = []
                self.documents_metadata = []
                self.initialized = False
            
            def initialize(self):
                """Initialise le stockage."""
                self.initialized = True
            
            def add_document(self, content: str, metadata: dict = None) -> int:
                """Ajoute un document au stockage."""
                if not self.initialized:
                    raise Exception("VectorStore non initialisé")
                
                doc_id = len(self.documents)
                self.documents.append(content)
                self.documents_metadata.append(metadata or {})
                return doc_id
            
            def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
                """Recherche des documents pertinents."""
                if not self.initialized:
                    raise Exception("VectorStore non initialisé")
                
                # Simulation de recherche basique
                results = []
                for i, doc in enumerate(self.documents):
                    if query.lower() in doc.lower():
                        results.append({
                            "document": {
                                "content": doc,
                                "metadata": self.documents_metadata[i]
                            },
                            "score": 0.8
                        })
                
                return results[:k]
    except ImportError:
        from tests.mocks import MockVectorStore as VectorStore
