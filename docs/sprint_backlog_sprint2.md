# Sprint Backlog - Sprint 2
**Durée**: 2 semaines  
**Objectif**: Authentification utilisateur et gestion du panier  
**Vélocité prévue**: 13 story points

## Vue d'ensemble du Sprint

### Objectifs du Sprint
- Implémenter l'authentification utilisateur (inscription/connexion)
- Développer la gestion du panier d'achat
- Créer les templates HTML avec Bootstrap
- Intégrer les fonctionnalités de base de l'e-commerce

### Équipe
- **Scrum Master**: Développeur Senior
- **Product Owner**: Développeur Senior
- **Développeur**: Développeur Senior Python Full Stack

## User Stories du Sprint

### US-003: Inscription utilisateur
**Effort**: 5 story points  
**Statut**: À faire

#### Tâches détaillées
- [ ] Créer le template register.html
  - [ ] Formulaire d'inscription
  - [ ] Validation côté client (JavaScript)
  - [ ] Messages d'erreur appropriés
  - [ ] Design responsive avec Bootstrap
- [ ] Implémenter la logique d'inscription
  - [ ] Route Flask /register
  - [ ] Validation des données
  - [ ] Vérification unicité email/username
  - [ ] Hashage sécurisé des mots de passe
  - [ ] Gestion des erreurs
- [ ] Tests d'inscription
  - [ ] Test avec données valides
  - [ ] Test avec données invalides
  - [ ] Test unicité des identifiants
  - [ ] Test sécurité des mots de passe

#### Critères d'acceptation
- [ ] Formulaire d'inscription fonctionnel
- [ ] Validation des données côté serveur
- [ ] Hashage sécurisé des mots de passe
- [ ] Vérification unicité email/username
- [ ] Messages d'erreur clairs
- [ ] Redirection après inscription réussie

#### Définition de fini
- [ ] Code testé et fonctionnel
- [ ] Interface utilisateur responsive
- [ ] Sécurité validée
- [ ] Documentation mise à jour

### US-004: Connexion utilisateur
**Effort**: 3 story points  
**Statut**: À faire

#### Tâches détaillées
- [ ] Créer le template login.html
  - [ ] Formulaire de connexion
  - [ ] Validation côté client
  - [ ] Design cohérent avec l'inscription
- [ ] Implémenter la logique de connexion
  - [ ] Route Flask /login
  - [ ] Vérification des identifiants
  - [ ] Gestion des sessions
  - [ ] Redirection après connexion
- [ ] Gestion de la déconnexion
  - [ ] Route Flask /logout
  - [ ] Nettoyage de la session
  - [ ] Redirection appropriée

#### Critères d'acceptation
- [ ] Formulaire de connexion fonctionnel
- [ ] Vérification des identifiants
- [ ] Gestion des sessions sécurisée
- [ ] Redirection après connexion
- [ ] Gestion de la déconnexion
- [ ] Messages d'erreur appropriés

#### Définition de fini
- [ ] Authentification sécurisée
- [ ] Gestion des sessions robuste
- [ ] Interface utilisateur intuitive
- [ ] Tests de sécurité passés

### US-005: Gestion du panier
**Effort**: 8 story points  
**Statut**: À faire

#### Tâches détaillées
- [ ] Créer le template cart.html
  - [ ] Affichage des articles du panier
  - [ ] Modification des quantités
  - [ ] Suppression d'articles
  - [ ] Calcul du total
  - [ ] Design responsive
- [ ] Implémenter l'ajout au panier
  - [ ] Route Flask /add_to_cart/<product_id>
  - [ ] Vérification de la connexion
  - [ ] Gestion des quantités
  - [ ] Persistance en base de données
- [ ] Implémenter la suppression du panier
  - [ ] Route Flask /remove_from_cart/<cart_item_id>
  - [ ] Vérification des permissions
  - [ ] Suppression sécurisée
- [ ] Implémenter la finalisation de commande
  - [ ] Route Flask /checkout
  - [ ] Création des achats
  - [ ] Nettoyage du panier
  - [ ] Redirection vers l'historique

#### Critères d'acceptation
- [ ] Ajout de produits au panier
- [ ] Modification des quantités
- [ ] Suppression d'articles
- [ ] Calcul correct des totaux
- [ ] Persistance du panier
- [ ] Finalisation de commande
- [ ] Gestion des erreurs

#### Définition de fini
- [ ] Panier fonctionnel et sécurisé
- [ ] Interface utilisateur intuitive
- [ ] Gestion des erreurs appropriée
- [ ] Tests de régression passés

## Planification du Sprint

### Semaine 1
**Jour 1-2**: Templates d'authentification
- Création des templates HTML
- Intégration Bootstrap
- Validation côté client

**Jour 3-4**: Logique d'authentification
- Routes Flask d'inscription/connexion
- Gestion des sessions
- Tests de sécurité

**Jour 5**: Interface du panier
- Template cart.html
- Design responsive
- Intégration JavaScript

### Semaine 2
**Jour 1-2**: Logique du panier
- Routes Flask du panier
- Gestion des quantités
- Persistance en base

**Jour 3-4**: Finalisation et tests
- Tests d'intégration
- Gestion des erreurs
- Optimisation des performances

**Jour 5**: Revue de sprint
- Démonstration des fonctionnalités
- Rétrospective
- Planification du sprint suivant

## Tâches techniques détaillées

### Templates HTML
```html
<!-- register.html -->
<form method="POST">
    <input type="text" name="username" required>
    <input type="email" name="email" required>
    <input type="password" name="password" required>
    <button type="submit">S'inscrire</button>
</form>

<!-- login.html -->
<form method="POST">
    <input type="text" name="username" required>
    <input type="password" name="password" required>
    <button type="submit">Se connecter</button>
</form>

<!-- cart.html -->
<div class="cart-item">
    <img src="{{ item.product.image_url }}">
    <h5>{{ item.product.name }}</h5>
    <span>{{ item.quantity }}</span>
    <span>{{ item.get_total_price() }} €</span>
    <button onclick="removeItem({{ item.id }})">Supprimer</button>
</div>
```

### Routes Flask
```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Logique d'inscription
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Logique de connexion
    pass

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Ajout au panier
    pass

@app.route('/remove_from_cart/<int:cart_item_id>')
def remove_from_cart(cart_item_id):
    # Suppression du panier
    pass

@app.route('/checkout')
def checkout():
    # Finalisation de commande
    pass
```

### JavaScript
```javascript
// Gestion du panier
function addToCart(productId) {
    fetch(`/add_to_cart/${productId}`)
        .then(response => response.json())
        .then(data => {
            updateCartCount();
            showSuccessMessage();
        });
}

function updateCartCount() {
    // Mise à jour du compteur
}

function showSuccessMessage() {
    // Notification de succès
}
```

## Critères de qualité

### Sécurité
- **Hashage**: Mots de passe hashés avec Werkzeug
- **Validation**: Toutes les entrées validées
- **Sessions**: Gestion sécurisée des sessions
- **CSRF**: Protection contre les attaques CSRF

### Interface utilisateur
- **Responsive**: Compatible mobile et desktop
- **Accessibilité**: Standards WCAG de base
- **Performance**: Temps de chargement < 3s
- **Cohérence**: Design uniforme

### Fonctionnalités
- **Robustesse**: Gestion des erreurs appropriée
- **Persistance**: Données sauvegardées correctement
- **Navigation**: Parcours utilisateur fluide
- **Feedback**: Messages d'erreur clairs

## Risques identifiés

### Risque 1: Sécurité des sessions
**Impact**: Critique  
**Probabilité**: Moyen  
**Mitigation**: Tests de sécurité approfondis

### Risque 2: Performance du panier
**Impact**: Moyen  
**Probabilité**: Faible  
**Mitigation**: Optimisation des requêtes

### Risque 3: Compatibilité navigateurs
**Impact**: Moyen  
**Probabilité**: Faible  
**Mitigation**: Tests sur différents navigateurs

## Métriques de suivi

### Vélocité
- **Prévue**: 13 story points
- **Réalisée**: À mesurer
- **Efficacité**: Temps réel vs estimé

### Qualité
- **Bugs**: 0 critique, 0 majeur
- **Tests**: 80% couverture minimum
- **Performance**: < 2s pour les pages principales

### Progression
- **US-003**: 0% → 100%
- **US-004**: 0% → 100%
- **US-005**: 0% → 100%

## Livrables du Sprint

### Code
- [ ] Templates HTML complets
- [ ] Routes Flask d'authentification
- [ ] Routes Flask du panier
- [ ] JavaScript pour interactions

### Interface
- [ ] Design responsive
- [ ] Navigation intuitive
- [ ] Messages d'erreur clairs
- [ ] Animations et transitions

### Sécurité
- [ ] Authentification robuste
- [ ] Gestion des sessions
- [ ] Validation des données
- [ ] Protection CSRF

## Définition de fini du Sprint

### Fonctionnel
- [ ] Inscription utilisateur fonctionnelle
- [ ] Connexion utilisateur fonctionnelle
- [ ] Panier d'achat complet
- [ ] Finalisation de commande

### Technique
- [ ] Code sécurisé et testé
- [ ] Interface responsive
- [ ] Performance optimisée
- [ ] Documentation mise à jour

### Qualité
- [ ] Aucun bug critique
- [ ] Tests automatisés passent
- [ ] Code maintenable
- [ ] Sécurité validée

## Notes importantes

1. **Sécurité**: Priorité absolue pour l'authentification
2. **UX**: Interface utilisateur intuitive
3. **Performance**: Optimisation des requêtes
4. **Tests**: Couverture complète des fonctionnalités

---

**Date de création**: 2024  
**Dernière mise à jour**: 2024  
**Responsable**: Scrum Master  
**Statut**: En cours

