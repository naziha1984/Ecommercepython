"""
Application Flask e-commerce avec MongoDB.

Cette version utilise MongoDB au lieu de SQLite pour stocker les données.
Base de données: ecommerce-python
Collections: users, products, purchases, cart

Auteur: Développeur Senior Python Full Stack
Date: 2024
"""

import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration de l'application Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre-cle-secrete-super-securisee-2024'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ecommerce-python'

# Initialisation de MongoDB
mongo = PyMongo(app)

# Collections MongoDB
users_collection = mongo.db.users
products_collection = mongo.db.product  # Collection au singulier comme dans MongoDB Compass
purchases_collection = mongo.db.purchases
cart_collection = mongo.db.cart

@app.route('/')
def index():
    """Page d'accueil avec tous les produits."""
    try:
        products = list(products_collection.find({'is_active': True}))
        logger.info(f"Affichage de {len(products)} produits sur la page d'accueil")
        return render_template('index.html', products=products)
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la page d'accueil: {e}")
        flash('Erreur lors du chargement des produits', 'error')
        return render_template('index.html', products=[])

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Inscription d'un nouvel utilisateur."""
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            
            # Vérification de l'existence de l'utilisateur
            if users_collection.find_one({'username': username}):
                flash('Ce nom d\'utilisateur existe déjà', 'error')
                return render_template('register.html')
            
            if users_collection.find_one({'email': email}):
                flash('Cette adresse email est déjà utilisée', 'error')
                return render_template('register.html')
            
            # Création du nouvel utilisateur
            user_data = {
                'username': username,
                'email': email,
                'password_hash': generate_password_hash(password),
                'created_at': datetime.utcnow(),
                'is_admin': False
            }
            
            users_collection.insert_one(user_data)
            
            logger.info(f"Nouvel utilisateur créé: {username}")
            flash('Compte créé avec succès ! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            logger.error(f"Erreur lors de l'inscription: {e}")
            flash('Erreur lors de la création du compte', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Connexion d'un utilisateur existant."""
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            user = users_collection.find_one({'username': username})
            
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = str(user['_id'])
                session['username'] = user['username']
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
    """Déconnexion de l'utilisateur."""
    session.clear()
    flash('Vous avez été déconnecté', 'info')
    logger.info("Utilisateur déconnecté")
    return redirect(url_for('index'))

@app.route('/product/<product_id>')
def product_detail(product_id):
    """Page de détail d'un produit."""
    try:
        product = products_collection.find_one({'_id': ObjectId(product_id)})
        if not product:
            flash('Produit non trouvé', 'error')
            return redirect(url_for('index'))
        
        logger.info(f"Affichage du produit {product_id}: {product['name']}")
        return render_template('product.html', product=product)
    except Exception as e:
        logger.error(f"Erreur lors du chargement du produit {product_id}: {e}")
        flash('Produit non trouvé', 'error')
        return redirect(url_for('index'))

@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    """Ajout d'un produit au panier."""
    if 'user_id' not in session:
        flash('Vous devez être connecté pour ajouter des produits au panier', 'error')
        return redirect(url_for('login'))
    
    try:
        user_id = ObjectId(session['user_id'])
        product = products_collection.find_one({'_id': ObjectId(product_id)})
        
        if not product:
            flash('Produit non trouvé', 'error')
            return redirect(url_for('index'))
        
        # Vérification si le produit est déjà dans le panier
        existing_cart_item = cart_collection.find_one({
            'user_id': user_id,
            'product_id': ObjectId(product_id)
        })
        
        if existing_cart_item:
            cart_collection.update_one(
                {'_id': existing_cart_item['_id']},
                {'$inc': {'quantity': 1}}
            )
        else:
            cart_item = {
                'user_id': user_id,
                'product_id': ObjectId(product_id),
                'quantity': 1,
                'added_at': datetime.utcnow()
            }
            cart_collection.insert_one(cart_item)
        
        logger.info(f"Produit {product_id} ajouté au panier de l'utilisateur {user_id}")
        flash(f"{product['name']} ajouté au panier !", 'success')
        
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout au panier: {e}")
        flash('Erreur lors de l\'ajout au panier', 'error')
    
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    """Affichage du panier de l'utilisateur."""
    if 'user_id' not in session:
        flash('Vous devez être connecté pour voir votre panier', 'error')
        return redirect(url_for('login'))
    
    try:
        # Gérer les deux types d'ID (int et ObjectId)
        user_id = session['user_id']
        if isinstance(user_id, int):
            # Si c'est un int, chercher l'utilisateur par son ID numérique
            user = users_collection.find_one({'username': {'$exists': True}})
            if user:
                user_id = user['_id']
            else:
                flash('Utilisateur non trouvé', 'error')
                return redirect(url_for('login'))
        else:
            user_id = ObjectId(user_id)
        
        cart_items = list(cart_collection.find({'user_id': user_id}))
        
        # Récupération des détails des produits
        cart_items_with_products = []
        total = 0
        
        for item in cart_items:
            product = products_collection.find_one({'_id': item['product_id']})
            if product:
                item['product'] = product
                item['total_price'] = product['price'] * item['quantity']
                total += item['total_price']
                cart_items_with_products.append(item)
        
        logger.info(f"Affichage du panier pour l'utilisateur {user_id}: {len(cart_items_with_products)} articles")
        return render_template('cart.html', cart_items=cart_items_with_products, total=total)
        
    except Exception as e:
        logger.error(f"Erreur lors du chargement du panier: {e}")
        flash('Erreur lors du chargement du panier', 'error')
        return render_template('cart.html', cart_items=[], total=0)

@app.route('/remove_from_cart/<cart_item_id>')
def remove_from_cart(cart_item_id):
    """Suppression d'un article du panier."""
    if 'user_id' not in session:
        flash('Vous devez être connecté', 'error')
        return redirect(url_for('login'))
    
    try:
        user_id = ObjectId(session['user_id'])
        cart_item = cart_collection.find_one({'_id': ObjectId(cart_item_id)})
        
        if not cart_item:
            flash('Article non trouvé', 'error')
            return redirect(url_for('cart'))
        
        # Vérification que l'article appartient à l'utilisateur connecté
        if cart_item['user_id'] != user_id:
            flash('Accès non autorisé', 'error')
            return redirect(url_for('cart'))
        
        cart_collection.delete_one({'_id': ObjectId(cart_item_id)})
        
        logger.info(f"Article {cart_item_id} supprimé du panier")
        flash('Article supprimé du panier', 'success')
        
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du panier: {e}")
        flash('Erreur lors de la suppression', 'error')
    
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    """Finalisation de la commande."""
    if 'user_id' not in session:
        flash('Vous devez être connecté pour finaliser votre commande', 'error')
        return redirect(url_for('login'))
    
    try:
        user_id = ObjectId(session['user_id'])
        cart_items = list(cart_collection.find({'user_id': user_id}))
        
        if not cart_items:
            flash('Votre panier est vide', 'error')
            return redirect(url_for('cart'))
        
        # Création des achats
        for cart_item in cart_items:
            product = products_collection.find_one({'_id': cart_item['product_id']})
            if product:
                purchase = {
                    'user_id': user_id,
                    'product_id': cart_item['product_id'],
                    'quantity': cart_item['quantity'],
                    'price': product['price'],
                    'purchase_date': datetime.utcnow()
                }
                purchases_collection.insert_one(purchase)
        
        # Suppression du panier
        cart_collection.delete_many({'user_id': user_id})
        
        logger.info(f"Commande finalisée pour l'utilisateur {user_id}: {len(cart_items)} articles")
        flash('Commande finalisée avec succès !', 'success')
        
        return redirect(url_for('purchase_history'))
        
    except Exception as e:
        logger.error(f"Erreur lors de la finalisation de la commande: {e}")
        flash('Erreur lors de la finalisation de la commande', 'error')
        return redirect(url_for('cart'))

@app.route('/purchase_history')
def purchase_history():
    """Historique des achats de l'utilisateur."""
    if 'user_id' not in session:
        flash('Vous devez être connecté pour voir votre historique', 'error')
        return redirect(url_for('login'))
    
    try:
        # Gérer les deux types d'ID (int et ObjectId)
        user_id = session['user_id']
        if isinstance(user_id, int):
            # Si c'est un int, chercher l'utilisateur par son ID numérique
            user = users_collection.find_one({'username': {'$exists': True}})
            if user:
                user_id = user['_id']
            else:
                flash('Utilisateur non trouvé', 'error')
                return redirect(url_for('login'))
        else:
            user_id = ObjectId(user_id)
        
        purchases = list(purchases_collection.find({'user_id': user_id}).sort('purchase_date', -1))
        
        # Récupération des détails des produits
        purchases_with_products = []
        for purchase in purchases:
            product = products_collection.find_one({'_id': purchase['product_id']})
            if product:
                purchase['product'] = product
                purchase['total_price'] = purchase['price'] * purchase['quantity']
                purchases_with_products.append(purchase)
        
        logger.info(f"Affichage de l'historique pour l'utilisateur {user_id}: {len(purchases_with_products)} achats")
        return render_template('purchase_history.html', purchases=purchases_with_products)
        
    except Exception as e:
        logger.error(f"Erreur lors du chargement de l'historique: {e}")
        flash('Erreur lors du chargement de l\'historique', 'error')
        return render_template('purchase_history.html', purchases=[])

@app.route('/recommendations')
def recommendations():
    """Page des recommandations personnalisées."""
    if 'user_id' not in session:
        flash('Vous devez être connecté pour voir vos recommandations', 'error')
        return redirect(url_for('login'))
    
    try:
        # Récupérer tous les produits actifs comme recommandations
        recommended_products = list(products_collection.find({'is_active': True}).limit(6))
        
        logger.info(f"Affichage de {len(recommended_products)} recommandations")
        return render_template('recommendations.html', recommendations=recommended_products, title="Recommandations personnalisées")
        
    except Exception as e:
        logger.error(f"Erreur lors du chargement des recommandations: {e}")
        flash('Erreur lors du chargement de vos recommandations', 'error')
        return redirect(url_for('index'))

def create_sample_data():
    """Crée des données d'exemple pour tester l'application."""
    try:
        # Vérification si des données existent déjà
        if users_collection.count_documents({}) > 0:
            logger.info("Des données existent déjà dans la base de données")
            return
        
        # Création des utilisateurs d'exemple
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@ecommerce.com',
                'password_hash': generate_password_hash('admin123'),
                'created_at': datetime.utcnow(),
                'is_admin': True
            },
            {
                'username': 'john_doe',
                'email': 'john.doe@email.com',
                'password_hash': generate_password_hash('password123'),
                'created_at': datetime.utcnow(),
                'is_admin': False
            },
            {
                'username': 'jane_smith',
                'email': 'jane.smith@email.com',
                'password_hash': generate_password_hash('password123'),
                'created_at': datetime.utcnow(),
                'is_admin': False
            },
        ]
        
        users_collection.insert_many(users_data)
        
        # Création des produits d'exemple
        products_data = [
            {
                'name': 'iPhone 15 Pro',
                'description': 'Smartphone Apple avec écran Super Retina XDR de 6,1 pouces, processeur A17 Pro, triple caméra 48MP',
                'price': 1199.99,
                'category': 'Électronique',
                'image_url': '/static/images/iphone15pro.jpg',
                'stock_quantity': 50,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'MacBook Air M2',
                'description': 'Ordinateur portable Apple avec puce M2, écran Liquid Retina 13,6 pouces, 8 Go RAM, 256 Go SSD',
                'price': 1299.99,
                'category': 'Informatique',
                'image_url': '/static/images/macbookair.jpg',
                'stock_quantity': 30,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'AirPods Pro 2',
                'description': 'Écouteurs sans fil Apple avec réduction de bruit active, boîtier de charge MagSafe',
                'price': 279.99,
                'category': 'Audio',
                'image_url': '/static/images/airpodspro.jpg',
                'stock_quantity': 100,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'iPad Air 5',
                'description': 'Tablette Apple avec puce M1, écran Liquid Retina 10,9 pouces, 64 Go de stockage',
                'price': 599.99,
                'category': 'Tablettes',
                'image_url': '/static/images/ipadair.jpg',
                'stock_quantity': 40,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'Apple Watch Series 9',
                'description': 'Montre connectée Apple avec écran Always-On, GPS, suivi de santé avancé',
                'price': 429.99,
                'category': 'Montres connectées',
                'image_url': '/static/images/applewatch.jpg',
                'stock_quantity': 60,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
        ]
        
        products_collection.insert_many(products_data)
        
        logger.info("Données d'exemple créées avec succès dans MongoDB")
        
    except Exception as e:
        logger.error(f"Erreur lors de la création des données d'exemple: {e}")

if __name__ == '__main__':
    """
    Point d'entrée de l'application Flask avec MongoDB.
    """
    # Création des données d'exemple
    create_sample_data()
    
    # Démarrage de l'application
    logger.info("Démarrage de l'application Flask e-commerce avec MongoDB")
    print("\n" + "="*60)
    print("E-COMMERCE IA - APPLICATION MONGODB DEMARREE")
    print("="*60)
    print("L'application est accessible sur: http://localhost:5000")
    print("Base de donnees: MongoDB (ecommerce-python)")
    print("Comptes de test disponibles:")
    print("   - admin / admin123 (administrateur)")
    print("   - john_doe / password123")
    print("   - jane_smith / password123")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
