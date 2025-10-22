"""
Script d'initialisation pour MongoDB.

Ce script initialise votre base de données MongoDB avec les collections
et les données d'exemple pour l'application E-Commerce IA.

Base de données: ecommerce-python
Collections: users, products, purchases, cart

Auteur: Développeur Senior Python Full Stack
Date: 2024
"""

import logging
from datetime import datetime
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_mongodb():
    """
    Initialise la base de données MongoDB avec les collections et données d'exemple.
    """
    try:
        # Connexion à MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['ecommerce-python']
        
        logger.info("Connexion à MongoDB établie")
        
        # Collections
        users_collection = db['users']
        products_collection = db['products']
        purchases_collection = db['purchases']
        cart_collection = db['cart']
        
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
            {
                'username': 'mike_wilson',
                'email': 'mike.wilson@email.com',
                'password_hash': generate_password_hash('password123'),
                'created_at': datetime.utcnow(),
                'is_admin': False
            },
            {
                'username': 'sarah_jones',
                'email': 'sarah.jones@email.com',
                'password_hash': generate_password_hash('password123'),
                'created_at': datetime.utcnow(),
                'is_admin': False
            },
            {
                'username': 'alex_brown',
                'email': 'alex.brown@email.com',
                'password_hash': generate_password_hash('password123'),
                'created_at': datetime.utcnow(),
                'is_admin': False
            }
        ]
        
        users_collection.insert_many(users_data)
        logger.info(f"Création de {len(users_data)} utilisateurs d'exemple")
        
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
            {
                'name': 'Samsung Galaxy S24',
                'description': 'Smartphone Samsung avec écran Dynamic AMOLED 6,2 pouces, triple caméra 50MP, 128 Go',
                'price': 899.99,
                'category': 'Électronique',
                'image_url': '/static/images/galaxys24.jpg',
                'stock_quantity': 35,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'Sony WH-1000XM5',
                'description': 'Casque audio sans fil avec réduction de bruit, autonomie 30h, charge rapide',
                'price': 399.99,
                'category': 'Audio',
                'image_url': '/static/images/sonywh1000xm5.jpg',
                'stock_quantity': 25,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'Dell XPS 13',
                'description': 'Ordinateur portable Dell avec processeur Intel i7, écran 13,4 pouces 4K, 16 Go RAM',
                'price': 1499.99,
                'category': 'Informatique',
                'image_url': '/static/images/dellxps13.jpg',
                'stock_quantity': 20,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'Nintendo Switch OLED',
                'description': 'Console de jeu portable Nintendo avec écran OLED 7 pouces, manettes Joy-Con',
                'price': 349.99,
                'category': 'Gaming',
                'image_url': '/static/images/switcholed.jpg',
                'stock_quantity': 45,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'PlayStation 5',
                'description': 'Console de jeu Sony PlayStation 5 avec lecteur Blu-ray Ultra HD, manette DualSense',
                'price': 499.99,
                'category': 'Gaming',
                'image_url': '/static/images/ps5.jpg',
                'stock_quantity': 15,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'Canon EOS R6',
                'description': 'Appareil photo hybride Canon avec capteur plein format 20MP, stabilisation 5 axes',
                'price': 2499.99,
                'category': 'Photo',
                'image_url': '/static/images/canoneosr6.jpg',
                'stock_quantity': 10,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'DJI Mini 3 Pro',
                'description': 'Drone DJI avec caméra 4K, stabilisation 3 axes, autonomie 47 minutes',
                'price': 759.99,
                'category': 'Drones',
                'image_url': '/static/images/djimini3pro.jpg',
                'stock_quantity': 8,
                'created_at': datetime.utcnow(),
                'is_active': True
            }
        ]
        
        products_collection.insert_many(products_data)
        logger.info(f"Création de {len(products_data)} produits d'exemple")
        
        # Création de quelques achats d'exemple pour les tests
        # Récupération des IDs des utilisateurs et produits
        users = list(users_collection.find())
        products = list(products_collection.find())
        
        if users and products:
            # Création d'achats d'exemple pour quelques utilisateurs
            sample_purchases = []
            for user in users[1:4]:  # Utilisateurs non-admin
                for i in range(2, 5):  # 2-3 achats par utilisateur
                    if i < len(products):
                        purchase = {
                            'user_id': user['_id'],
                            'product_id': products[i]['_id'],
                            'quantity': 1,
                            'price': products[i]['price'],
                            'purchase_date': datetime.utcnow()
                        }
                        sample_purchases.append(purchase)
            
            if sample_purchases:
                purchases_collection.insert_many(sample_purchases)
                logger.info(f"Création de {len(sample_purchases)} achats d'exemple")
        
        # Affichage des statistiques
        logger.info("Statistiques de la base de données MongoDB:")
        logger.info(f"- Utilisateurs: {users_collection.count_documents({})}")
        logger.info(f"- Produits: {products_collection.count_documents({})}")
        logger.info(f"- Achats: {purchases_collection.count_documents({})}")
        logger.info(f"- Panier: {cart_collection.count_documents({})}")
        
        logger.info("Initialisation de la base de données MongoDB terminée avec succès")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de MongoDB: {e}")
        raise

if __name__ == '__main__':
    """
    Point d'entrée du script d'initialisation.
    """
    try:
        logger.info("="*60)
        logger.info("INITIALISATION DE LA BASE DE DONNÉES MONGODB")
        logger.info("="*60)
        
        init_mongodb()
        
        print("\n" + "="*60)
        print("✅ INITIALISATION MONGODB TERMINÉE")
        print("="*60)
        print("🗄️ Base de données: ecommerce-python")
        print("📊 Collections créées:")
        print("   - users (utilisateurs)")
        print("   - products (produits)")
        print("   - purchases (achats)")
        print("   - cart (panier)")
        print("\n👤 Comptes de test disponibles:")
        print("   - admin / admin123 (administrateur)")
        print("   - john_doe / password123")
        print("   - jane_smith / password123")
        print("   - mike_wilson / password123")
        print("   - sarah_jones / password123")
        print("   - alex_brown / password123")
        print("\n🚀 Vous pouvez maintenant lancer l'application avec:")
        print("   python app_mongodb.py")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution: {e}")
        print(f"\n❌ Erreur: {e}")
        print("Vérifiez que MongoDB est démarré sur localhost:27017")
