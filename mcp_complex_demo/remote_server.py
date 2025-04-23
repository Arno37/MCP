# mcp_complex_demo/remote_server.py
from flask import Flask, jsonify
import requests

app = Flask(__name__)
PORT = 5002
REMOTE_API_URL = "https://jsonplaceholder.typicode.com/posts/1"

@app.route('/get_api_data', methods=['GET'])
def get_api_data():
    """Endpoint pour récupérer les données de l'API distante."""
    print(f"[Remote Server:{PORT}] Reçu demande pour /get_api_data")
    try:
        response = requests.get(REMOTE_API_URL, timeout=10)
        response.raise_for_status() # Vérifie les erreurs HTTP
        print(f"[Remote Server:{PORT}] Accès API réussi.")
        # On renvoie directement le JSON de la réponse de l'API externe
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"[Remote Server:{PORT}] ERREUR API: {e}")
        return jsonify({"error": f"Impossible d'accéder à l'API distante: {e}"}), 503 # 503 Service Unavailable
    except Exception as e: # Autres erreurs potentielles (ex: JSONDecodeError si l'API change)
        print(f"[Remote Server:{PORT}] ERREUR Générale: {e}")
        return jsonify({"error": f"Erreur interne du serveur distant: {e}"}), 500

if __name__ == '__main__':
    print(f"--- Serveur MCP Distant démarré sur http://localhost:{PORT} ---")
    app.run(host='0.0.0.0', port=PORT, debug=True) 