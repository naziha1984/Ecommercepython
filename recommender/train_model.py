"""
Script d'entraînement du modèle de recommandation.

Ce module entraîne et sauvegarde le modèle de recommandation intelligent
en utilisant les données de la base de données SQLite.

Auteur: Développeur Senior Python Full Stack
Date: 2024
"""

import os
import sys
import logging
from datetime import datetime

# Ajout du répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from recommender.recommender import RecommendationEngine

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def train_recommendation_model():
    """
    Entraîne le modèle de recommandation avec les données de la base.
    """
    try:
        logger.info("Début de l'entraînement du modèle de recommandation")
        
        # Initialisation du moteur de recommandation
        engine = RecommendationEngine()
        
        # Chargement des données depuis la base de données
        logger.info("Chargement des données depuis la base de données...")
        engine.load_data_from_database(db.session)
        
        if engine.df.empty:
            logger.warning("Aucune donnée d'achat trouvée dans la base de données")
            logger.info("Ajoutez des achats pour entraîner le modèle de recommandation")
            return
        
        # Création de la matrice utilisateur-produit
        logger.info("Création de la matrice utilisateur-produit...")
        engine.create_user_item_matrix()
        
        # Calcul de la similarité utilisateur
        logger.info("Calcul de la similarité entre utilisateurs...")
        engine.compute_user_similarity()
        
        # Calcul de la similarité produit
        logger.info("Calcul de la similarité entre produits...")
        engine.compute_item_similarity()
        
        # Entraînement du modèle SVD
        logger.info("Entraînement du modèle SVD...")
        engine.train_svd_model(n_components=min(50, engine.user_item_matrix.shape[1] - 1))
        
        # Calcul de la popularité des produits
        logger.info("Calcul de la popularité des produits...")
        engine.compute_product_popularity()
        
        # Sauvegarde du modèle
        logger.info("Sauvegarde du modèle...")
        engine.save_model()
        
        # Affichage des statistiques
        logger.info("Statistiques du modèle entraîné:")
        logger.info(f"- Nombre d'utilisateurs: {engine.user_item_matrix.shape[0]}")
        logger.info(f"- Nombre de produits: {engine.user_item_matrix.shape[1]}")
        logger.info(f"- Nombre d'interactions: {len(engine.df)}")
        
        # Test des recommandations pour quelques utilisateurs
        logger.info("Test des recommandations...")
        test_users = engine.df['user_id'].unique()[:3]
        
        for user_id in test_users:
            recommendations = engine.get_user_recommendations(user_id, limit=3)
            logger.info(f"Recommandations pour l'utilisateur {user_id}: {recommendations}")
        
        logger.info("Entraînement du modèle terminé avec succès")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'entraînement du modèle: {e}")
        raise

def evaluate_model():
    """
    Évalue les performances du modèle de recommandation.
    """
    try:
        logger.info("Début de l'évaluation du modèle")
        
        # Initialisation du moteur
        engine = RecommendationEngine()
        
        # Chargement des données
        engine.load_data_from_database(db.session)
        
        if engine.df.empty:
            logger.warning("Aucune donnée pour l'évaluation")
            return
        
        # Création de la matrice
        engine.create_user_item_matrix()
        
        # Calcul des métriques de base
        total_users = engine.user_item_matrix.shape[0]
        total_products = engine.user_item_matrix.shape[1]
        total_interactions = len(engine.df)
        
        # Calcul de la densité de la matrice
        density = (total_interactions / (total_users * total_products)) * 100
        
        # Calcul du nombre moyen d'achats par utilisateur
        avg_purchases_per_user = engine.df.groupby('user_id').size().mean()
        
        # Calcul du nombre moyen d'achats par produit
        avg_purchases_per_product = engine.df.groupby('product_id').size().mean()
        
        logger.info("Métriques d'évaluation:")
        logger.info(f"- Densité de la matrice: {density:.2f}%")
        logger.info(f"- Achats moyens par utilisateur: {avg_purchases_per_user:.2f}")
        logger.info(f"- Achats moyens par produit: {avg_purchases_per_product:.2f}")
        
        # Test de performance des algorithmes
        test_user = engine.df['user_id'].iloc[0]
        
        # Test des différentes méthodes
        methods = ['user', 'item', 'popular', 'hybrid']
        
        for method in methods:
            start_time = datetime.now()
            recommendations = engine.get_user_recommendations(test_user, limit=5, method=method)
            end_time = datetime.now()
            
            response_time = (end_time - start_time).total_seconds() * 1000
            
            logger.info(f"Méthode {method}: {len(recommendations)} recommandations en {response_time:.2f}ms")
        
        logger.info("Évaluation du modèle terminée")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'évaluation du modèle: {e}")
        raise

def main():
    """
    Fonction principale d'entraînement et d'évaluation.
    """
    try:
        with app.app_context():
            logger.info("="*60)
            logger.info("ENTRAÎNEMENT DU MODÈLE DE RECOMMANDATION")
            logger.info("="*60)
            
            # Entraînement du modèle
            train_recommendation_model()
            
            # Évaluation du modèle
            evaluate_model()
            
            logger.info("="*60)
            logger.info("ENTRAÎNEMENT TERMINÉ AVEC SUCCÈS")
            logger.info("="*60)
            
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution: {e}")
        raise

if __name__ == '__main__':
    main()

