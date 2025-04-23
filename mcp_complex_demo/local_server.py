# mcp_complex_demo/local_server.py
from flask import Flask, jsonify
import os

app = Flask(__name__)
PORT = 5001
LOCAL_FILE = "ma_note_locale.txt"

@app.route('/get_note', methods=['GET'])
def get_note():
    """Endpoint pour récupérer le contenu du fichier local."""
    print(f"[Local Server:{PORT}] Reçu demande pour /get_note")
    try:
        # Utiliser abspath pour être sûr d'avoir le chemin absolu du script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"[Local Server:{PORT}] Répertoire du script: {script_dir}") # Impression de débogage
        file_path = os.path.join(script_dir, LOCAL_FILE)
        print(f"[Local Server:{PORT}] Chemin complet calculé: {file_path}") # Impression de débogage

        if not os.path.exists(file_path):
             # Message d'erreur plus précis
             print(f"[Local Server:{PORT}] ERREUR: Fichier '{LOCAL_FILE}' non trouvé au chemin calculé.")
             return jsonify({"error": f"Fichier local '{LOCAL_FILE}' introuvable au chemin: {file_path}"}), 404

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"[Local Server:{PORT}] Fichier lu avec succès.")
        return jsonify({"data": content})
    except Exception as e:
        print(f"[Local Server:{PORT}] ERREUR: {e}")
        return jsonify({"error": f"Impossible de lire le fichier local: {e}"}), 500

if __name__ == '__main__':
    print(f"--- Serveur MCP Local démarré sur http://localhost:{PORT} ---")
    # host='0.0.0.0' permet d'écouter sur toutes les interfaces réseau
    # debug=True pour le rechargement automatique (utile en dév)
    app.run(host='0.0.0.0', port=PORT, debug=True) 