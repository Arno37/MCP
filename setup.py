from setuptools import setup, find_packages

setup(
    name="mcp",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # Pas de dépendance à spacy pour les tests
    ],
) 