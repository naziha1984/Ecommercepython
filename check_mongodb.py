"""
Script pour vérifier et initialiser la base MongoDB.
"""

from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "ecommerce-python"

def check_and_init_mongodb():
    """Vérifie et initialise la base MongoDB."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        # Vérifier les collections
        users_count = db.users.count_documents({})
        products_count = db.products.count_documents({})
        purchases_count = db.purchases.count_documents({})
        
        print(f"Utilisateurs dans la base: {users_count}")
        print(f"Produits dans la base: {products_count}")
        print(f"Achats dans la base: {purchases_count}")
        
        if products_count == 0:
            print("Aucun produit trouvé. Ajout des produits d'exemple...")
            
            # Ajouter des produits d'exemple
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
                    'description': 'Smartphone Samsung avec écran Dynamic AMOLED 6,2 pouces, processeur Snapdragon 8 Gen 3',
                    'price': 999.99,
                    'category': 'Électronique',
                    'image_url': '/static/images/galaxys24.jpg',
                    'stock_quantity': 45,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Dell XPS 13',
                    'description': 'Ordinateur portable Dell avec processeur Intel Core i7, écran 13,4 pouces, 16 Go RAM',
                    'price': 1299.99,
                    'category': 'Informatique',
                    'image_url': '/static/images/dellxps13.jpg',
                    'stock_quantity': 25,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Sony WH-1000XM5',
                    'description': 'Casque sans fil Sony avec réduction de bruit active, autonomie 30h',
                    'price': 399.99,
                    'category': 'Audio',
                    'image_url': '/static/images/sonywh1000xm5.jpg',
                    'stock_quantity': 80,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Samsung Galaxy Tab S9',
                    'description': 'Tablette Samsung avec écran 11 pouces, processeur Snapdragon 8 Gen 2, 128 Go',
                    'price': 799.99,
                    'category': 'Tablettes',
                    'image_url': '/static/images/galaxytabs9.jpg',
                    'stock_quantity': 35,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Garmin Fenix 7',
                    'description': 'Montre GPS Garmin avec écran solaire, suivi multisport, autonomie 18 jours',
                    'price': 699.99,
                    'category': 'Montres connectées',
                    'image_url': '/static/images/garminfenix7.jpg',
                    'stock_quantity': 20,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'Nintendo Switch OLED',
                    'description': 'Console de jeu portable Nintendo avec écran OLED 7 pouces, 64 Go de stockage',
                    'price': 349.99,
                    'category': 'Gaming',
                    'image_url': '/static/images/nintendoswitch.jpg',
                    'stock_quantity': 70,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                },
                {
                    'name': 'PlayStation 5',
                    'description': 'Console de jeu Sony PlayStation 5 avec lecteur Blu-ray Ultra HD, 825 Go SSD',
                    'price': 499.99,
                    'category': 'Gaming',
                    'image_url': '/static/images/playstation5.jpg',
                    'stock_quantity': 15,
                    'created_at': datetime.utcnow(),
                    'is_active': True
                }
            ]
            
            db.products.insert_many(products_data)
            print(f"Ajout de {len(products_data)} produits dans la base de données")
        
        if users_count == 0:
            print("Aucun utilisateur trouvé. Ajout des utilisateurs d'exemple...")
            
            # Ajouter des utilisateurs d'exemple
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
            
            db.users.insert_many(users_data)
            print(f"Ajout de {len(users_data)} utilisateurs dans la base de données")
        
        print("Base de données MongoDB initialisée avec succès!")
        
        client.close()
        
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == '__main__':
    check_and_init_mongodb()
