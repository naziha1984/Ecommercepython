# Sprint Backlog - Sprint 1
**Durée**: 2 semaines  
**Objectif**: Infrastructure de base et modèles de données  
**Vélocité prévue**: 8 story points

## Vue d'ensemble du Sprint

### Objectifs du Sprint
- Mettre en place l'infrastructure Flask
- Créer les modèles de base de données
- Initialiser la base de données avec des données d'exemple
- Configurer le logging et la structure du projet

### Équipe
- **Scrum Master**: Développeur Senior
- **Product Owner**: Développeur Senior
- **Développeur**: Développeur Senior Python Full Stack

## User Stories du Sprint

### US-001: Configuration de l'environnement Flask
**Effort**: 3 story points  
**Statut**: À faire

#### Tâches détaillées
- [ ] Créer la structure de projet
- [ ] Installer Flask et dépendances
- [ ] Configurer SQLAlchemy
- [ ] Créer le fichier app.py principal
- [ ] Configurer le logging
- [ ] Tester l'application de base

#### Critères d'acceptation
- [ ] Application Flask démarre sans erreur
- [ ] Configuration SQLAlchemy fonctionnelle
- [ ] Logging configuré et fonctionnel
- [ ] Structure de projet respectée

#### Définition de fini
- [ ] Code testé et fonctionnel
- [ ] Documentation technique
- [ ] Respect des standards PEP8
- [ ] Tests unitaires de base

### US-002: Modèles de base de données
**Effort**: 5 story points  
**Statut**: À faire

#### Tâches détaillées
- [ ] Créer le modèle User
  - [ ] Champs: id, username, email, password_hash, created_at, is_admin
  - [ ] Méthodes: set_password, check_password
  - [ ] Relations avec Purchase et Cart
- [ ] Créer le modèle Product
  - [ ] Champs: id, name, description, price, category, image_url, stock_quantity, created_at, is_active
  - [ ] Méthodes: is_available, reduce_stock, get_total_sold
  - [ ] Relations avec Purchase et Cart
- [ ] Créer le modèle Purchase
  - [ ] Champs: id, user_id, product_id, quantity, price, purchase_date
  - [ ] Méthodes: get_total_price
  - [ ] Relations avec User et Product
- [ ] Créer le modèle Cart
  - [ ] Champs: id, user_id, product_id, quantity, added_at
  - [ ] Méthodes: get_total_price
  - [ ] Relations avec User et Product
- [ ] Créer le script d'initialisation
- [ ] Générer des données d'exemple

#### Critères d'acceptation
- [ ] Tous les modèles créés et fonctionnels
- [ ] Relations entre modèles définies
- [ ] Script d'initialisation opérationnel
- [ ] Données d'exemple générées
- [ ] Tests de création/lecture des données

#### Définition de fini
- [ ] Modèles testés individuellement
- [ ] Relations testées
- [ ] Données d'exemple réalistes
- [ ] Documentation des modèles

## Planification du Sprint

### Semaine 1
**Jour 1-2**: Configuration Flask
- Installation et configuration de l'environnement
- Création de la structure de projet
- Configuration SQLAlchemy et logging

**Jour 3-4**: Modèles de base
- Création du modèle User
- Création du modèle Product
- Tests des modèles de base

**Jour 5**: Modèles avancés
- Création du modèle Purchase
- Création du modèle Cart
- Définition des relations

### Semaine 2
**Jour 1-2**: Script d'initialisation
- Développement du script db_init.py
- Génération de données d'exemple
- Tests d'initialisation

**Jour 3-4**: Tests et documentation
- Tests unitaires complets
- Documentation technique
- Validation des critères d'acceptation

**Jour 5**: Revue de sprint
- Démonstration des fonctionnalités
- Rétrospective
- Planification du sprint suivant

## Tâches techniques détaillées

### Configuration Flask
```python
# Structure attendue
app.py
├── Configuration Flask
├── Initialisation SQLAlchemy
├── Configuration logging
└── Point d'entrée principal
```

### Modèles de données
```python
# Modèle User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relations
    purchases = db.relationship('Purchase', backref='user', lazy='dynamic')
    cart_items = db.relationship('Cart', backref='user', lazy='dynamic')
```

### Script d'initialisation
```python
# Fonctionnalités attendues
def init_database():
    # Création des tables
    # Insertion de données d'exemple
    # Validation des données
    # Logging des opérations
```

## Critères de qualité

### Code
- **Standards**: Respect PEP8
- **Documentation**: Docstrings complètes
- **Tests**: Couverture minimale 80%
- **Logging**: Traçabilité des opérations

### Base de données
- **Intégrité**: Contraintes respectées
- **Performance**: Index sur les clés étrangères
- **Sécurité**: Hashage des mots de passe
- **Données**: Exemples réalistes

## Risques identifiés

### Risque 1: Complexité des relations
**Impact**: Moyen  
**Probabilité**: Faible  
**Mitigation**: Tests approfondis des relations

### Risque 2: Performance de l'initialisation
**Impact**: Faible  
**Probabilité**: Moyen  
**Mitigation**: Optimisation des requêtes d'insertion

### Risque 3: Compatibilité des versions
**Impact**: Moyen  
**Probabilité**: Faible  
**Mitigation**: Tests sur différentes versions Python

## Métriques de suivi

### Vélocité
- **Prévue**: 8 story points
- **Réalisée**: À mesurer
- **Efficacité**: Temps réel vs estimé

### Qualité
- **Bugs**: 0 critique, 0 majeur
- **Tests**: 80% couverture minimum
- **Performance**: < 2s pour l'initialisation

### Progression
- **US-001**: 0% → 100%
- **US-002**: 0% → 100%

## Livrables du Sprint

### Code
- [ ] Application Flask fonctionnelle
- [ ] Modèles de données complets
- [ ] Script d'initialisation
- [ ] Tests unitaires

### Documentation
- [ ] README technique
- [ ] Documentation des modèles
- [ ] Guide d'installation
- [ ] Architecture technique

### Base de données
- [ ] Schéma de base de données
- [ ] Données d'exemple
- [ ] Scripts de migration
- [ ] Documentation des relations

## Définition de fini du Sprint

### Fonctionnel
- [ ] Application Flask démarre sans erreur
- [ ] Tous les modèles créés et testés
- [ ] Base de données initialisée avec données d'exemple
- [ ] Scripts d'initialisation fonctionnels

### Technique
- [ ] Code respecte les standards PEP8
- [ ] Documentation complète
- [ ] Tests unitaires passent
- [ ] Logging configuré

### Qualité
- [ ] Aucun bug critique
- [ ] Performance acceptable
- [ ] Code maintenable
- [ ] Documentation à jour

## Notes importantes

1. **Priorité**: Infrastructure avant fonctionnalités
2. **Qualité**: Standards élevés dès le début
3. **Documentation**: Essentielle pour la suite
4. **Tests**: Base solide pour l'évolution

---

**Date de création**: 2024  
**Dernière mise à jour**: 2024  
**Responsable**: Scrum Master  
**Statut**: En cours

