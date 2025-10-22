/**
 * Script JavaScript principal pour l'application E-Commerce IA
 * 
 * Ce fichier contient toutes les fonctionnalités JavaScript pour :
 * - Gestion du panier
 * - Interactions utilisateur
 * - Animations et effets visuels
 * - Communication AJAX
 * 
 * Auteur: Développeur Senior Python Full Stack
 * Date: 2024
 */

// Configuration globale
const CONFIG = {
    API_BASE_URL: '',
    CART_UPDATE_DELAY: 300,
    ANIMATION_DURATION: 300
};

// Utilitaires
const Utils = {
    /**
     * Affiche une notification toast
     * @param {string} message - Message à afficher
     * @param {string} type - Type de notification (success, error, info, warning)
     */
    showToast(message, type = 'info') {
        const toastContainer = this.getOrCreateToastContainer();
        const toast = this.createToast(message, type);
        toastContainer.appendChild(toast);
        
        // Animation d'entrée
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Suppression automatique
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },

    /**
     * Crée ou récupère le conteneur de toasts
     * @returns {HTMLElement} Conteneur de toasts
     */
    getOrCreateToastContainer() {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container position-fixed top-0 end-0 p-3';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
        }
        return container;
    },

    /**
     * Crée un élément toast
     * @param {string} message - Message
     * @param {string} type - Type
     * @returns {HTMLElement} Élément toast
     */
    createToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        return toast;
    },

    /**
     * Formate un prix
     * @param {number} price - Prix à formater
     * @returns {string} Prix formaté
     */
    formatPrice(price) {
        return new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: 'EUR'
        }).format(price);
    },

    /**
     * Débounce une fonction
     * @param {Function} func - Fonction à débouncer
     * @param {number} wait - Délai d'attente
     * @returns {Function} Fonction débouncée
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Gestionnaire du panier
const CartManager = {
    /**
     * Met à jour le compteur du panier
     */
    updateCartCount() {
        fetch('/cart')
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const cartItems = doc.querySelectorAll('.cart-item');
                const cartCount = document.getElementById('cart-count');
                
                if (cartCount) {
                    cartCount.textContent = cartItems.length;
                    
                    // Animation du compteur
                    if (cartItems.length > 0) {
                        cartCount.classList.add('pulse');
                        setTimeout(() => cartCount.classList.remove('pulse'), 300);
                    }
                }
            })
            .catch(error => console.error('Erreur lors de la mise à jour du panier:', error));
    },

    /**
     * Ajoute un produit au panier
     * @param {number} productId - ID du produit
     * @param {HTMLElement} button - Bouton cliqué
     */
    addToCart(productId, button) {
        // Vérification de la connexion
        if (!this.isUserLoggedIn()) {
            window.location.href = '/login';
            return;
        }

        // Désactivation du bouton pendant la requête
        button.disabled = true;
        button.classList.add('loading');

        fetch(`/add_to_cart/${productId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Erreur lors de l\'ajout au panier');
        })
        .then(html => {
            // Mise à jour du compteur
            this.updateCartCount();
            
            // Animation de succès
            this.animateSuccess(button);
            
            // Notification
            Utils.showToast('Produit ajouté au panier !', 'success');
        })
        .catch(error => {
            console.error('Erreur:', error);
            Utils.showToast('Erreur lors de l\'ajout au panier', 'error');
        })
        .finally(() => {
            // Réactivation du bouton
            button.disabled = false;
            button.classList.remove('loading');
        });
    },

    /**
     * Vérifie si l'utilisateur est connecté
     * @returns {boolean} True si connecté
     */
    isUserLoggedIn() {
        // Vérification basée sur la présence d'éléments spécifiques
        return document.querySelector('[data-user-logged-in]') !== null;
    },

    /**
     * Anime le succès d'ajout au panier
     * @param {HTMLElement} button - Bouton à animer
     */
    animateSuccess(button) {
        const originalContent = button.innerHTML;
        const originalClasses = button.className;
        
        // Animation de succès
        button.innerHTML = '<i class="fas fa-check me-1"></i>Ajouté!';
        button.className = button.className.replace('btn-primary', 'btn-success');
        button.classList.add('pulse');
        
        // Retour à l'état normal
        setTimeout(() => {
            button.innerHTML = originalContent;
            button.className = originalClasses;
            button.classList.remove('pulse');
        }, 2000);
    }
};

// Initialisation de l'application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 E-Commerce IA - Application initialisée');
    
    // Gestion des boutons "Ajouter au panier"
    document.addEventListener('click', (e) => {
        if (e.target.closest('.add-to-cart')) {
            const button = e.target.closest('.add-to-cart');
            const productId = button.getAttribute('data-product-id');
            CartManager.addToCart(productId, button);
        }
    });
    
    // Mise à jour initiale du panier
    if (document.querySelector('[data-user-logged-in]')) {
        CartManager.updateCartCount();
    }
    
    // Gestion des toasts Bootstrap
    const toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(toast => {
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
    });
    
    console.log('✅ Tous les gestionnaires ont été initialisés');
});

// Export pour utilisation dans d'autres modules
window.ECommerceApp = {
    Utils,
    CartManager
};