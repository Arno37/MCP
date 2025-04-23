# mcp_complex_demo/orchestrator.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
PORT = 5000
LOCAL_SERVER_URL = "http://localhost:5001/get_note"
REMOTE_SERVER_URL = "http://localhost:5002/get_api_data"

@app.route('/query', methods=['GET'])
def handle_query():
    """Endpoint principal qui reçoit les requêtes du client et route vers les serveurs MCP."""
    source_type = request.args.get('source', None) # Récupère le paramètre 'source' (?source=local)
    print(f"[Orchestrator:{PORT}] Reçu demande pour la source: {source_type}")

    if source_type == 'local':
        target_url = LOCAL_SERVER_URL
        print(f"[Orchestrator:{PORT}] Routage vers le serveur local: {target_url}")
    elif source_type == 'remote':
        target_url = REMOTE_SERVER_URL
        print(f"[Orchestrator:{PORT}] Routage vers le serveur distant: {target_url}")
    else:
        print(f"[Orchestrator:{PORT}] ERREUR: Type de source inconnu ou manquant: {source_type}")
        return jsonify({"error": "Paramètre 'source' manquant ou invalide (doit être 'local' ou 'remote')"}), 400

    # Tenter de contacter le serveur MCP approprié
    try:
        response = requests.get(target_url, timeout=5)
        response.raise_for_status() # Vérifie les erreurs HTTP du serveur contacté
        print(f"[Orchestrator:{PORT}] Réponse reçue du serveur MCP.")
        # Renvoyer la réponse JSON du serveur MCP directement au client
        return jsonify(response.json())
    except requests.exceptions.Timeout:
        print(f"[Orchestrator:{PORT}] ERREUR: Timeout en contactant {target_url}")
        return jsonify({"error": f"Timeout en contactant le serveur MCP à {target_url}"}), 504 # Gateway Timeout
    except requests.exceptions.ConnectionError:
        print(f"[Orchestrator:{PORT}] ERREUR: Echec de connexion à {target_url}")
        return jsonify({"error": f"Impossible de se connecter au serveur MCP à {target_url}"}), 502 # Bad Gateway
    except requests.exceptions.RequestException as e:
        print(f"[Orchestrator:{PORT}] ERREUR: Erreur de requête vers {target_url}: {e}")
        # Essayer de renvoyer l'erreur du serveur MCP si possible, sinon erreur générique
        try:
            return jsonify(e.response.json()), e.response.status_code
        except:
            return jsonify({"error": f"Erreur lors de la communication avec le serveur MCP: {e}"}), 500
    except Exception as e: # Autres erreurs
        print(f"[Orchestrator:{PORT}] ERREUR Générale: {e}")
        return jsonify({"error": f"Erreur interne de l'orchestrateur: {e}"}), 500


if __name__ == '__main__':
    print(f"--- Orchestrateur MCP démarré sur http://localhost:{PORT} ---")
    app.run(host='0.0.0.0', port=PORT, debug=True) 