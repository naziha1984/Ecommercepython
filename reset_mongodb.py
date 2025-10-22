"""
Script pour réinitialiser complètement la base MongoDB.
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

def reset_mongodb():
    """Réinitialise complètement la base MongoDB."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        print("Connexion a MongoDB etablie")
        
        # Supprimer toutes les collections existantes
        print("Suppression des collections existantes...")
        db.product.drop()
        db.products.drop()
        db.users.drop()
        db.purchases.drop()
        db.cart.drop()
        
        print("Collections supprimees")
        
        # Ajouter des utilisateurs
        print("Ajout des utilisateurs...")
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
        print(f"Ajout de {len(users_data)} utilisateurs")
        
        # Ajouter des produits
        print("Ajout des produits...")
        products_data = [
            {
                'name': 'iPhone 15 Pro',
                'description': 'Smartphone Apple avec ecran Super Retina XDR de 6,1 pouces, processeur A17 Pro, triple camera 48MP',
                'price': 1199.99,
                'category': 'Electronique',
                'image_url': '/static/images/iphone15pro.jpg',
                'stock_quantity': 50,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'MacBook Air M2',
                'description': 'Ordinateur portable Apple avec puce M2, ecran Liquid Retina 13,6 pouces, 8 Go RAM, 256 Go SSD',
                'price': 1299.99,
                'category': 'Informatique',
                'image_url': '/static/images/macbookair.jpg',
                'stock_quantity': 30,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'AirPods Pro 2',
                'description': 'Ecouteurs sans fil Apple avec reduction de bruit active, boitier de charge MagSafe',
                'price': 279.99,
                'category': 'Audio',
                'image_url': '/static/images/airpodspro.jpg',
                'stock_quantity': 100,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'iPad Air 5',
                'description': 'Tablette Apple avec puce M1, ecran Liquid Retina 10,9 pouces, 64 Go de stockage',
                'price': 599.99,
                'category': 'Tablettes',
                'image_url': '/static/images/ipadair.jpg',
                'stock_quantity': 40,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'Apple Watch Series 9',
                'description': 'Montre connectee Apple avec ecran Always-On, GPS, suivi de sante avance',
                'price': 429.99,
                'category': 'Montres connectees',
                'image_url': '/static/images/applewatch.jpg',
                'stock_quantity': 60,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'Samsung Galaxy S24',
                'description': 'Smartphone Samsung avec ecran Dynamic AMOLED 6,2 pouces, processeur Snapdragon 8 Gen 3',
                'price': 999.99,
                'category': 'Electronique',
                'image_url': '/static/images/galaxys24.jpg',
                'stock_quantity': 45,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'Dell XPS 13',
                'description': 'Ordinateur portable Dell avec processeur Intel Core i7, ecran 13,4 pouces, 16 Go RAM',
                'price': 1299.99,
                'category': 'Informatique',
                'image_url': '/static/images/dellxps13.jpg',
                'stock_quantity': 25,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'Sony WH-1000XM5',
                'description': 'Casque sans fil Sony avec reduction de bruit active, autonomie 30h',
                'price': 399.99,
                'category': 'Audio',
                'image_url': '/static/images/sonywh1000xm5.jpg',
                'stock_quantity': 80,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'Samsung Galaxy Tab S9',
                'description': 'Tablette Samsung avec ecran 11 pouces, processeur Snapdragon 8 Gen 2, 128 Go',
                'price': 799.99,
                'category': 'Tablettes',
                'image_url': '/static/images/galaxytabs9.jpg',
                'stock_quantity': 35,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'Garmin Fenix 7',
                'description': 'Montre GPS Garmin avec ecran solaire, suivi multisport, autonomie 18 jours',
                'price': 699.99,
                'category': 'Montres connectees',
                'image_url': '/static/images/garminfenix7.jpg',
                'stock_quantity': 20,
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                'name': 'Nintendo Switch OLED',
                'description': 'Console de jeu portable Nintendo avec ecran OLED 7 pouces, 64 Go de stockage',
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
        
        db.product.insert_many(products_data)
        print(f"Ajout de {len(products_data)} produits")
        
        # Vérifier les données
        users_count = db.users.count_documents({})
        products_count = db.product.count_documents({})
        
        print(f"Utilisateurs dans la base: {users_count}")
        print(f"Produits dans la base: {products_count}")
        
        client.close()
        print("Base de donnees MongoDB reinitialisee avec succes!")
        
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == '__main__':
    reset_mongodb()
