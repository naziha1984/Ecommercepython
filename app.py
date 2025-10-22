"""
Application Flask e-commerce avec système de recommandation intelligent.

Ce module contient l'application principale Flask qui gère :
- L'authentification des utilisateurs
- La gestion des produits et du panier
- Le système de recommandation personnalisé
- L'interface web complète

Auteur: Développeur Senior Python Full Stack
Date: 2024
"""

import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration de l'application Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre-cle-secrete-super-securisee-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialisation de la base de données
db = SQLAlchemy(app)

# Import des modèles après l'initialisation de db
from database.models import User, Product, Purchase, Cart

# Import du système de recommandation
from recommender.recommender import RecommendationEngine

# Initialisation du moteur de recommandation
recommendation_engine = RecommendationEngine()

@app.route('/')
def index():
    """
    Page d'accueil affichant tous les produits disponibles.
    
    Returns:
        render_template: Template HTML de la page d'accueil
    """
    try:
        # Récupération de tous les produits
        products = Product.query.all()
        logger.info(f"Affichage de {len(products)} produits sur la page d'accueil")
        
        # Récupération des recommandations si l'utilisateur est connecté
        recommendations = []
        if 'user_id' in session:
            user_id = session['user_id']
            recommendations = recommendation_engine.get_user_recommendations(user_id, limit=4)
            logger.info(f"Recommandations générées pour l'utilisateur {user_id}")
        
        return render_template('index.html', 
                             products=products, 
                             recommendations=recommendations)
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la page d'accueil: {e}")
        flash('Erreur lors du chargement des produits', 'error')
        return render_template('index.html', products=[], recommendations=[])

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Inscription d'un nouvel utilisateur.
    
    Returns:
        render_template ou redirect: Formulaire d'inscription ou redirection
    """
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            
            # Vérification de l'existence de l'utilisateur
            if User.query.filter_by(username=username).first():
                flash('Ce nom d\'utilisateur existe déjà', 'error')
                return render_template('register.html')
            
            if User.query.filter_by(email=email).first():
                flash('Cette adresse email est déjà utilisée', 'error')
                return render_template('register.html')
            
            # Création du nouvel utilisateur
            hashed_password = generate_password_hash(password)
            new_user = User(
                username=username,
                email=email,
                password_hash=hashed_password,
                created_at=datetime.utcnow()
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            logger.info(f"Nouvel utilisateur créé: {username}")
            flash('Compte créé avec succès ! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            logger.error(f"Erreur lors de l'inscription: {e}")
            db.session.rollback()
            flash('Erreur lors de la création du compte', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Connexion d'un utilisateur existant.
    
    Returns:
        render_template ou redirect: Formulaire de connexion ou redirection
    """
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                session['username'] = user.username
                logger.info(f"Connexion réussie pour l'utilisateur: {username}")
                flash('Connexion réussie !', 'success')
                return redirect(url_for('index'))
            else:
                flash('Nom d\'utilisateur ou mot de passe incorrect', 'error')
                
        except Exception as e:
            logger.error(f"Erreur lors de la connexion: {e}")
            flash('Erreur lors de la connexion', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Déconnexion de l'utilisateur.
    
    Returns:
        redirect: Redirection vers la page d'accueil
    """
    session.clear()
    flash('Vous avez été déconnecté', 'info')
    logger.info("Utilisateur déconnecté")
    return redirect(url_for('index'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """
    Page de détail d'un produit.
    
    Args:
        product_id (int): ID du produit à afficher
        
    Returns:
        render_template: Template HTML du détail du produit
    """
    try:
        product = Product.query.get_or_404(product_id)
        
        # Récupération des produits similaires basés sur les recommandations
        similar_products = []
        if 'user_id' in session:
            similar_products = recommendation_engine.get_similar_products(product_id, limit=4)
        
        logger.info(f"Affichage du produit {product_id}: {product.name}")
        return render_template('product.html', 
                             product=product, 
                             similar_products=similar_products)
    except Exception as e:
        logger.error(f"Erreur lors du chargement du produit {product_id}: {e}")
        flash('Produit non trouvé', 'error')
        return redirect(url_for('index'))

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    """
    Ajout d'un produit au panier.
    
    Args:
        product_id (int): ID du produit à ajouter
        
    Returns:
        redirect: Redirection vers le panier
    """
    if 'user_id' not in session:
        flash('Vous devez être connecté pour ajouter des produits au panier', 'error')
        return redirect(url_for('login'))
    
    try:
        user_id = session['user_id']
        product = Product.query.get_or_404(product_id)
        
        # Vérification si le produit est déjà dans le panier
        existing_cart_item = Cart.query.filter_by(
            user_id=user_id, 
            product_id=product_id
        ).first()
        
        if existing_cart_item:
            existing_cart_item.quantity += 1
        else:
            new_cart_item = Cart(
                user_id=user_id,
                product_id=product_id,
                quantity=1,
                added_at=datetime.utcnow()
            )
            db.session.add(new_cart_item)
        
        db.session.commit()
        logger.info(f"Produit {product_id} ajouté au panier de l'utilisateur {user_id}")
        flash(f'{product.name} ajouté au panier !', 'success')
        
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout au panier: {e}")
        db.session.rollback()
        flash('Erreur lors de l\'ajout au panier', 'error')
    
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    """
    Affichage du panier de l'utilisateur.
    
    Returns:
        render_template: Template HTML du panier
    """
    if 'user_id' not in session:
        flash('Vous devez être connecté pour voir votre panier', 'error')
        return redirect(url_for('login'))
    
    try:
        user_id = session['user_id']
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        
        # Calcul du total
        total = sum(item.product.price * item.quantity for item in cart_items)
        
        logger.info(f"Affichage du panier pour l'utilisateur {user_id}: {len(cart_items)} articles")
        return render_template('cart.html', cart_items=cart_items, total=total)
        
    except Exception as e:
        logger.error(f"Erreur lors du chargement du panier: {e}")
        flash('Erreur lors du chargement du panier', 'error')
        return render_template('cart.html', cart_items=[], total=0)

@app.route('/remove_from_cart/<int:cart_item_id>')
def remove_from_cart(cart_item_id):
    """
    Suppression d'un article du panier.
    
    Args:
        cart_item_id (int): ID de l'article à supprimer
        
    Returns:
        redirect: Redirection vers le panier
    """
    if 'user_id' not in session:
        flash('Vous devez être connecté', 'error')
        return redirect(url_for('login'))
    
    try:
        cart_item = Cart.query.get_or_404(cart_item_id)
        
        # Vérification que l'article appartient à l'utilisateur connecté
        if cart_item.user_id != session['user_id']:
            flash('Accès non autorisé', 'error')
            return redirect(url_for('cart'))
        
        db.session.delete(cart_item)
        db.session.commit()
        
        logger.info(f"Article {cart_item_id} supprimé du panier")
        flash('Article supprimé du panier', 'success')
        
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du panier: {e}")
        db.session.rollback()
        flash('Erreur lors de la suppression', 'error')
    
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    """
    Finalisation de la commande.
    
    Returns:
        redirect: Redirection vers l'historique des achats
    """
    if 'user_id' not in session:
        flash('Vous devez être connecté pour finaliser votre commande', 'error')
        return redirect(url_for('login'))
    
    try:
        user_id = session['user_id']
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        
        if not cart_items:
            flash('Votre panier est vide', 'error')
            return redirect(url_for('cart'))
        
        # Création des achats
        for cart_item in cart_items:
            purchase = Purchase(
                user_id=user_id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                purchase_date=datetime.utcnow()
            )
            db.session.add(purchase)
        
        # Suppression du panier
        Cart.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        
        logger.info(f"Commande finalisée pour l'utilisateur {user_id}: {len(cart_items)} articles")
        flash('Commande finalisée avec succès !', 'success')
        
        # Mise à jour du modèle de recommandation
        recommendation_engine.update_model()
        
        return redirect(url_for('purchase_history'))
        
    except Exception as e:
        logger.error(f"Erreur lors de la finalisation de la commande: {e}")
        db.session.rollback()
        flash('Erreur lors de la finalisation de la commande', 'error')
        return redirect(url_for('cart'))

@app.route('/purchase_history')
def purchase_history():
    """
    Historique des achats de l'utilisateur.
    
    Returns:
        render_template: Template HTML de l'historique
    """
    if 'user_id' not in session:
        flash('Vous devez être connecté pour voir votre historique', 'error')
        return redirect(url_for('login'))
    
    try:
        user_id = session['user_id']
        purchases = Purchase.query.filter_by(user_id=user_id).order_by(
            Purchase.purchase_date.desc()
        ).all()
        
        logger.info(f"Affichage de l'historique pour l'utilisateur {user_id}: {len(purchases)} achats")
        return render_template('purchase_history.html', purchases=purchases)
        
    except Exception as e:
        logger.error(f"Erreur lors du chargement de l'historique: {e}")
        flash('Erreur lors du chargement de l\'historique', 'error')
        return render_template('purchase_history.html', purchases=[])

@app.route('/recommendations')
def recommendations():
    """
    Page des recommandations personnalisées.
    
    Returns:
        render_template: Template HTML des recommandations
    """
    if 'user_id' not in session:
        flash('Vous devez être connecté pour voir vos recommandations', 'error')
        return redirect(url_for('login'))
    
    try:
        user_id = session['user_id']
        recommendations = recommendation_engine.get_user_recommendations(user_id, limit=8)
        
        logger.info(f"Recommandations générées pour l'utilisateur {user_id}: {len(recommendations)} produits")
        return render_template('recommendations.html', recommendations=recommendations)
        
    except Exception as e:
        logger.error(f"Erreur lors de la génération des recommandations: {e}")
        flash('Erreur lors de la génération des recommandations', 'error')
        return render_template('recommendations.html', recommendations=[])

@app.route('/admin/dashboard')
def admin_dashboard():
    """
    Dashboard administrateur avec visualisations.
    
    Returns:
        render_template: Template HTML du dashboard admin
    """
    try:
        # Statistiques générales
        total_users = User.query.count()
        total_products = Product.query.count()
        total_purchases = Purchase.query.count()
        
        # Produits les plus vendus
        popular_products = db.session.query(
            Product.name,
            db.func.sum(Purchase.quantity).label('total_sold')
        ).join(Purchase).group_by(Product.id).order_by(
            db.func.sum(Purchase.quantity).desc()
        ).limit(5).all()
        
        logger.info("Affichage du dashboard administrateur")
        return render_template('admin_dashboard.html',
                             total_users=total_users,
                             total_products=total_products,
                             total_purchases=total_purchases,
                             popular_products=popular_products)
        
    except Exception as e:
        logger.error(f"Erreur lors du chargement du dashboard admin: {e}")
        flash('Erreur lors du chargement du dashboard', 'error')
        return render_template('admin_dashboard.html',
                             total_users=0,
                             total_products=0,
                             total_purchases=0,
                             popular_products=[])

@app.errorhandler(404)
def not_found_error(error):
    """
    Gestionnaire d'erreur 404.
    
    Args:
        error: Erreur 404
        
    Returns:
        render_template: Page d'erreur 404
    """
    logger.warning(f"Page non trouvée: {request.url}")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """
    Gestionnaire d'erreur 500.
    
    Args:
        error: Erreur 500
        
    Returns:
        render_template: Page d'erreur 500
    """
    logger.error(f"Erreur interne du serveur: {error}")
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    """
    Point d'entrée de l'application Flask.
    """
    # Création des tables de base de données
    with app.app_context():
        db.create_all()
        logger.info("Tables de base de données créées")
    
    # Démarrage de l'application
    logger.info("Démarrage de l'application Flask e-commerce")
    app.run(debug=True, host='0.0.0.0', port=5000)

