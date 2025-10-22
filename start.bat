@echo off
echo ========================================
echo    E-COMMERCE IA - DEMARRAGE RAPIDE
echo ========================================
echo.

echo Installation des dependances...
pip install -r requirements.txt

echo.
echo Initialisation de la base de donnees...
python database/db_init.py

echo.
echo Entrainement du modele de recommandation...
python recommender/train_model.py

echo.
echo Demarrage de l'application...
echo L'application sera accessible sur: http://localhost:5000
echo.
echo Comptes de test disponibles:
echo - admin / admin123 (administrateur)
echo - john_doe / password123
echo - jane_smith / password123
echo - mike_wilson / password123
echo - sarah_jones / password123
echo - alex_brown / password123
echo.

python app.py

pause
