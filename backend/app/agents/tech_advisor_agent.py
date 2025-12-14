# app/agents/tech_advisor_agent.py

from typing import Dict, List, Any


class TechAdvisorAgent:
    """
    Agent qui recommande les technologies appropriées selon le projet
    """
    
    def __init__(self):
        self.name = "Tech Advisor"
    
    def recommend_stack(self, project_description: str) -> Dict[str, Any]:
        """
        Génère des recommendations technologiques selon le projet
        """
        desc_lower = project_description.lower()
        
        # Détection du projet
        is_web = any(word in desc_lower for word in ['site', 'web', 'application web'])
        is_mobile = any(word in desc_lower for word in ['mobile', 'ios', 'android', 'app mobile'])
        is_api = any(word in desc_lower for word in ['api', 'backend', 'serveur'])
        is_ecommerce = any(word in desc_lower for word in ['e-commerce', 'ecommerce', 'boutique', 'shop'])
        is_dashboard = any(word in desc_lower for word in ['dashboard', 'tableau de bord', 'analytics'])
        is_realtime = any(word in desc_lower for word in ['temps réel', 'realtime', 'chat', 'notification'])
        
        recommendations = {
            "frontend": [],
            "backend": [],
            "database": [],
            "devops": [],
            "tools": []
        }
        
        # Frontend
        if is_web:
            recommendations["frontend"].append({
                "name": "React + Next.js",
                "category": "Framework Frontend",
                "reason": "SSR performant, SEO optimisé, écosystème riche",
                "pros": ["Performance excellente", "SEO friendly", "Great DX"],
                "cons": ["Courbe d'apprentissage", "Bundle size"],
                "priority": "Recommandé"
            })
            recommendations["frontend"].append({
                "name": "TailwindCSS",
                "category": "CSS Framework",
                "reason": "Utility-first, responsive facile, customizable",
                "pros": ["Rapide à développer", "Consistant", "Performant"],
                "cons": ["HTML verbeux"],
                "priority": "Recommandé"
            })
            if is_dashboard:
                recommendations["frontend"].append({
                    "name": "Recharts / Chart.js",
                    "category": "Visualisation",
                    "reason": "Graphiques interactifs pour dashboards",
                    "pros": ["Facile à utiliser", "Personnalisable"],
                    "cons": ["Performance avec gros datasets"],
                    "priority": "Optionnel"
                })
        
        if is_mobile:
            recommendations["frontend"].append({
                "name": "React Native",
                "category": "Mobile Framework",
                "reason": "Code partagé iOS/Android, grande communauté",
                "pros": ["Cross-platform", "Même code que web", "Performance native"],
                "cons": ["Certains packages natifs nécessaires"],
                "priority": "Recommandé"
            })
            recommendations["frontend"].append({
                "name": "Expo",
                "category": "Toolchain Mobile",
                "reason": "Setup rapide, OTA updates, dev facile",
                "pros": ["Setup simple", "Updates OTA", "Dev cloud"],
                "cons": ["Limitations sur modules natifs"],
                "priority": "Recommandé"
            })
        
        # Backend
        if is_api or is_web or is_mobile:
            recommendations["backend"].append({
                "name": "FastAPI (Python)",
                "category": "Backend Framework",
                "reason": "API REST rapide, auto-doc, type safety",
                "pros": ["Très rapide", "Auto-documentation", "Async natif"],
                "cons": ["Nécessite Python 3.7+"],
                "priority": "Recommandé"
            })
            recommendations["backend"].append({
                "name": "Alternative: Node.js + Express",
                "category": "Backend Framework",
                "reason": "JavaScript fullstack, énorme écosystème",
                "pros": ["Un seul langage", "NPM ecosystem", "Async"],
                "cons": ["Moins structuré que FastAPI"],
                "priority": "Alternative"
            })
        
        if is_ecommerce:
            recommendations["backend"].append({
                "name": "Stripe API",
                "category": "Paiement",
                "reason": "Solution de paiement complète et sécurisée",
                "pros": ["Facile à intégrer", "Très sécurisé", "Mondial"],
                "cons": ["Frais de transaction"],
                "priority": "Recommandé"
            })
        
        if is_realtime:
            recommendations["backend"].append({
                "name": "WebSockets / Socket.io",
                "category": "Real-time",
                "reason": "Communication bidirectionnelle temps réel",
                "pros": ["Latence faible", "Facile à utiliser"],
                "cons": ["Complexité scaling"],
                "priority": "Requis"
            })
        
        # Database
        recommendations["database"].append({
            "name": "PostgreSQL",
            "category": "Base de données",
            "reason": "Relationnel robuste, ACID, performant",
            "pros": ["Fiable", "Features riches", "Open source"],
            "cons": ["Setup initial"],
            "priority": "Recommandé"
        })
        
        if is_realtime or is_dashboard:
            recommendations["database"].append({
                "name": "Redis",
                "category": "Cache / Real-time",
                "reason": "Cache ultra-rapide, pub/sub pour temps réel",
                "pros": ["Extrêmement rapide", "Pub/Sub natif"],
                "cons": ["En mémoire (limité par RAM)"],
                "priority": "Recommandé"
            })
        
        # DevOps
        recommendations["devops"].append({
            "name": "Docker",
            "category": "Conteneurisation",
            "reason": "Déploiement cohérent, isolation",
            "pros": ["Portable", "Reproductible", "Scalable"],
            "cons": ["Courbe d'apprentissage"],
            "priority": "Recommandé"
        })
        
        recommendations["devops"].append({
            "name": "GitHub Actions",
            "category": "CI/CD",
            "reason": "CI/CD intégré GitHub, facile à setup",
            "pros": ["Gratuit pour projets publics", "Bien intégré"],
            "cons": ["Limité sur plan gratuit"],
           "priority": "Recommandé"
        })
        
        if is_web:
            recommendations["devops"].append({
                "name": "Vercel / Netlify",
                "category": "Hébergement Frontend",
                "reason": "Deploy automatique, CDN global, SSL gratuit",
                "pros": ["Simple", "Rapide", "CDN"],
                "cons": ["Vendor lock-in"],
                "priority": "Recommandé"
            })
        
        # Tools
        recommendations["tools"].append({
            "name": "Git + GitHub",
            "category": "Version Control",
            "reason": "Standard industrie, collaboration facile",
            "pros": ["Standard", "Gratuit", "Outils nombreux"],
            "cons": ["Aucun"],
            "priority": "Essentiel"
        })
        
        recommendations["tools"].append({
            "name": "VSCode",
            "category": "IDE",
            "reason": "Extensions riches, léger, gratuit",
            "pros": ["Gratuit", "Performant", "Extensions"],
            "cons": ["Peut être lent avec gros projets"],
            "priority": "Recommandé"
        })
        
        if is_api:
            recommendations["tools"].append({
                "name": "Postman / Insomnia",
                "category": "API Testing",
                "reason": "Test et documentation d'API",
                "pros": ["Visuel", "Collections", "Mocking"],
                "cons": ["Peut être lourd"],
                "priority": "Utile"
            })
        
        return {
            "project_type": self._detect_project_type(desc_lower),
            "recommendations": recommendations,
            "summary": self._generate_summary(recommendations)
        }
    
    def _detect_project_type(self, desc_lower: str) -> str:
        """Détecte le type de projet"""
        if 'e-commerce' in desc_lower or 'ecommerce' in desc_lower:
            return "E-commerce"
        elif 'mobile' in desc_lower:
            return "Application Mobile"
        elif 'dashboard' in desc_lower or 'tableau de bord' in desc_lower:
            return "Dashboard / Analytics"
        elif 'api' in desc_lower:
            return "Backend API"
        elif 'site' in desc_lower or 'web' in desc_lower:
            return "Application Web"
        else:
            return "Projet Logiciel"
    
    def _generate_summary(self, recommendations: Dict) -> str:
        """Génère un résumé du stack"""
        parts = []
        
        if recommendations["frontend"]:
            frontend_names = [r["name"] for r in recommendations["frontend"][:2]]
            parts.append(f"Frontend: {', '.join(frontend_names)}")
        
        if recommendations["backend"]:
            backend_names = [r["name"] for r in recommendations["backend"][:2]]
            parts.append(f"Backend: {', '.join(backend_names)}")
        
        if recommendations["database"]:
            db_names = [r["name"] for r in recommendations["database"][:1]]
            parts.append(f"Database: {', '.join(db_names)}")
        
        return " | ".join(parts)
