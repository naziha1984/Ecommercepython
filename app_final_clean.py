#!/usr/bin/env python3
"""
E-COMMERCE IA - APPLICATION FINALE PROPRE
Version complète et fonctionnelle avec toutes les fonctionnalités
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import logging
import os
from bson import ObjectId

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration de l'application Flask
app = Flask(__name__)
app.secret_key = 'ecommerce_ai_secret_key_2025_professional'

# Configuration MongoDB
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ecommerce-python'
mongo = PyMongo(app)

def test_mongodb_connection():
    """Test de connexion MongoDB."""
    try:
        mongo.db.command('ping')
        return True
    except Exception as e:
        logger.error(f"Erreur connexion MongoDB: {e}")
        return False

def get_products():
    """Récupère tous les produits actifs."""
    try:
        products_collection = mongo.db.product
        products = list(products_collection.find({'is_active': True}))
        
        # Conversion des ObjectId en string
        for product in products:
            product['id'] = str(product['_id'])
        
        return products
    except Exception as e:
        logger.error(f"Erreur chargement produits: {e}")
        return []

def create_sample_data():
    """Crée les données d'exemple si elles n'existent pas."""
    try:
        # Vérification des produits
        if mongo.db.product.count_documents({}) == 0:
            products_data = [
                # ÉLECTRONIQUE
                {
                    'name': 'iPhone 15 Pro',
                    'description': 'Smartphone Apple avec écran Super Retina XDR de 6,1 pouces, processeur A17 Pro, triple caméra 48MP',
                    'price': 1199.99,
                    'category': 'Electronique',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 50,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'MacBook Air M2',
                    'description': 'Ordinateur portable Apple avec puce M2, écran Liquid Retina 13,6 pouces, 8 Go RAM, 256 Go SSD',
                    'price': 1299.99,
                    'category': 'Electronique',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 30,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'AirPods Pro',
                    'description': 'Écouteurs sans fil Apple avec réduction de bruit active et audio spatial',
                    'price': 249.99,
                    'category': 'Electronique',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 100,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Samsung Galaxy S24',
                    'description': 'Smartphone Samsung avec écran Dynamic AMOLED 6,2 pouces, processeur Snapdragon 8 Gen 3',
                    'price': 999.99,
                    'category': 'Electronique',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 40,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'iPad Pro 12.9"',
                    'description': 'Tablette Apple avec écran Liquid Retina XDR 12,9 pouces, puce M2, 256 Go de stockage',
                    'price': 1099.99,
                    'category': 'Electronique',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 25,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Sony WH-1000XM5',
                    'description': 'Casque sans fil Sony avec réduction de bruit active et audio haute résolution',
                    'price': 399.99,
                    'category': 'Electronique',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 35,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                
                # MODE & VÊTEMENTS
                {
                    'name': 'Nike Air Max 270',
                    'description': 'Chaussures de sport Nike avec technologie Air Max pour un confort optimal',
                    'price': 150.00,
                    'category': 'Mode',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 75,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Adidas Ultraboost 22',
                    'description': 'Chaussures de course Adidas avec technologie Boost pour une énergie de retour maximale',
                    'price': 180.00,
                    'category': 'Mode',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 60,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Levi\'s 501 Original',
                    'description': 'Jean classique Levi\'s 501 en denim 100% coton, coupe droite intemporelle',
                    'price': 89.99,
                    'category': 'Mode',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 120,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Zara Blazer Femme',
                    'description': 'Blazer élégant Zara en laine mélangée, coupe moderne et professionnelle',
                    'price': 79.99,
                    'category': 'Mode',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 45,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Converse Chuck Taylor',
                    'description': 'Baskets iconiques Converse Chuck Taylor All Star en toile, design intemporel',
                    'price': 65.00,
                    'category': 'Mode',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 90,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                
                # MAISON & DÉCORATION
                {
                    'name': 'IKEA Billy Bibliothèque',
                    'description': 'Bibliothèque Billy IKEA en bois blanc, 5 étagères, dimensions 80x28x202 cm',
                    'price': 45.99,
                    'category': 'Maison',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 20,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Dyson V15 Detect',
                    'description': 'Aspirateur sans fil Dyson V15 Detect avec laser de détection de poussière',
                    'price': 699.99,
                    'category': 'Maison',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 15,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Nespresso Vertuo Plus',
                    'description': 'Machine à café Nespresso Vertuo Plus avec technologie Centrifusion',
                    'price': 199.99,
                    'category': 'Maison',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 30,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Philips Hue Starter Kit',
                    'description': 'Kit d\'éclairage intelligent Philips Hue avec 3 ampoules et pont de connexion',
                    'price': 149.99,
                    'category': 'Maison',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 25,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                
                # SPORT & FITNESS
                {
                    'name': 'Apple Watch Series 9',
                    'description': 'Montre connectée Apple Watch Series 9 avec GPS, écran Retina toujours allumé',
                    'price': 429.99,
                    'category': 'Sport',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 40,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Peloton Bike+',
                    'description': 'Vélo d\'intérieur Peloton Bike+ avec écran tactile 23,8 pouces et abonnement inclus',
                    'price': 2495.00,
                    'category': 'Sport',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 8,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Yoga Mat Premium',
                    'description': 'Tapis de yoga premium en caoutchouc naturel, dimensions 183x61x0.6 cm',
                    'price': 45.99,
                    'category': 'Sport',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 80,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                
                # BEAUTÉ & SOINS
                {
                    'name': 'Dyson Supersonic',
                    'description': 'Sèche-cheveux Dyson Supersonic avec technologie de flux d\'air intelligent',
                    'price': 399.99,
                    'category': 'Beaute',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 20,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'La Mer Crème de la Mer',
                    'description': 'Crème hydratante luxueuse La Mer avec Miracle Broth et algues marines',
                    'price': 195.00,
                    'category': 'Beaute',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 15,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Chanel No.5 Eau de Parfum',
                    'description': 'Parfum iconique Chanel No.5, flacon de 100ml, fragrance florale-aldéhydée',
                    'price': 120.00,
                    'category': 'Beaute',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 25,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                
                # LIVRES & ÉDUCATION
                {
                    'name': 'Python pour les Nuls',
                    'description': 'Livre d\'apprentissage Python pour débutants, édition 2024, 400 pages',
                    'price': 24.99,
                    'category': 'Education',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 50,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Kindle Paperwhite',
                    'description': 'Liseuse Amazon Kindle Paperwhite avec écran 6,8 pouces et éclairage intégré',
                    'price': 139.99,
                    'category': 'Education',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 35,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Cours en Ligne IA',
                    'description': 'Formation complète en Intelligence Artificielle, 40h de contenu vidéo',
                    'price': 199.99,
                    'category': 'Education',
                    'image_url': '/static/images/placeholder.svg',
                    'stock_quantity': 100,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                }
            ]
            
            mongo.db.product.insert_many(products_data)
            logger.info("Produits d'exemple créés")
        
        # Vérification des utilisateurs
        if mongo.db.users.count_documents({}) == 0:
            users_data = [
                {
                    'username': 'admin',
                    'email': 'admin@ecommerce.com',
                    'password_hash': generate_password_hash('admin123'),
                    'created_at': datetime.utcnow(),
                    'is_admin': True
                },
                {
                    'username': 'test',
                    'email': 'test@ecommerce.com',
                    'password_hash': generate_password_hash('test123'),
                    'created_at': datetime.utcnow(),
                    'is_admin': False
                }
            ]
            
            mongo.db.users.insert_many(users_data)
            logger.info("Utilisateurs d'exemple créés")
            
    except Exception as e:
        logger.error(f"Erreur création données: {e}")

# Routes principales
@app.route('/')
def index():
    """Page d'accueil."""
    try:
        # Test de connexion
        if not test_mongodb_connection():
            flash('Erreur de connexion à la base de données', 'error')
            return render_template('index.html', products=[], recommendations=[])
        
        # Récupération des produits
        products = get_products()
        
        # Si aucun produit, créer des données d'exemple
        if not products:
            create_sample_data()
            products = get_products()
        
        # Recommandations pour utilisateur connecté
        recommendations = []
        if 'user_id' in session and products:
            recommendations = products[:4]
        
        return render_template('index.html', products=products, recommendations=recommendations)
        
    except Exception as e:
        logger.error(f"Erreur page accueil: {e}")
        flash('Erreur lors du chargement de la page', 'error')
        return render_template('index.html', products=[], recommendations=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Connexion utilisateur."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = mongo.db.users.find_one({'username': username})
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['is_admin'] = user.get('is_admin', False)
            flash('Connexion réussie !', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Inscription utilisateur."""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Vérification si l'utilisateur existe déjà
        if mongo.db.users.find_one({'username': username}):
            flash('Ce nom d\'utilisateur existe déjà', 'error')
            return render_template('register.html')
        
        if mongo.db.users.find_one({'email': email}):
            flash('Cette adresse email existe déjà', 'error')
            return render_template('register.html')
        
        # Création du nouvel utilisateur
        user_data = {
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password),
            'created_at': datetime.utcnow(),
            'is_admin': False
        }
        
        mongo.db.users.insert_one(user_data)
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Déconnexion utilisateur."""
    session.clear()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('index'))

@app.route('/product/<product_id>')
def product_detail(product_id):
    """Détail d'un produit."""
    try:
        product = mongo.db.product.find_one({'_id': ObjectId(product_id)})
        
        if not product:
            flash('Produit non trouvé', 'error')
            return redirect(url_for('index'))
        
        product['id'] = str(product['_id'])
        return render_template('product.html', product=product)
        
    except Exception as e:
        logger.error(f"Erreur détail produit: {e}")
        flash('Erreur lors du chargement du produit', 'error')
        return redirect(url_for('index'))

@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    """Ajouter un produit au panier."""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Vous devez être connecté'}), 401
    
    try:
        product = mongo.db.product.find_one({'_id': ObjectId(product_id)})
        
        if not product:
            return jsonify({'success': False, 'message': 'Produit non trouvé'}), 404
        
        # Vérification du stock
        if product['stock_quantity'] <= 0:
            return jsonify({'success': False, 'message': 'Produit en rupture de stock'}), 400
        
        # Vérifier si le produit est déjà dans le panier
        existing_item = mongo.db.cart.find_one({
            'user_id': session['user_id'],
            'product_id': product_id
        })
        
        if existing_item:
            # Augmenter la quantité
            mongo.db.cart.update_one(
                {'_id': existing_item['_id']},
                {'$inc': {'quantity': 1}}
            )
        else:
            # Ajouter un nouvel article
            cart_item = {
                'user_id': session['user_id'],
                'product_id': product_id,
                'product_name': product['name'],
                'price': product['price'],
                'quantity': 1,
                'added_at': datetime.utcnow()
            }
            mongo.db.cart.insert_one(cart_item)
        
        return jsonify({
            'success': True, 
            'message': f'{product["name"]} ajouté au panier !',
            'product_name': product['name']
        })
        
    except Exception as e:
        logger.error(f"Erreur ajout panier: {e}")
        return jsonify({'success': False, 'message': 'Erreur lors de l\'ajout au panier'}), 500

@app.route('/cart')
def cart():
    """Page du panier."""
    if 'user_id' not in session:
        flash('Vous devez être connecté pour voir votre panier', 'warning')
        return redirect(url_for('login'))
    
    try:
        cart_items = list(mongo.db.cart.find({'user_id': session['user_id']}))
        
        # Calcul du total
        total = sum(item['price'] * item['quantity'] for item in cart_items)
        
        return render_template('cart.html', cart_items=cart_items, total=total)
        
    except Exception as e:
        logger.error(f"Erreur panier: {e}")
        flash('Erreur lors du chargement du panier', 'error')
        return redirect(url_for('index'))

@app.route('/remove_from_cart/<cart_item_id>')
def remove_from_cart(cart_item_id):
    """Supprimer un article du panier."""
    if 'user_id' not in session:
        flash('Vous devez être connecté', 'warning')
        return redirect(url_for('login'))
    
    try:
        mongo.db.cart.delete_one({'_id': ObjectId(cart_item_id), 'user_id': session['user_id']})
        flash('Article supprimé du panier', 'success')
    except Exception as e:
        logger.error(f"Erreur suppression panier: {e}")
        flash('Erreur lors de la suppression', 'error')
    
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    """Finaliser la commande."""
    if 'user_id' not in session:
        flash('Vous devez être connecté pour finaliser votre commande', 'warning')
        return redirect(url_for('login'))
    
    try:
        cart_items = list(mongo.db.cart.find({'user_id': session['user_id']}))
        
        if not cart_items:
            flash('Votre panier est vide', 'warning')
            return redirect(url_for('cart'))
        
        # Création de la commande
        total = sum(item['price'] * item['quantity'] for item in cart_items)
        
        purchase_data = {
            'user_id': session['user_id'],
            'items': cart_items,
            'total': total,
            'status': 'completed',
            'created_at': datetime.utcnow()
        }
        
        mongo.db.purchases.insert_one(purchase_data)
        
        # Vider le panier
        mongo.db.cart.delete_many({'user_id': session['user_id']})
        
        flash('Commande finalisée avec succès !', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        logger.error(f"Erreur checkout: {e}")
        flash('Erreur lors de la finalisation de la commande', 'error')
        return redirect(url_for('cart'))

@app.route('/recommendations')
def recommendations():
    """Page des statistiques de recommandation."""
    try:
        if 'user_id' not in session:
            flash('Vous devez être connecté pour voir les statistiques', 'warning')
            return redirect(url_for('login'))
        
        # Récupération des données pour les statistiques
        products_collection = mongo.db.product
        users_collection = mongo.db.users
        
        # Statistiques générales
        total_products = products_collection.count_documents({})
        active_products = products_collection.count_documents({'is_active': True})
        total_users = users_collection.count_documents({})
        
        # Produits les plus populaires (par stock)
        popular_products = list(products_collection.find({}).sort('stock_quantity', -1).limit(5))
        
        # Catégories
        categories = products_collection.distinct('category')
        
        # Statistiques par catégorie
        category_stats = []
        for category in categories:
            count = products_collection.count_documents({'category': category})
            category_stats.append({
                'name': category,
                'count': count
            })
        
        # Produits récents
        recent_products = list(products_collection.find({}).sort('created_at', -1).limit(3))
        
        return render_template('recommendations.html', 
                         total_products=total_products,
                         active_products=active_products,
                         total_users=total_users,
                         popular_products=popular_products,
                         category_stats=category_stats,
                         recent_products=recent_products)
        
    except Exception as e:
        logger.error(f"Erreur page recommandations: {e}")
        flash('Erreur lors du chargement des statistiques', 'error')
        return redirect(url_for('index'))

@app.route('/purchase_history')
def purchase_history():
    """Historique des achats."""
    if 'user_id' not in session:
        flash('Vous devez être connecté pour voir votre historique', 'warning')
        return redirect(url_for('login'))
    
    try:
        # Récupération des achats avec conversion des ObjectId
        purchases = list(mongo.db.purchases.find({'user_id': session['user_id']}).sort('created_at', -1))
        
        # Conversion des ObjectId en string pour chaque achat
        for purchase in purchases:
            purchase['id'] = str(purchase['_id'])
            # Conversion des ObjectId des items
            for item in purchase.get('items', []):
                if '_id' in item:
                    item['id'] = str(item['_id'])
        
        return render_template('purchase_history.html', purchases=purchases)
        
    except Exception as e:
        logger.error(f"Erreur historique: {e}")
        flash('Erreur lors du chargement de l\'historique', 'error')
        return redirect(url_for('index'))

@app.route('/api/cart/count')
def cart_count():
    """API pour récupérer le nombre d'articles dans le panier."""
    if 'user_id' not in session:
        return jsonify({'count': 0})
    
    try:
        count = mongo.db.cart.count_documents({'user_id': session['user_id']})
        return jsonify({'count': count})
    except Exception as e:
        logger.error(f"Erreur compteur panier: {e}")
        return jsonify({'count': 0})

# Routes d'administration
@app.route('/admin')
def admin_dashboard():
    """Dashboard administrateur."""
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('Accès refusé. Droits administrateur requis.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Statistiques générales
        total_products = mongo.db.product.count_documents({})
        total_users = mongo.db.users.count_documents({})
        total_orders = mongo.db.purchases.count_documents({})
        
        # Produits récents
        recent_products = list(mongo.db.product.find({}).sort('created_at', -1).limit(5))
        
        # Utilisateurs récents
        recent_users = list(mongo.db.users.find({}).sort('created_at', -1).limit(5))
        
        # Commandes récentes
        recent_orders = list(mongo.db.purchases.find({}).sort('created_at', -1).limit(5))
        
        return render_template('admin/dashboard.html',
                             total_products=total_products,
                             total_users=total_users,
                             total_orders=total_orders,
                             recent_products=recent_products,
                             recent_users=recent_users,
                             recent_orders=recent_orders)
        
    except Exception as e:
        logger.error(f"Erreur dashboard admin: {e}")
        flash('Erreur lors du chargement du dashboard', 'error')
        return redirect(url_for('index'))

@app.route('/admin/products')
def admin_products():
    """Gestion des produits."""
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('Accès refusé. Droits administrateur requis.', 'error')
        return redirect(url_for('index'))
    
    try:
        products = list(mongo.db.product.find({}).sort('created_at', -1))
        for product in products:
            product['id'] = str(product['_id'])
        
        return render_template('admin/products.html', products=products)
        
    except Exception as e:
        logger.error(f"Erreur gestion produits: {e}")
        flash('Erreur lors du chargement des produits', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/products/add', methods=['GET', 'POST'])
def admin_add_product():
    """Ajouter un produit."""
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('Accès refusé. Droits administrateur requis.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            product_data = {
                'name': request.form['name'],
                'description': request.form['description'],
                'price': float(request.form['price']),
                'category': request.form['category'],
                'image_url': request.form.get('image_url', '/static/images/placeholder.svg'),
                'stock_quantity': int(request.form['stock_quantity']),
                'created_at': datetime.utcnow(),
                'is_active': request.form.get('is_active') == 'on'
            }
            
            mongo.db.product.insert_one(product_data)
            flash('Produit ajouté avec succès !', 'success')
            return redirect(url_for('admin_products'))
            
        except Exception as e:
            logger.error(f"Erreur ajout produit: {e}")
            flash('Erreur lors de l\'ajout du produit', 'error')
    
    return render_template('admin/add_product.html')

@app.route('/admin/products/edit/<product_id>', methods=['GET', 'POST'])
def admin_edit_product(product_id):
    """Modifier un produit."""
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('Accès refusé. Droits administrateur requis.', 'error')
        return redirect(url_for('index'))
    
    try:
        product = mongo.db.product.find_one({'_id': ObjectId(product_id)})
        if not product:
            flash('Produit non trouvé', 'error')
            return redirect(url_for('admin_products'))
        
        if request.method == 'POST':
            update_data = {
                'name': request.form['name'],
                'description': request.form['description'],
                'price': float(request.form['price']),
                'category': request.form['category'],
                'image_url': request.form.get('image_url', '/static/images/placeholder.svg'),
                'stock_quantity': int(request.form['stock_quantity']),
                'is_active': request.form.get('is_active') == 'on'
            }
            
            mongo.db.product.update_one(
                {'_id': ObjectId(product_id)},
                {'$set': update_data}
            )
            flash('Produit modifié avec succès !', 'success')
            return redirect(url_for('admin_products'))
        
        product['id'] = str(product['_id'])
        return render_template('admin/edit_product.html', product=product)
        
    except Exception as e:
        logger.error(f"Erreur modification produit: {e}")
        flash('Erreur lors de la modification du produit', 'error')
        return redirect(url_for('admin_products'))

@app.route('/admin/products/delete/<product_id>')
def admin_delete_product(product_id):
    """Supprimer un produit."""
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('Accès refusé. Droits administrateur requis.', 'error')
        return redirect(url_for('index'))
    
    try:
        mongo.db.product.delete_one({'_id': ObjectId(product_id)})
        flash('Produit supprimé avec succès !', 'success')
    except Exception as e:
        logger.error(f"Erreur suppression produit: {e}")
        flash('Erreur lors de la suppression du produit', 'error')
    
    return redirect(url_for('admin_products'))

if __name__ == '__main__':
    print("="*60)
    print("E-COMMERCE IA - VERSION FINALE PROPRE")
    print("="*60)
    print("Application accessible sur: http://localhost:5000")
    print("Comptes de test:")
    print("  - admin / admin123 (administrateur)")
    print("  - test / test123 (utilisateur)")
    print("="*60)
    
    # Création des données d'exemple
    create_sample_data()
    
    # Démarrage de l'application
    app.run(debug=True, host='0.0.0.0', port=5000)
