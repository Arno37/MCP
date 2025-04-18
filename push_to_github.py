"""Script pour pousser les fichiers sur GitHub."""
import os
import shutil
import subprocess

def create_archive():
    """Crée une archive des fichiers à pousser."""
    if os.path.exists("archive_to_push"):
        shutil.rmtree("archive_to_push")
    
    os.makedirs("archive_to_push/src/orchestration", exist_ok=True)
    os.makedirs("archive_to_push/tests", exist_ok=True)
    
    # Copie des fichiers src
    shutil.copy("src/__init__.py", "archive_to_push/src/")
    
    # Copie des fichiers orchestration
    for file in os.listdir("src/orchestration"):
        if file.endswith(".py"):
            shutil.copy(f"src/orchestration/{file}", f"archive_to_push/src/orchestration/{file}")
    
    # Copie des fichiers tests
    for file in ["__init__.py", "conftest.py", "mocks.py", "test_orchestrator.py"]:
        if os.path.exists(f"tests/{file}"):
            shutil.copy(f"tests/{file}", f"archive_to_push/tests/{file}")

def push_to_github():
    """Pousse les fichiers sur GitHub."""
    try:
        # Checkout de la branche develop
        subprocess.run(["git", "checkout", "develop"], check=True)
        
        # Copie des fichiers de l'archive vers le projet
        for root, dirs, files in os.walk("archive_to_push"):
            for file in files:
                src_path = os.path.join(root, file)
                dest_path = src_path.replace("archive_to_push/", "")
                
                # Création du répertoire si nécessaire
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                # Copie du fichier
                shutil.copy(src_path, dest_path)
        
        # Ajout des fichiers
        subprocess.run(["git", "add", "src/orchestration", "tests"], check=True)
        
        # Commit
        subprocess.run(["git", "commit", "-m", "Ajout de l'orchestrateur MCP"], check=True)
        
        # Push
        subprocess.run(["git", "push", "origin", "develop"], check=True)
        
        print("Fichiers poussés avec succès sur la branche develop.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande Git : {e}")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    create_archive()
    push_to_github() 