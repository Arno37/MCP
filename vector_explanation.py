import spacy
import numpy as np

# Chargement du modèle
nlp = spacy.load("fr_core_news_md")

# Phrases à comparer
phrase1 = "Le chat est sur le tapis."
phrase2 = "Où est le chat ?"

# Traitement des phrases
doc1 = nlp(phrase1)
doc2 = nlp(phrase2)

print("=== Vecteurs des mots individuels ===")
print("\nPhrase 1 - 'Le chat est sur le tapis':")
for token in doc1:
    print(f"\nMot: '{token.text}'")
    print(f"Vecteur (5 premières dimensions): {token.vector[:5]}")

print("\nPhrase 2 - 'Où est le chat':")
for token in doc2:
    print(f"\nMot: '{token.text}'")
    print(f"Vecteur (5 premières dimensions): {token.vector[:5]}")

print("\n=== Vecteur de la phrase entière ===")
print(f"\nPhrase 1 - Vecteur complet (5 premières dimensions): {doc1.vector[:5]}")
print(f"Phrase 2 - Vecteur complet (5 premières dimensions): {doc2.vector[:5]}")

# Calcul de la similarité
similarity = doc1.similarity(doc2)
print(f"\nSimilarité entre les phrases: {similarity:.4f}")

# Explication
print("""
Explication:
1. Chaque mot a son propre vecteur (embedding)
2. Le vecteur de la phrase est la moyenne des vecteurs des mots
3. La similarité est calculée entre les vecteurs des phrases entières
4. Plus le score est proche de 1, plus les phrases sont similaires sémantiquement
""") 