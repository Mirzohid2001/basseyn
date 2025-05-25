// ===== MODERN JAVASCRIPT FOR VODOPADDOV =====

class ModernSite {
    constructor() {
        this.navbar = document.getElementById('navbar');
        this.navToggle = document.getElementById('nav-toggle');
        this.navMenu = document.getElementById('nav-menu');
        this.backToTop = document.getElementById('backToTop');
        this.loadingScreen = document.getElementById('loading-screen');
        this.notification = document.getElementById('notification');
        
        this.init();
    }
    
    init() {
        this.setupLoading();
        this.setupNavigation();
        this.setupScrollEffects();
        this.setupAnimations();
        this.setupAjax();
        this.setupCounters();
        this.setupParallax();
    }
    
    // ===== LOADING SCREEN =====
    setupLoading() {
        window.addEventListener('load', () => {
            setTimeout(() => {
                this.loadingScreen.classList.add('hidden');
                this.animatePageLoad();
            }, 1000);
        });
    }
    
    animatePageLoad() {
        // GSAP page load animation
        gsap.timeline()
            .from('.navbar', {
                y: -80,
                opacity: 0,
                duration: 0.8,
                ease: 'power2.out'
            })
            .from('.hero-content', {
                y: 50,
                opacity: 0,
                duration: 1,
                ease: 'power2.out'
            }, '-=0.4');
    }
    
    // ===== NAVIGATION =====
    setupNavigation() {
        // Mobile menu toggle
        this.navToggle.addEventListener('click', () => {
            this.navToggle.classList.toggle('active');
            this.navMenu.classList.toggle('active');
        });
        
        // Close mobile menu when clicking on links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                this.navToggle.classList.remove('active');
                this.navMenu.classList.remove('active');
            });
        });
        
        // Navbar scroll effect
        window.addEventListener('scroll', () => {
            if (window.scrollY > 100) {
                this.navbar.classList.add('scrolled');
            } else {
                this.navbar.classList.remove('scrolled');
            }
        });
    }
    
    // ===== SCROLL EFFECTS =====
    setupScrollEffects() {
        // Back to top button
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                this.backToTop.classList.add('visible');
            } else {
                this.backToTop.classList.remove('visible');
            }
        });
        
        this.backToTop.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        
        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    // ===== GSAP ANIMATIONS =====
    setupAnimations() {
        // Register ScrollTrigger plugin
        gsap.registerPlugin(ScrollTrigger);
        
        // Fade in elements on scroll
        gsap.utils.toArray('.fade-in').forEach(element => {
            gsap.fromTo(element, {
                opacity: 0,
                y: 50
            }, {
                opacity: 1,
                y: 0,
                duration: 1,
                scrollTrigger: {
                    trigger: element,
                    start: 'top 80%',
                    end: 'bottom 20%',
                    toggleActions: 'play none none reverse'
                }
            });
        });
        
        // Stagger animations for cards
        gsap.utils.toArray('.card-container').forEach(container => {
            const cards = container.querySelectorAll('.card');
            gsap.fromTo(cards, {
                opacity: 0,
                y: 50,
                scale: 0.8
            }, {
                opacity: 1,
                y: 0,
                scale: 1,
                duration: 0.6,
                stagger: 0.1,
                ease: 'power2.out',
                scrollTrigger: {
                    trigger: container,
                    start: 'top 80%',
                    toggleActions: 'play none none reverse'
                }
            });
        });
        
        // Parallax effect for hero background
        if (document.querySelector('.hero-section')) {
            gsap.to('.hero-background', {
                yPercent: -50,
                ease: 'none',
                scrollTrigger: {
                    trigger: '.hero-section',
                    start: 'top bottom',
                    end: 'bottom top',
                    scrub: true
                }
            });
        }
    }
    
    // ===== COUNTERS =====
    setupCounters() {
        const counters = document.querySelectorAll('.stat-number');
        
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-count'));
            
            gsap.fromTo(counter, {
                innerHTML: 0
            }, {
                innerHTML: target,
                duration: 2,
                ease: 'power2.out',
                snap: { innerHTML: 1 },
                scrollTrigger: {
                    trigger: counter,
                    start: 'top 80%',
                    toggleActions: 'play none none reverse'
                },
                onUpdate: function() {
                    counter.innerHTML = Math.ceil(counter.innerHTML);
                }
            });
        });
    }
    
    // ===== PARALLAX EFFECTS =====
    setupParallax() {
        // Floating elements
        gsap.utils.toArray('.float').forEach(element => {
            gsap.to(element, {
                y: -20,
                duration: 2,
                ease: 'power1.inOut',
                yoyo: true,
                repeat: -1
            });
        });
        
        // Mouse move parallax
        document.addEventListener('mousemove', (e) => {
            const mouseX = e.clientX / window.innerWidth;
            const mouseY = e.clientY / window.innerHeight;
            
            gsap.to('.parallax-light', {
                x: mouseX * 30,
                y: mouseY * 30,
                duration: 1,
                ease: 'power2.out'
            });
            
            gsap.to('.parallax-medium', {
                x: mouseX * 20,
                y: mouseY * 20,
                duration: 1,
                ease: 'power2.out'
            });
            
            gsap.to('.parallax-heavy', {
                x: mouseX * 10,
                y: mouseY * 10,
                duration: 1,
                ease: 'power2.out'
            });
        });
    }
    
    // ===== AJAX FUNCTIONALITY =====
    setupAjax() {
        // Setup CSRF token for Django
        const csrfToken = this.getCookie('csrftoken');
        
        // Order form AJAX
        const orderForms = document.querySelectorAll('.order-form');
        orderForms.forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.submitOrderForm(form);
            });
        });
        
        // Contact form AJAX
        const contactForms = document.querySelectorAll('.contact-form');
        contactForms.forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.submitContactForm(form);
            });
        });
        
        // Product filtering
        const filterForms = document.querySelectorAll('.filter-form');
        filterForms.forEach(form => {
            const inputs = form.querySelectorAll('input, select');
            inputs.forEach(input => {
                input.addEventListener('change', () => {
                    this.filterProducts(form);
                });
            });
        });
    }
    
    // Submit order form via AJAX
    async submitOrderForm(form) {
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        
        // Show loading state
        this.setButtonLoading(submitBtn, true);
        
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': this.getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showNotification('Заказ успешно отправлен!', 'success');
                form.reset();
                
                // Animate success
                gsap.fromTo(form, {
                    scale: 1
                }, {
                    scale: 0.95,
                    duration: 0.1,
                    yoyo: true,
                    repeat: 1
                });
            } else {
                this.showNotification('Произошла ошибка. Попробуйте еще раз.', 'error');
            }
        } catch (error) {
            this.showNotification('Произошла ошибка соединения.', 'error');
        } finally {
            this.setButtonLoading(submitBtn, false);
        }
    }
    
    // Submit contact form via AJAX
    async submitContactForm(form) {
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        
        this.setButtonLoading(submitBtn, true);
        
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': this.getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showNotification('Сообщение отправлено!', 'success');
                form.reset();
            } else {
                this.showNotification('Произошла ошибка. Попробуйте еще раз.', 'error');
            }
        } catch (error) {
            this.showNotification('Произошла ошибка соединения.', 'error');
        } finally {
            this.setButtonLoading(submitBtn, false);
        }
    }
    
    // Filter products via AJAX
    async filterProducts(form) {
        const formData = new FormData(form);
        const productContainer = document.querySelector('.product-grid');
        
        if (!productContainer) return;
        
        // Show loading state
        productContainer.style.opacity = '0.5';
        
        try {
            const response = await fetch(form.action + '?' + new URLSearchParams(formData), {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newProducts = doc.querySelector('.product-grid');
            
            if (newProducts) {
                // Animate out old products
                gsap.to(productContainer.children, {
                    opacity: 0,
                    y: 20,
                    duration: 0.3,
                    stagger: 0.05,
                    onComplete: () => {
                        // Replace content
                        productContainer.innerHTML = newProducts.innerHTML;
                        
                        // Animate in new products
                        gsap.fromTo(productContainer.children, {
                            opacity: 0,
                            y: 20
                        }, {
                            opacity: 1,
                            y: 0,
                            duration: 0.5,
                            stagger: 0.1
                        });
                    }
                });
            }
        } catch (error) {
            this.showNotification('Ошибка при загрузке товаров.', 'error');
        } finally {
            productContainer.style.opacity = '1';
        }
    }
    
    // ===== UTILITY FUNCTIONS =====
    
    // Show notification
    showNotification(message, type = 'success') {
        const notification = this.notification;
        const icon = notification.querySelector('.notification-icon');
        const text = notification.querySelector('.notification-text');
        
        // Set content
        text.textContent = message;
        
        // Set type and icon
        notification.className = `notification ${type}`;
        icon.className = `notification-icon fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}`;
        
        // Show notification
        notification.classList.add('show');
        
        // Hide after 4 seconds
        setTimeout(() => {
            notification.classList.remove('show');
        }, 4000);
    }
    
    // Set button loading state
    setButtonLoading(button, loading) {
        if (loading) {
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Отправка...';
        } else {
            button.disabled = false;
            button.innerHTML = button.dataset.originalText || 'Отправить';
        }
    }
    
    // Get Django CSRF cookie
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Debounce function
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
    
    // Throttle function
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }
}

// ===== ADDITIONAL FEATURES =====

// Image lazy loading
class LazyImageLoader {
    constructor() {
        this.images = document.querySelectorAll('img[data-src]');
        this.imageObserver = new IntersectionObserver(this.onIntersection.bind(this));
        this.observe();
    }
    
    observe() {
        this.images.forEach(img => this.imageObserver.observe(img));
    }
    
    onIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                this.loadImage(entry.target);
                this.imageObserver.unobserve(entry.target);
            }
        });
    }
    
    loadImage(img) {
        img.src = img.dataset.src;
        img.addEventListener('load', () => {
            img.classList.add('loaded');
        });
    }
}

// Modal functionality
class Modal {
    constructor() {
        this.modals = document.querySelectorAll('.modal');
        this.setup();
    }
    
    setup() {
        // Open modal triggers
        document.querySelectorAll('[data-modal]').forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                this.open(trigger.dataset.modal);
            });
        });
        
        // Close modal triggers
        document.querySelectorAll('.modal-close').forEach(close => {
            close.addEventListener('click', () => {
                this.closeAll();
            });
        });
        
        // Close on backdrop click
        this.modals.forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.close(modal);
                }
            });
        });
        
        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeAll();
            }
        });
    }
    
    open(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
            
            // Animate modal
            gsap.fromTo(modal.querySelector('.modal-content'), {
                scale: 0.8,
                opacity: 0
            }, {
                scale: 1,
                opacity: 1,
                duration: 0.3,
                ease: 'power2.out'
            });
        }
    }
    
    close(modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    closeAll() {
        this.modals.forEach(modal => this.close(modal));
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ModernSite();
    new LazyImageLoader();
    new Modal();
});

// Performance optimization
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
} 