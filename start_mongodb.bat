@echo off
echo ========================================
echo    E-COMMERCE IA - MONGODB VERSION
echo ========================================
echo.

echo Initialisation de la base de donnees MongoDB...
python init_mongodb.py

echo.
echo Demarrage de l'application avec MongoDB...
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

python app_mongodb.py

pause
