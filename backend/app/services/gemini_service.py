# Mock Gemini Service for Python 3.14 compatibility
# TODO: Replace with real google-generativeai when Python 3.14 support is available

import os
from dotenv import load_dotenv
from typing import List, Dict, Any
import json

load_dotenv()

# Mock implementation that generates reasonable default data
class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        print("⚠️  Using MOCK Gemini Service (Python 3.14 compatibility mode)")
        print("📝 Real AI generation will be available when google-generativeai supports Python 3.14")
    
    def generate_tasks(self, project_description: str) -> List[Dict[str, Any]]:
        """
        Génère des tâches basées sur la description du projet
        """
        # Analyse de la description pour personnaliser
        desc_lower = project_description.lower()
        
        tasks = []
        task_id = 1
        
        # Détecter le type de projet
        is_web = any(word in desc_lower for word in ['site', 'web', 'application', 'frontend', 'backend', 'api'])
        is_ecommerce = any(word in desc_lower for word in ['e-commerce', 'ecommerce', 'boutique', 'panier', 'paiement', 'stripe', 'paypal'])
        is_mobile = any(word in desc_lower for word in ['mobile', 'ios', 'android', 'app mobile'])
        is_data = any(word in desc_lower for word in ['data', 'donnée', 'analyse', 'dashboard', 'visualisation'])
        has_auth = any(word in desc_lower for word in ['authentification', 'login', 'utilisateur', 'compte'])
        has_admin = any(word in desc_lower for word in ['admin', 'administration', 'gestion'])
        
        # Phase 1: Planification
        tasks.append({
            "id": task_id,
            "title": f"Analyse des besoins - {project_description[:50]}...",
            "description": f"Analyser et documenter les besoins pour: {project_description[:100]}",
            "duration_days": 3,
            "priority": "high",
            "dependencies": "",
            "status": "todo",
            "order": task_id - 1
        })
        task_id += 1
        
        tasks.append({
            "id": task_id,
            "title": "Conception de l'architecture système",
            "description": "Définir l'architecture technique, les patterns et les technologies",
            "duration_days": 4,
            "priority": "high",
            "dependencies": "1",
            "status": "todo",
            "order": task_id - 1
        })
        task_id += 1
        
        if is_web or is_mobile:
            tasks.append({
                "id": task_id,
                "title": "Design UI/UX et maquettes",
                "description": "Créer les maquettes et définir l'expérience utilisateur",
                "duration_days": 5,
                "priority": "high",
                "dependencies": "1",
                "status": "todo",
                "order": task_id - 1
            })
            task_id += 1
        
        # Phase 2: Setup
        tasks.append({
            "id": task_id,
            "title": "Configuration de l'environnement de développement",
            "description": "Setup Git, CI/CD, outils de développement",
            "duration_days": 2,
            "priority": "medium",
            "dependencies": "2",
            "status": "todo",
            "order": task_id - 1
        })
        task_id += 1
        
        tasks.append({
            "id": task_id,
            "title": "Initialisation de la base de données",
            "description": "Création des schémas, migrations et seeders",
            "duration_days": 2,
            "priority": "high",
            "dependencies": f"{task_id-1}",
            "status": "todo",
            "order": task_id - 1
        })
        task_id += 1
        
        # Phase 3: Backend/API
        if is_web or is_mobile or is_ecommerce:
            tasks.append({
                "id": task_id,
                "title": "Développement de l'API REST",
                "description": "Créer les endpoints principaux de l'API",
                "duration_days": 7,
                "priority": "high",
                "dependencies": f"{task_id-1}",
                "status": "todo",
                "order": task_id - 1
            })
            task_id += 1
        
        # Authentification
        if has_auth:
            tasks.append({
                "id": task_id,
                "title": "Système d'authentification",
                "description": "Implémenter login, register, JWT/sessions",
                "duration_days": 4,
                "priority": "high",
                "dependencies": f"{task_id-1}",
                "status": "todo",
                "order": task_id - 1
            })
            task_id += 1
        
        # E-commerce spécifique
        if is_ecommerce:
            tasks.append({
                "id": task_id,
                "title": "Développement du système de panier",
                "description": "Panier d'achat avec ajout/suppression de produits",
                "duration_days": 5,
                "priority": "high",
                "dependencies": f"{task_id-2}",
                "status": "todo",
                "order": task_id - 1
            })
            task_id += 1
            
            tasks.append({
                "id": task_id,
                "title": "Intégration du paiement (Stripe/PayPal)",
                "description": "Implémenter le processus de paiement sécurisé",
                "duration_days": 6,
                "priority": "high",
                "dependencies": f"{task_id-1}",
                "status": "todo",
                "order": task_id - 1
            })
            task_id += 1
            
            tasks.append({
                "id": task_id,
                "title": "Gestion des stocks",
                "description": "Système de gestion des stocks et inventaire",
                "duration_days": 4,
                "priority": "medium",
                "dependencies": f"{task_id-2}",
                "status": "todo",
                "order": task_id - 1
            })
            task_id += 1
        
        # Phase 4: Frontend
        if is_web:
            tasks.append({
                "id": task_id,
                "title": "Développement des composants UI",
                "description": "Créer les composants réutilisables",
                "duration_days": 6,
                "priority": "high",
                "dependencies": "3",
                "status": "todo",
                "order": task_id - 1
            })
            task_id += 1
            
            tasks.append({
                "id": task_id,
                "title": "Intégration frontend-backend",
                "description": "Connecter l'interface avec l'API",
                "duration_days": 5,
                "priority": "high",
                "dependencies": f"{task_id-1}",
                "status": "todo",
                "order": task_id - 1
            })
            task_id += 1
        
        # Admin panel
        if has_admin:
            tasks.append({
                "id": task_id,
                "title": "Panel d'administration",
                "description": "Interface d'administration complète",
                "duration_days": 7,
                "priority": "medium",
                "dependencies": f"{task_id-1}",
                "status": "todo",
                "order": task_id - 1
            })
            task_id += 1
        
        # Phase 5: Tests
        tasks.append({
            "id": task_id,
            "title": "Tests unitaires",
            "description": "Écrire et exécuter les tests unitaires",
            "duration_days": 4,
            "priority": "medium",
            "dependencies": "",
            "status": "todo",
            "order": task_id - 1
        })
        task_id += 1
        
        tasks.append({
            "id": task_id,
            "title": "Tests d'intégration",
            "description": "Tester l'intégration des différents modules",
            "duration_days": 3,
            "priority": "medium",
            "dependencies": f"{task_id-1}",
            "status": "todo",
            "order": task_id - 1
        })
        task_id += 1
        
        # Phase 6: Déploiement
        tasks.append({
            "id": task_id,
            "title": "Configuration serveur de production",
            "description": "Setup du serveur, SSL, domaine",
            "duration_days": 2,
            "priority": "high",
            "dependencies": "",
            "status": "todo",
            "order": task_id - 1
        })
        task_id += 1
        
        tasks.append({
            "id": task_id,
            "title": "Déploiement en production",
            "description": "Premier déploiement et mise en ligne",
            "duration_days": 2,
            "priority": "high",
            "dependencies": f"{task_id-2},{task_id-1}",
            "status": "todo",
            "order": task_id - 1
        })
        task_id += 1
        
        tasks.append({
            "id": task_id,
            "title": "Documentation et formation",
            "description": "Rédaction de la documentation technique et utilisateur",
            "duration_days": 3,
            "priority": "medium",
            "dependencies": "",
            "status": "todo",
            "order": task_id - 1
        })
        
        return tasks
    
    def generate_user_stories(self, project_description: str) -> List[Dict[str, Any]]:
        """
        Génère des User Stories basées sur la description
        """
        desc_lower = project_description.lower()
        
        # Détection des types de projets
        is_ecommerce = any(word in desc_lower for word in ['e-commerce', 'ecommerce', 'boutique', 'panier', 'paiement'])
        has_users = any(word in desc_lower for word in ['utilisateur', 'user', 'compte', 'profil', 'login'])
        has_admin = any(word in desc_lower for word in ['admin', 'administration', 'gestion'])
        is_dashboard = any(word in desc_lower for word in ['dashboard', 'tableau de bord', 'visualisation', 'graphique'])
        
        stories = []
        story_id = 1
        
        # Story générique de départ
        stories.append({
            "id": story_id,
            "title": f"En tant qu'utilisateur, je veux utiliser {project_description[:40]}...",
            "description": f"Pouvoir accéder et utiliser les fonctionnalités principales: {project_description[:80]}",
            "points": 8,
            "priority": "Must Have",
            "status": "todo",
            "sprint": 1,
            "acceptance_criteria": "1. Interface accessible\\n2. Fonctionnalités principales disponibles\\n3. Navigation intuitive"
        })
        story_id += 1
        
        # Stories pour e-commerce
        if is_ecommerce:
            stories.append({
                "id": story_id,
                "title": "En tant que client, je veux ajouter des produits au panier afin de faire mes achats",
                "description": "Panier d'achat avec ajout, modification, suppression",
                "points": 8,
                "priority": "Must Have",
                "status": "todo",
                "sprint": 1,
                "acceptance_criteria": "1. Ajout au panier\\n2. Modification quantités\\n3. Suppression articles\\n4. Calcul total"
            })
            story_id += 1
            
            stories.append({
                "id": story_id,
                "title": "En tant que client, je veux procéder au paiement afin de finaliser ma commande",
                "description": "Processus de checkout avec paiement sécurisé",
                "points": 13,
                "priority": "Must Have",
                "status": "todo",
                "sprint": 1,
                "acceptance_criteria": "1. Formulaire de livraison\\n2. Choix mode de paiement\\n3. Paiement sécurisé\\n4. Confirmation commande"
            })
            story_id += 1
            
            stories.append({
                "id": story_id,
                "title": "En tant que client, je veux consulter mes commandes afin de suivre leur état",
                "description": "Historique et suivi des commandes",
                "points": 5,
                "priority": "Should Have",
                "status": "todo",
                "sprint": 2,
                "acceptance_criteria": "1. Liste des commandes\\n2. Détail commande\\n3. Statut de livraison"
            })
            story_id += 1
        
        # Stories pour système utilisateur
        if has_users:
            stories.append({
                "id": story_id,
                "title": "En tant qu'utilisateur, je veux créer un compte afin d'accéder au système",
                "description": "Inscription avec email et mot de passe",
                "points": 5,
                "priority": "Must Have",
                "status": "todo",
                "sprint": 1,
                "acceptance_criteria": "1. Formulaire d'inscription\\n2. Validation email\\n3. Création compte\\n4. Email de confirmation"
            })
            story_id += 1
            
            stories.append({
                "id": story_id,
                "title": "En tant qu'utilisateur, je veux me connecter afin d'accéder à mon espace",
                "description": "Connexion sécurisée",
                "points": 3,
                "priority": "Must Have",
                "status": "todo",
                "sprint": 1,
                "acceptance_criteria": "1. Login/password\\n2. Récupération mot de passe\\n3. Session sécurisée"
            })
            story_id += 1
            
            stories.append({
                "id": story_id,
                "title": "En tant qu'utilisateur, je veux modifier mon profil afin de mettre à jour mes informations",
                "description": "Gestion du profil utilisateur",
                "points": 3,
                "priority": "Should Have",
                "status": "todo",
                "sprint": 2,
                "acceptance_criteria": "1. Modification infos\\n2. Changement mot de passe\\n3. Upload avatar"
            })
            story_id += 1
        
        # Stories pour admin
        if has_admin:
            stories.append({
                "id": story_id,
                "title": "En tant qu'admin, je veux gérer le contenu afin de maintenir le système",
                "description": "Panel d'administration CRUD",
                "points": 13,
                "priority": "Must Have",
                "status": "todo",
                "sprint": 2,
                "acceptance_criteria": "1. Interface admin\\n2. CRUD complet\\n3. Recherche et filtres\\n4. Export données"
            })
            story_id += 1
            
            stories.append({
                "id": story_id,
                "title": "En tant qu'admin, je veux consulter les statistiques afin de suivre l'activité",
                "description": "Dashboard avec métriques clés",
                "points": 8,
                "priority": "Should Have",
                "status": "todo",
                "sprint": 2,
                "acceptance_criteria": "1. Métriques temps réel\\n2. Graphiques\\n3. Export rapports"
            })
            story_id += 1
        
        # Stories pour dashboard
        if is_dashboard:
            stories.append({
                "id": story_id,
                "title": "En tant qu'utilisateur, je veux visualiser mes données afin de prendre des décisions",
                "description": "Tableau de bord interactif",
                "points": 13,
                "priority": "Must Have",
                "status": "todo",
                "sprint": 1,
                "acceptance_criteria": "1. Graphiques interactifs\\n2. Filtres temporels\\n3. Export données"
            })
            story_id += 1
        
        # Stories communes
        stories.append({
            "id": story_id,
            "title": "En tant qu'utilisateur, je veux recevoir des notifications afin de rester informé",
            "description": "Système de notifications",
            "points": 5,
            "priority": "Could Have",
            "status": "todo",
            "sprint": 3,
            "acceptance_criteria": "1. Notifications temps réel\\n2. Historique\\n3. Préférences notifications"
        })
        story_id += 1
        
        stories.append({
            "id": story_id,
            "title": "En tant qu'utilisateur, je veux utiliser l'application sur mobile afin d'y accéder partout",
            "description": "Interface responsive mobile",
            "points": 8,
            "priority": "Should Have",
            "status": "todo",
            "sprint": 3,
            "acceptance_criteria": "1. Design responsive\\n2. Touch-friendly\\n3. Performance mobile"
        })
        
        return stories
    
    def _get_default_tasks(self) -> List[Dict[str, Any]]:
        """Fallback pour compatibilité"""
        return self.generate_tasks("Projet générique")
    
    def _get_default_stories(self) -> List[Dict[str, Any]]:
        """Fallback pour compatibilité"""
        return self.generate_user_stories("Projet générique")

# Instance globale
gemini_service = GeminiService()

