from pathlib import Path
from typing import List, Dict, Any
import PyPDF2
import docx

class DocumentLoader:
    """Classe responsable du chargement des documents depuis différents formats.(PDF, DOCX, TXT)"""
    
    def __init__(self, documents_dir: str = "data/documents"):
        """Initialise le chargeur de documents avec le chemin du dossier source."""
        self.documents_dir = Path(documents_dir)
        if not self.documents_dir.exists():
            self.documents_dir.mkdir(parents=True, exist_ok=True)
    
    def load_pdf(self, file_path: str) -> str:
        """Charge le contenu d'un fichier PDF."""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"Erreur lors du chargement du PDF {file_path}: {str(e)}")
            return ""
    
    def load_docx(self, file_path: str) -> str:
        """Charge le contenu d'un fichier DOCX."""
        try:
            doc = docx.Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            print(f"Erreur lors du chargement du DOCX {file_path}: {str(e)}")
            return ""
    
    def load_text(self, file_path: str) -> str:
        """Charge le contenu d'un fichier texte."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Erreur lors du chargement du fichier texte {file_path}: {str(e)}")
            return ""
    
    def load_document(self, file_path: str) -> Dict[str, Any]:
        """Charge un document en fonction de son extension."""
        path = Path(file_path)
        content = ""
        
        if path.suffix.lower() == '.pdf':
            content = self.load_pdf(file_path)
        elif path.suffix.lower() == '.docx':
            content = self.load_docx(file_path)
        elif path.suffix.lower() in ['.txt', '.md']:
            content = self.load_text(file_path)
        else:
            print(f"Format de fichier non supporté: {path.suffix}")
        
        return {
            "file_path": str(path),
            "file_name": path.name,
            "content": content,
            "file_type": path.suffix.lower()
        }
    
    def load_all_documents(self) -> List[Dict[str, Any]]:
        """Charge tous les documents du dossier source."""
        documents = []
        for file_path in self.documents_dir.glob('*'):
            if file_path.is_file():
                doc = self.load_document(str(file_path))
                if doc["content"]:  # Ne garder que les documents chargés avec succès
                    documents.append(doc)
        return documents

# Exemple d'utilisation
if __name__ == "__main__":
    loader = DocumentLoader()
    documents = loader.load_all_documents()
    print(f"Nombre de documents chargés: {len(documents)}")
    for doc in documents:
        print(f"Document: {doc['file_name']}, Type: {doc['file_type']}")
