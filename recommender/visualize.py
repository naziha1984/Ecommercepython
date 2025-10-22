"""
Module de visualisation pour le système de recommandation.

Ce module génère des graphiques et visualisations pour analyser
les performances et les patterns du système de recommandation.

Auteur: Développeur Senior Python Full Stack
Date: 2024
"""

import os
import sys
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# Ajout du répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from recommender.recommender import RecommendationEngine

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration des graphiques
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class RecommendationVisualizer:
    """
    Classe pour la visualisation des données de recommandation.
    """
    
    def __init__(self, output_dir: str = 'outputs'):
        """
        Initialise le visualiseur.
        
        Args:
            output_dir (str): Répertoire de sortie pour les graphiques
        """
        self.output_dir = output_dir
        self.engine = RecommendationEngine()
        
        # Création du répertoire de sortie
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info(f"Visualiseur initialisé avec répertoire de sortie: {output_dir}")
    
    def load_data(self):
        """
        Charge les données depuis la base de données.
        """
        try:
            with app.app_context():
                self.engine.load_data_from_database(db.session)
                self.engine.create_user_item_matrix()
                self.engine.compute_user_similarity()
                self.engine.compute_item_similarity()
                self.engine.compute_product_popularity()
                
            logger.info("Données chargées pour la visualisation")
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données: {e}")
            raise
    
    def plot_user_similarity_heatmap(self, figsize: Tuple[int, int] = (12, 10)):
        """
        Génère une heatmap de similarité entre utilisateurs.
        
        Args:
            figsize (Tuple[int, int]): Taille de la figure
        """
        try:
            if self.engine.user_similarity_df is None:
                logger.warning("Matrice de similarité utilisateurs non disponible")
                return
            
            fig, ax = plt.subplots(figsize=figsize)
            
            # Création de la heatmap
            sns.heatmap(
                self.engine.user_similarity_df,
                annot=True,
                fmt='.2f',
                cmap='coolwarm',
                center=0,
                square=True,
                ax=ax
            )
            
            ax.set_title('Matrice de Similarité Utilisateurs', fontsize=16, fontweight='bold')
            ax.set_xlabel('Utilisateurs', fontsize=12)
            ax.set_ylabel('Utilisateurs', fontsize=12)
            
            # Rotation des labels
            plt.xticks(rotation=45)
            plt.yticks(rotation=0)
            
            # Sauvegarde
            output_path = os.path.join(self.output_dir, 'user_similarity_heatmap.png')
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Heatmap de similarité utilisateurs sauvegardée: {output_path}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de la heatmap utilisateurs: {e}")
    
    def plot_item_similarity_heatmap(self, figsize: Tuple[int, int] = (12, 10)):
        """
        Génère une heatmap de similarité entre produits.
        
        Args:
            figsize (Tuple[int, int]): Taille de la figure
        """
        try:
            if self.engine.item_similarity_df is None:
                logger.warning("Matrice de similarité produits non disponible")
                return
            
            # Limitation à 20 produits pour la lisibilité
            similarity_subset = self.engine.item_similarity_df.iloc[:20, :20]
            
            fig, ax = plt.subplots(figsize=figsize)
            
            # Création de la heatmap
            sns.heatmap(
                similarity_subset,
                annot=True,
                fmt='.2f',
                cmap='viridis',
                center=0,
                square=True,
                ax=ax
            )
            
            ax.set_title('Matrice de Similarité Produits (Top 20)', fontsize=16, fontweight='bold')
            ax.set_xlabel('Produits', fontsize=12)
            ax.set_ylabel('Produits', fontsize=12)
            
            # Rotation des labels
            plt.xticks(rotation=45)
            plt.yticks(rotation=0)
            
            # Sauvegarde
            output_path = os.path.join(self.output_dir, 'item_similarity_heatmap.png')
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Heatmap de similarité produits sauvegardée: {output_path}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de la heatmap produits: {e}")
    
    def plot_product_popularity(self, top_n: int = 15, figsize: Tuple[int, int] = (12, 8)):
        """
        Génère un graphique des produits les plus populaires.
        
        Args:
            top_n (int): Nombre de produits à afficher
            figsize (Tuple[int, int]): Taille de la figure
        """
        try:
            if self.engine.product_popularity is None:
                logger.warning("Données de popularité des produits non disponibles")
                return
            
            # Top N produits
            top_products = self.engine.product_popularity.head(top_n)
            
            fig, ax = plt.subplots(figsize=figsize)
            
            # Création du graphique en barres
            bars = ax.bar(range(len(top_products)), top_products.values, color='skyblue', edgecolor='navy')
            
            # Configuration des axes
            ax.set_title(f'Top {top_n} Produits les Plus Populaires', fontsize=16, fontweight='bold')
            ax.set_xlabel('Produits', fontsize=12)
            ax.set_ylabel('Quantité Vendue', fontsize=12)
            
            # Labels des produits
            ax.set_xticks(range(len(top_products)))
            ax.set_xticklabels([f'Produit {pid}' for pid in top_products.index], rotation=45)
            
            # Ajout des valeurs sur les barres
            for i, bar in enumerate(bars):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{int(height)}', ha='center', va='bottom')
            
            # Sauvegarde
            output_path = os.path.join(self.output_dir, 'product_popularity.png')
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Graphique de popularité des produits sauvegardé: {output_path}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du graphique de popularité: {e}")
    
    def plot_user_activity_distribution(self, figsize: Tuple[int, int] = (12, 8)):
        """
        Génère un graphique de la distribution de l'activité utilisateur.
        
        Args:
            figsize (Tuple[int, int]): Taille de la figure
        """
        try:
            # Calcul de l'activité par utilisateur
            user_activity = self.engine.df.groupby('user_id')['quantity'].sum()
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
            
            # Histogramme de l'activité
            ax1.hist(user_activity.values, bins=20, color='lightblue', edgecolor='black', alpha=0.7)
            ax1.set_title('Distribution de l\'Activité Utilisateur', fontweight='bold')
            ax1.set_xlabel('Nombre d\'Articles Achetés')
            ax1.set_ylabel('Nombre d\'Utilisateurs')
            ax1.grid(True, alpha=0.3)
            
            # Box plot de l'activité
            ax2.boxplot(user_activity.values, vert=True)
            ax2.set_title('Box Plot de l\'Activité Utilisateur', fontweight='bold')
            ax2.set_ylabel('Nombre d\'Articles Achetés')
            ax2.grid(True, alpha=0.3)
            
            # Sauvegarde
            output_path = os.path.join(self.output_dir, 'user_activity_distribution.png')
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Graphique de distribution de l'activité utilisateur sauvegardé: {output_path}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du graphique d'activité: {e}")
    
    def plot_category_analysis(self, figsize: Tuple[int, int] = (12, 8)):
        """
        Génère une analyse des catégories de produits.
        
        Args:
            figsize (Tuple[int, int]): Taille de la figure
        """
        try:
            # Récupération des données de produits depuis la base
            with app.app_context():
                from database.models import Product
                products = db.session.query(Product).all()
                
                # Création d'un DataFrame des produits
                product_data = []
                for product in products:
                    product_data.append({
                        'id': product.id,
                        'name': product.name,
                        'category': product.category,
                        'price': product.price
                    })
                
                products_df = pd.DataFrame(product_data)
            
            if products_df.empty:
                logger.warning("Aucune donnée de produit disponible pour l'analyse des catégories")
                return
            
            # Analyse par catégorie
            category_stats = products_df.groupby('category').agg({
                'id': 'count',
                'price': ['mean', 'std']
            }).round(2)
            
            category_stats.columns = ['Nombre_Produits', 'Prix_Moyen', 'Prix_Std']
            category_stats = category_stats.sort_values('Nombre_Produits', ascending=False)
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
            
            # Graphique du nombre de produits par catégorie
            category_stats['Nombre_Produits'].plot(kind='bar', ax=ax1, color='lightcoral')
            ax1.set_title('Nombre de Produits par Catégorie', fontweight='bold')
            ax1.set_xlabel('Catégorie')
            ax1.set_ylabel('Nombre de Produits')
            ax1.tick_params(axis='x', rotation=45)
            
            # Graphique du prix moyen par catégorie
            category_stats['Prix_Moyen'].plot(kind='bar', ax=ax2, color='lightgreen')
            ax2.set_title('Prix Moyen par Catégorie', fontweight='bold')
            ax2.set_xlabel('Catégorie')
            ax2.set_ylabel('Prix Moyen (€)')
            ax2.tick_params(axis='x', rotation=45)
            
            # Sauvegarde
            output_path = os.path.join(self.output_dir, 'category_analysis.png')
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Analyse des catégories sauvegardée: {output_path}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'analyse des catégories: {e}")
    
    def plot_recommendation_quality_metrics(self, figsize: Tuple[int, int] = (12, 8)):
        """
        Génère des métriques de qualité des recommandations.
        
        Args:
            figsize (Tuple[int, int]): Taille de la figure
        """
        try:
            # Test des différentes méthodes de recommandation
            test_users = self.engine.df['user_id'].unique()[:5]
            methods = ['user', 'item', 'popular', 'hybrid']
            
            results = {}
            
            for method in methods:
                method_results = []
                for user_id in test_users:
                    recommendations = self.engine.get_user_recommendations(user_id, limit=5, method=method)
                    method_results.append(len(recommendations))
                
                results[method] = method_results
            
            # Création du graphique
            fig, ax = plt.subplots(figsize=figsize)
            
            # Box plot des résultats
            method_data = [results[method] for method in methods]
            box_plot = ax.boxplot(method_data, labels=methods, patch_artist=True)
            
            # Coloration des box plots
            colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow']
            for patch, color in zip(box_plot['boxes'], colors):
                patch.set_facecolor(color)
            
            ax.set_title('Qualité des Recommandations par Méthode', fontweight='bold')
            ax.set_xlabel('Méthode de Recommandation')
            ax.set_ylabel('Nombre de Recommandations Générées')
            ax.grid(True, alpha=0.3)
            
            # Sauvegarde
            output_path = os.path.join(self.output_dir, 'recommendation_quality_metrics.png')
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Métriques de qualité des recommandations sauvegardées: {output_path}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la création des métriques de qualité: {e}")
    
    def generate_all_visualizations(self):
        """
        Génère toutes les visualisations disponibles.
        """
        try:
            logger.info("Génération de toutes les visualisations...")
            
            # Chargement des données
            self.load_data()
            
            # Génération des graphiques
            self.plot_user_similarity_heatmap()
            self.plot_item_similarity_heatmap()
            self.plot_product_popularity()
            self.plot_user_activity_distribution()
            self.plot_category_analysis()
            self.plot_recommendation_quality_metrics()
            
            logger.info("Toutes les visualisations ont été générées avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération des visualisations: {e}")
            raise

def main():
    """
    Fonction principale pour générer les visualisations.
    """
    try:
        logger.info("="*60)
        logger.info("GÉNÉRATION DES VISUALISATIONS")
        logger.info("="*60)
        
        # Initialisation du visualiseur
        visualizer = RecommendationVisualizer()
        
        # Génération de toutes les visualisations
        visualizer.generate_all_visualizations()
        
        logger.info("="*60)
        logger.info("VISUALISATIONS GÉNÉRÉES AVEC SUCCÈS")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution: {e}")
        raise

if __name__ == '__main__':
    main()

