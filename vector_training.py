import spacy
from spacy import displacy
import numpy as np

# Chargement du modèle
nlp = spacy.load("fr_core_news_md")

# Explication des dimensions
print("""
=== Comment sont choisies les 300 dimensions ? ===

1. Apprentissage automatique :
   - Le modèle est entraîné sur des millions de textes
   - Il apprend à représenter le sens des mots
   - Chaque dimension capture un aspect sémantique différent

2. Exemple de ce que capturent les dimensions :
   - Dimension 1 : Animé vs Inanimé
   - Dimension 2 : Humain vs Animal
   - Dimension 3 : Taille
   - Dimension 4 : Couleur
   - ... et ainsi de suite jusqu'à 300

3. Pourquoi 300 ?
   - C'est un compromis entre :
     * Précision (plus de dimensions = plus de détails)
     * Performance (moins de dimensions = calculs plus rapides)
   - 300 dimensions permettent de capturer :
     * Le sens des mots
     * Les relations entre les mots
     * Le contexte
     * Les nuances sémantiques

4. Comment le modèle apprend :
   - Il regarde comment les mots sont utilisés ensemble
   - Il apprend que "chat" et "chien" sont proches
   - Il apprend que "chat" et "table" sont différents
   - Les 300 dimensions reflètent ces relations
""")

# Démonstration avec des mots similaires et différents
mots = ["chat", "chien", "table", "chaise", "voiture"]
print("\n=== Similarité entre différents mots ===")
for mot1 in mots:
    doc1 = nlp(mot1)
    print(f"\nComparaison avec '{mot1}':")
    for mot2 in mots:
        if mot1 != mot2:
            doc2 = nlp(mot2)
            similarite = doc1.similarity(doc2)
            print(f"  - {mot2}: {similarite:.4f}")

print("""
Observation :
- 'chat' et 'chien' ont une similarité élevée (animaux)
- 'table' et 'chaise' ont une similarité élevée (meubles)
- 'chat' et 'table' ont une similarité faible (catégories différentes)
""") 