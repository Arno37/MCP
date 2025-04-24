import requests
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def generate_response_ollama(
    question: str, 
    context_chunks: List[Dict[str, Any]], 
    model_name: str = "mistral", # Modèle à utiliser avec Ollama
    ollama_base_url: str = "http://localhost:11434" # URL de base d'Ollama
) -> str:
    """
    Génère une réponse à une question en utilisant les chunks de contexte fournis,
    via un modèle hébergé par Ollama.

    Args:
        question: La question originale de l'utilisateur.
        context_chunks: Une liste de dictionnaires, chaque dict contenant au moins 
                        une clé 'content' avec le texte du chunk pertinent.
        model_name: Le nom du modèle à utiliser dans Ollama (doit être préalablement 'pulled').
        ollama_base_url: L'URL où l'API d'Ollama est accessible.

    Returns:
        La réponse textuelle générée par le modèle, ou un message d'erreur.
    """
    
    prompt = build_prompt(question, context_chunks)
    
    # Log détaillé du prompt (attention si très long ou contient des données sensibles)
    # logger.debug(f"Prompt complet envoyé à Ollama:\n---\n{prompt}\n---")
    
    api_url = f"{ollama_base_url}/api/generate"
    
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False, # On veut la réponse complète, pas en streaming
        "options": { # Quelques options possibles, peuvent être ajustées
            "temperature": 0.7,
            # "num_ctx": 4096 # Taille du contexte si besoin d'ajuster
        }
    }

    try:
        logger.info(f"Envoi de la requête à Ollama (modèle: {model_name}) pour la question: '{question[:50]}...'")
        # Ajout d'un timeout généreux (ex: 300 secondes = 5 minutes)
        response = requests.post(api_url, json=payload, timeout=300)
        logger.info(f"Réponse reçue d'Ollama avec statut HTTP: {response.status_code}")

        # Log du contenu brut de la réponse pour débogage
        # logger.debug(f"Contenu brut de la réponse Ollama: {response.text}")
        
        response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)

        # Traitement de la réponse JSON d'Ollama
        response_data = response.json()
        
        if "response" in response_data:
            final_response = response_data["response"].strip()
            logger.info("Réponse reçue d'Ollama.")
            # Log potentiel des métriques de performance si disponibles
            # eval_count = response_data.get('eval_count')
            # eval_duration = response_data.get('eval_duration')
            # if eval_count and eval_duration:
            #    logger.debug(f"Ollama eval metrics: count={eval_count}, duration={eval_duration/1e9:.2f}s")
            return final_response
        else:
            logger.error(f"Réponse inattendue d'Ollama: {response_data}")
            return "Erreur: Réponse inattendue reçue d'Ollama."

    except requests.exceptions.ConnectionError:
        logger.error(f"Erreur de connexion à Ollama à l'adresse {api_url}. Assurez-vous qu'Ollama est lancé.")
        return f"Erreur: Impossible de se connecter au serveur Ollama à {api_url}."
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de la requête à Ollama: {e}")
        # Essayer d'extraire plus de détails si la réponse contient du JSON malgré l'erreur
        try:
            error_details = response.json()
            logger.error(f"Détails de l'erreur Ollama: {error_details}")
            error_msg = error_details.get("error", str(e))
        except (json.JSONDecodeError, AttributeError):
            error_msg = str(e)
        return f"Erreur lors de la communication avec Ollama: {error_msg}"
    except requests.exceptions.Timeout:
        logger.error(f"Timeout dépassé ({300}s) lors de l'attente de la réponse d'Ollama à {api_url}.")
        return f"Erreur: Timeout ({300}s) dépassé en attendant Ollama."
    except Exception as e:
        logger.exception(f"Erreur inattendue lors de la génération via Ollama: {e}")
        return f"Erreur inattendue: {e}"

def build_prompt(question: str, context_chunks: List[Dict[str, Any]]) -> str:
    """
    Construit le prompt pour le LLM en combinant la question et le contexte.
    Adaptez ce prompt selon les besoins et le modèle utilisé (Mistral ici).
    """
    
    context = "\n\n".join([chunk['content'] for chunk in context_chunks])
    
    # Prompt simple pour Mistral (peut être amélioré)
    # Note: Mistral fonctionne bien avec des instructions claires.
    prompt = f"""Contexte:
{context}

Question: {question}

En te basant uniquement sur le contexte fourni ci-dessus, réponds à la question de manière concise. Si le contexte ne permet pas de répondre, dis-le clairement.
Réponse:"""
    
    logger.debug(f"Prompt construit (longueur: {len(prompt)}):\n{prompt[:300]}...") # Log tronqué
    return prompt

# Pour ajouter le __init__.py nécessaire pour que src/generation soit un package
# (Créer un fichier vide __init__.py si ce n'est pas déjà fait)
# Par exemple, via un autre appel edit_file ou manuellement. 