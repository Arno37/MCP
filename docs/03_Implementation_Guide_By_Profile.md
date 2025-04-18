# Guide d'Implémentation Sécurisée des MCP par Profil Client - [Date]

## 1. Introduction

*   Objectif : Fournir un guide pratique pour configurer et déployer l'intégration MCP pour différents profils de sécurité client, en s'appuyant sur l'architecture définie.
*   Public Cible : Équipes de déploiement, administrateurs système, consultants.
*   Prérequis : Compréhension de l'architecture d'intégration (`docs/02_Secure_Integration_Architecture.md`), accès aux composants (Gateway, Orchestrateur).

## 2. Rappel des Profils Clients

*   Description concise des profils de sécurité définis (ex: "Standard", "Restrictif", "Audit Élevé", etc.).
*   Référence aux politiques de sécurité associées (voir `src/mcp_orchestrator/security.py` ou configuration centrale).

## 3. Procédure d'Implémentation Générale

*   Étapes communes à tous les profils :
    *   Déploiement des composants (Gateway, Orchestrateur).
    *   Configuration de base de la connectivité réseau.
    *   Configuration du système de logging centralisé.
    *   Tests de connectivité initiaux.

## 4. Configuration par Profil Client

### 4.1. Profil "Standard"

*   **Objectifs de Sécurité :** Accès équilibré aux MCP autorisées avec filtrage modéré.
*   **Configuration de l'Orchestrateur :**
    *   Assigner le `client_profile` "standard".
    *   Vérifier les MCP autorisées dans la politique (`security.py/CLIENT_POLICIES["standard"]["allowed_mcps"]`).
*   **Configuration de la Secure Gateway (si applicable) :**
    *   Règles de firewall/routage spécifiques (si nécessaire).
    *   Configuration du niveau de logging.
*   **Configuration du Filtrage (`security.py`) :**
    *   Vérifier que `filter_level` est "medium".
    *   Adapter les règles de sanitization si besoin.
*   **Tests Spécifiques :**
    *   Vérifier l'accès aux MCP A et B.
    *   Vérifier le niveau de filtrage sur des requêtes/réponses test.
    *   Valider les logs générés.

### 4.2. Profil "Restrictif"

*   **Objectifs de Sécurité :** Accès limité aux MCP les plus critiques, filtrage élevé des données.
*   **Configuration de l'Orchestrateur :**
    *   Assigner le `client_profile` "profil_restrictif".
    *   Confirmer que seules les MCP autorisées (ex: MCP A) sont listées dans la politique.
*   **Configuration de la Secure Gateway (si applicable) :**
    *   Règles plus strictes pour limiter le trafic sortant uniquement vers les endpoints de la MCP A.
    *   Niveau de logging potentiellement plus élevé.
*   **Configuration du Filtrage (`security.py`) :**
    *   Vérifier que `filter_level` est "high".
    *   Implémenter/vérifier les règles de sanitization/anonymisation avancées (ex: suppression de mots-clés, redaction).
*   **Tests Spécifiques :**
    *   Vérifier l'accès UNIQUEMENT à la MCP A.
    *   Tester explicitement le refus d'accès à la MCP B.
    *   Valider l'efficacité du filtrage "high" sur des requêtes contenant des informations potentiellement sensibles.
    *   Analyser la verbosité des logs.

### 4.3. [Profil "Autre Profil Spécifique" - si défini]

*   *(Mêmes sections que pour les autres profils, adaptées aux objectifs spécifiques)*

## 5. Procédures de Vérification Post-Implémentation

*   Checklist des points à vérifier pour chaque déploiement :
    *   Configuration du profil client correcte.
    *   Accès aux MCP attendues (et refus pour les autres).
    *   Fonctionnement du filtrage/sanitization.
    *   Génération et accessibilité des logs d'audit.
    *   Tests fonctionnels de bout en bout avec des requêtes types.

## 6. Dépannage (Troubleshooting)

*   Problèmes courants et leurs solutions :
    *   Erreurs de connexion à la Gateway / aux MCP.
    *   Accès refusé inattendu (vérifier politique/profil).
    *   Problèmes de filtrage (trop/pas assez).
    *   Logs manquants ou incomplets.

## Annexe

*   Configuration d'exemple pour [Technologie Gateway spécifique].
*   Scripts de test utiles. 