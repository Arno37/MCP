# mcp_complex_demo/client.py
import requests
import json

ORCHESTRATOR_URL = "http://localhost:5000/query"

def query_orchestrator(source_type):
    """Fonction pour interroger l'orchestrateur pour un type de source donné."""
    print(f"\n[Client] Envoi requête à l'orchestrateur pour source = '{source_type}'...")
    url = f"{ORCHESTRATOR_URL}?source={source_type}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Vérifie si l'orchestrateur a renvoyé une erreur HTTP
        print(f"[Client] Réponse reçue de l'orchestrateur pour source = '{source_type}' (Status: {response.status_code})")
        return response.json()
    except requests.exceptions.Timeout:
        print(f"[Client] ERREUR: Timeout en contactant l'orchestrateur à {ORCHESTRATOR_URL}")
        return {"error": "Timeout"}
    except requests.exceptions.ConnectionError:
         print(f"[Client] ERREUR: Connexion refusée par l'orchestrateur à {ORCHESTRATOR_URL} (Est-il démarré?)")
         return {"error": "Connection Refused"}
    except requests.exceptions.RequestException as e:
        print(f"[Client] ERREUR: Problème de requête vers l'orchestrateur: {e}")
        # Essayer d'afficher l'erreur JSON renvoyée par l'orchestrateur
        try:
             error_details = e.response.json()
             print(f"[Client] Détails de l'erreur de l'orchestrateur: {error_details}")
             return error_details
        except:
             return {"error": f"Erreur HTTP {e.response.status_code} de l'orchestrateur"}
    except Exception as e:
         print(f"[Client] ERREUR inattendue: {e}")
         return {"error": f"Erreur inattendue: {e}"}

if __name__ == "__main__":
    print("--- Client Démo MCP Complexe ---")

    # 1. Demander la donnée locale via l'orchestrateur
    local_data = query_orchestrator('local')
    print("\n>>> Donnée reçue (via Orchestrateur) pour source='local':")
    print(json.dumps(local_data, indent=2))
    print("-" * 40)

    # 2. Demander la donnée distante via l'orchestrateur
    remote_data = query_orchestrator('remote')
    print("\n>>> Donnée reçue (via Orchestrateur) pour source='remote':")
    print(json.dumps(remote_data, indent=2))
    print("-" * 40)

    # 3. Exemple d'appel invalide
    invalid_data = query_orchestrator('inconnu')
    print("\n>>> Donnée reçue (via Orchestrateur) pour source='inconnu':")
    print(json.dumps(invalid_data, indent=2))
    print("-" * 40)


    print("\n--- Fin du Client Démo ---") 