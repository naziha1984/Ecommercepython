"""
Modèles de base de données pour l'application e-commerce.

Ce module contient tous les modèles SQLAlchemy pour la gestion des données :
- User: Utilisateurs du système
- Product: Produits disponibles
- Purchase: Historique des achats
- Cart: Panier d'achat temporaire

Auteur: Développeur Senior Python Full Stack
Date: 2024
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Cette variable sera importée depuis app.py
db = None

def init_db(database):
    """
    Initialise la variable db avec l'instance SQLAlchemy.
    
    Args:
        database: Instance SQLAlchemy de l'application Flask
    """
    global db
    db = database

class User(db.Model):
    """
    Modèle utilisateur pour l'authentification et la gestion des comptes.
    
    Attributs:
        id (int): Identifiant unique de l'utilisateur
        username (str): Nom d'utilisateur unique
        email (str): Adresse email unique
        password_hash (str): Hash du mot de passe
        created_at (datetime): Date de création du compte
        is_admin (bool): Statut administrateur
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relations
    purchases = db.relationship('Purchase', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    cart_items = db.relationship('Cart', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, username, email, password_hash, is_admin=False):
        """
        Constructeur du modèle User.
        
        Args:
            username (str): Nom d'utilisateur
            email (str): Adresse email
            password_hash (str): Hash du mot de passe
            is_admin (bool): Statut administrateur
        """
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin
    
    def set_password(self, password):
        """
        Définit le mot de passe de l'utilisateur.
        
        Args:
            password (str): Mot de passe en clair
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Vérifie le mot de passe de l'utilisateur.
        
        Args:
            password (str): Mot de passe à vérifier
            
        Returns:
            bool: True si le mot de passe est correct
        """
        return check_password_hash(self.password_hash, password)
    
    def get_total_purchases(self):
        """
        Calcule le nombre total d'achats de l'utilisateur.
        
        Returns:
            int: Nombre total d'achats
        """
        return self.purchases.count()
    
    def get_total_spent(self):
        """
        Calcule le montant total dépensé par l'utilisateur.
        
        Returns:
            float: Montant total dépensé
        """
        return sum(purchase.price * purchase.quantity for purchase in self.purchases)
    
    def __repr__(self):
        """
        Représentation string de l'utilisateur.
        
        Returns:
            str: Représentation de l'utilisateur
        """
        return f'<User {self.username}>'

class Product(db.Model):
    """
    Modèle produit pour le catalogue e-commerce.
    
    Attributs:
        id (int): Identifiant unique du produit
        name (str): Nom du produit
        description (str): Description détaillée
        price (float): Prix du produit
        category (str): Catégorie du produit
        image_url (str): URL de l'image du produit
        stock_quantity (int): Quantité en stock
        created_at (datetime): Date de création
        is_active (bool): Statut actif du produit
    """
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False, index=True)
    image_url = db.Column(db.String(500), nullable=True)
    stock_quantity = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relations
    purchases = db.relationship('Purchase', backref='product', lazy='dynamic')
    cart_items = db.relationship('Cart', backref='product', lazy='dynamic')
    
    def __init__(self, name, description, price, category, image_url=None, stock_quantity=0):
        """
        Constructeur du modèle Product.
        
        Args:
            name (str): Nom du produit
            description (str): Description du produit
            price (float): Prix du produit
            category (str): Catégorie du produit
            image_url (str): URL de l'image
            stock_quantity (int): Quantité en stock
        """
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.image_url = image_url
        self.stock_quantity = stock_quantity
    
    def is_available(self):
        """
        Vérifie si le produit est disponible en stock.
        
        Returns:
            bool: True si le produit est disponible
        """
        return self.stock_quantity > 0 and self.is_active
    
    def reduce_stock(self, quantity):
        """
        Réduit le stock du produit.
        
        Args:
            quantity (int): Quantité à soustraire
            
        Returns:
            bool: True si la réduction a réussi
        """
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            return True
        return False
    
    def get_total_sold(self):
        """
        Calcule le nombre total d'unités vendues.
        
        Returns:
            int: Nombre total d'unités vendues
        """
        return sum(purchase.quantity for purchase in self.purchases)
    
    def get_total_revenue(self):
        """
        Calcule le chiffre d'affaires généré par ce produit.
        
        Returns:
            float: Chiffre d'affaires total
        """
        return sum(purchase.price * purchase.quantity for purchase in self.purchases)
    
    def __repr__(self):
        """
        Représentation string du produit.
        
        Returns:
            str: Représentation du produit
        """
        return f'<Product {self.name}>'

class Purchase(db.Model):
    """
    Modèle achat pour l'historique des commandes.
    
    Attributs:
        id (int): Identifiant unique de l'achat
        user_id (int): ID de l'utilisateur
        product_id (int): ID du produit
        quantity (int): Quantité achetée
        price (float): Prix unitaire au moment de l'achat
        purchase_date (datetime): Date de l'achat
    """
    __tablename__ = 'purchases'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __init__(self, user_id, product_id, quantity, price):
        """
        Constructeur du modèle Purchase.
        
        Args:
            user_id (int): ID de l'utilisateur
            product_id (int): ID du produit
            quantity (int): Quantité achetée
            price (float): Prix unitaire
        """
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
    
    def get_total_price(self):
        """
        Calcule le prix total de cet achat.
        
        Returns:
            float: Prix total (prix unitaire × quantité)
        """
        return self.price * self.quantity
    
    def __repr__(self):
        """
        Représentation string de l'achat.
        
        Returns:
            str: Représentation de l'achat
        """
        return f'<Purchase User:{self.user_id} Product:{self.product_id} Qty:{self.quantity}>'

class Cart(db.Model):
    """
    Modèle panier pour la gestion temporaire des articles.
    
    Attributs:
        id (int): Identifiant unique de l'article du panier
        user_id (int): ID de l'utilisateur
        product_id (int): ID du produit
        quantity (int): Quantité dans le panier
        added_at (datetime): Date d'ajout au panier
    """
    __tablename__ = 'cart'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __init__(self, user_id, product_id, quantity=1):
        """
        Constructeur du modèle Cart.
        
        Args:
            user_id (int): ID de l'utilisateur
            product_id (int): ID du produit
            quantity (int): Quantité à ajouter
        """
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
    
    def get_total_price(self):
        """
        Calcule le prix total de cet article du panier.
        
        Returns:
            float: Prix total (prix du produit × quantité)
        """
        return self.product.price * self.quantity
    
    def __repr__(self):
        """
        Représentation string de l'article du panier.
        
        Returns:
            str: Représentation de l'article
        """
        return f'<Cart User:{self.user_id} Product:{self.product_id} Qty:{self.quantity}>'

