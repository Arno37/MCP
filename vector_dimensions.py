import spacy
import numpy as np

# Chargement du modèle
nlp = spacy.load("fr_core_news_md")

# Phrases de différentes longueurs
phrases = [
    "Chat",  # 1 mot
    "Le chat",  # 2 mots
    "Le chat est sur le tapis",  # 6 mots
    "Le chat noir et blanc dort paisiblement sur le tapis rouge du salon"  # 13 mots
]

print("=== Dimensions des vecteurs ===")
for phrase in phrases:
    doc = nlp(phrase)
    print(f"\nPhrase: '{phrase}'")
    print(f"Nombre de mots: {len(doc)}")
    print(f"Dimension du vecteur: {len(doc.vector)}")
    print(f"5 premières dimensions: {doc.vector[:5]}")
    
    # Vérification que c'est bien un vecteur de 300 dimensions
    assert len(doc.vector) == 300, f"Le vecteur devrait avoir 300 dimensions, pas {len(doc.vector)}"

print("""
Explication:
1. Chaque mot est transformé en un vecteur de 300 dimensions
2. La phrase entière devient un vecteur de 300 dimensions (moyenne des mots)
3. La dimension est fixe (300) quelle que soit la longueur de la phrase
4. C'est comme une 'signature numérique' de la phrase
""") 