from typing import List, Dict, Any
import re

class TextSplitter:
    """Classe responsable du découpage du texte en chunks pour le traitement."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialise le découpeur de texte.
        
        Args:
            chunk_size: Taille maximale d'un chunk en caractères
            chunk_overlap: Nombre de caractères de chevauchement entre les chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str) -> List[str]:
        """Découpe le texte en chunks de taille appropriée."""
        if not text:
            return []
        
        # Nettoyage initial du texte
        text = self._clean_text(text)
        
        # Découpage en phrases (approximation)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            
            # Si la phrase est plus grande que chunk_size, on la découpe
            if sentence_size > self.chunk_size:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = []
                    current_size = 0
                
                # Découpage de la grande phrase
                words = sentence.split()
                temp_chunk = []
                temp_size = 0
                
                for word in words:
                    word_size = len(word) + 1  # +1 pour l'espace
                    if temp_size + word_size > self.chunk_size:
                        chunks.append(" ".join(temp_chunk))
                        temp_chunk = []
                        temp_size = 0
                    temp_chunk.append(word)
                    temp_size += word_size
                
                if temp_chunk:
                    chunks.append(" ".join(temp_chunk))
                continue
            
            # Ajout normal de la phrase au chunk courant
            if current_size + sentence_size > self.chunk_size:
                chunks.append(" ".join(current_chunk))
                # Gestion du chevauchement
                if self.chunk_overlap > 0:
                    overlap_words = " ".join(current_chunk).split()[-self.chunk_overlap//5:]  # Approximation
                    current_chunk = overlap_words
                    current_size = len(" ".join(current_chunk))
                else:
                    current_chunk = []
                    current_size = 0
            
            current_chunk.append(sentence)
            current_size += sentence_size + 1  # +1 pour l'espace
        
        # Ajout du dernier chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """Nettoie le texte avant le découpage."""
        # Suppression des espaces multiples
        text = re.sub(r'\s+', ' ', text)
        # Suppression des sauts de ligne multiples
        text = re.sub(r'\n+', '\n', text)
        return text.strip()
    
    def process_document(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Traite un document complet et retourne ses chunks."""
        chunks = self.split_text(document["content"])
        return [
            {
                "file_path": document["file_path"],
                "file_name": document["file_name"],
                "chunk_index": i,
                "content": chunk,
                "file_type": document["file_type"]
            }
            for i, chunk in enumerate(chunks)
        ]

# Exemple d'utilisation
if __name__ == "__main__":
    splitter = TextSplitter(chunk_size=500, chunk_overlap=100)
    test_text = "Ceci est un texte de test. Il contient plusieurs phrases. Chaque phrase devrait être correctement découpée. Le chevauchement entre les chunks devrait être géré proprement."
    chunks = splitter.split_text(test_text)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {chunk[:50]}...")
