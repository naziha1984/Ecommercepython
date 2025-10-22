"""
Application Flask e-commerce simplifiée pour test rapide.

Cette version simplifiée évite les erreurs d'import et permet de tester
les fonctionnalités de base rapidement.

Auteur: Développeur Senior Python Full Stack
Date: 2024
"""

import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

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

# Initialisation de la base de données
db = SQLAlchemy(app)

# Modèles de base de données simplifiés
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(500))
    stock_quantity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def is_available(self):
        return self.stock_quantity > 0 and self.is_active

class Purchase(db.Model):
    __tablename__ = 'purchases'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='purchases')
    product = db.relationship('Product', backref='purchases')

class Cart(db.Model):
    __tablename__ = 'cart'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='cart_items')
    product = db.relationship('Product', backref='cart_items')

@app.route('/')
def index():
    """Page d'accueil avec tous les produits."""
    try:
        products = Product.query.all()
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
            if User.query.filter_by(username=username).first():
                flash('Ce nom d\'utilisateur existe déjà', 'error')
                return render_template('register.html')
            
            if User.query.filter_by(email=email).first():
                flash('Cette adresse email est déjà utilisée', 'error')
                return render_template('register.html')
            
            # Création du nouvel utilisateur
            new_user = User(
                username=username,
                email=email
            )
            new_user.set_password(password)
            
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
    """Connexion d'un utilisateur existant."""
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
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
    """Déconnexion de l'utilisateur."""
    session.clear()
    flash('Vous avez été déconnecté', 'info')
    logger.info("Utilisateur déconnecté")
    return redirect(url_for('index'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Page de détail d'un produit."""
    try:
        product = Product.query.get_or_404(product_id)
        logger.info(f"Affichage du produit {product_id}: {product.name}")
        return render_template('product.html', product=product)
    except Exception as e:
        logger.error(f"Erreur lors du chargement du produit {product_id}: {e}")
        flash('Produit non trouvé', 'error')
        return redirect(url_for('index'))

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    """Ajout d'un produit au panier."""
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
                quantity=1
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
    """Affichage du panier de l'utilisateur."""
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
    """Suppression d'un article du panier."""
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
    """Finalisation de la commande."""
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
                price=cart_item.product.price
            )
            db.session.add(purchase)
        
        # Suppression du panier
        Cart.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        
        logger.info(f"Commande finalisée pour l'utilisateur {user_id}: {len(cart_items)} articles")
        flash('Commande finalisée avec succès !', 'success')
        
        return redirect(url_for('purchase_history'))
        
    except Exception as e:
        logger.error(f"Erreur lors de la finalisation de la commande: {e}")
        db.session.rollback()
        flash('Erreur lors de la finalisation de la commande', 'error')
        return redirect(url_for('cart'))

@app.route('/purchase_history')
def purchase_history():
    """Historique des achats de l'utilisateur."""
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

def create_sample_data():
    """Crée des données d'exemple pour tester l'application."""
    try:
        # Vérification si des données existent déjà
        if User.query.count() > 0:
            logger.info("Des données existent déjà dans la base de données")
            return
        
        # Création des utilisateurs d'exemple
        users_data = [
            {'username': 'admin', 'email': 'admin@ecommerce.com', 'password': 'admin123', 'is_admin': True},
            {'username': 'john_doe', 'email': 'john.doe@email.com', 'password': 'password123', 'is_admin': False},
            {'username': 'jane_smith', 'email': 'jane.smith@email.com', 'password': 'password123', 'is_admin': False},
        ]
        
        for user_data in users_data:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                is_admin=user_data['is_admin']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
        
        # Création des produits d'exemple
        products_data = [
            {'name': 'iPhone 15 Pro', 'description': 'Smartphone Apple avec écran Super Retina XDR', 'price': 1199.99, 'category': 'Électronique', 'stock_quantity': 50},
            {'name': 'MacBook Air M2', 'description': 'Ordinateur portable Apple avec puce M2', 'price': 1299.99, 'category': 'Informatique', 'stock_quantity': 30},
            {'name': 'AirPods Pro 2', 'description': 'Écouteurs sans fil Apple avec réduction de bruit', 'price': 279.99, 'category': 'Audio', 'stock_quantity': 100},
            {'name': 'iPad Air 5', 'description': 'Tablette Apple avec puce M1', 'price': 599.99, 'category': 'Tablettes', 'stock_quantity': 40},
            {'name': 'Apple Watch Series 9', 'description': 'Montre connectée Apple avec GPS', 'price': 429.99, 'category': 'Montres connectées', 'stock_quantity': 60},
        ]
        
        for product_data in products_data:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        logger.info("Données d'exemple créées avec succès")
        
    except Exception as e:
        logger.error(f"Erreur lors de la création des données d'exemple: {e}")
        db.session.rollback()

if __name__ == '__main__':
    """
    Point d'entrée de l'application Flask.
    """
    # Création des tables de base de données
    with app.app_context():
        db.create_all()
        logger.info("Tables de base de données créées")
        
        # Création des données d'exemple
        create_sample_data()
    
    # Démarrage de l'application
    logger.info("Démarrage de l'application Flask e-commerce")
    print("\n" + "="*60)
    print("🛍️ E-COMMERCE IA - APPLICATION DÉMARRÉE")
    print("="*60)
    print("🌐 L'application est accessible sur: http://localhost:5000")
    print("👤 Comptes de test disponibles:")
    print("   - admin / admin123 (administrateur)")
    print("   - john_doe / password123")
    print("   - jane_smith / password123")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
