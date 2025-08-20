// Modern Portfolio JavaScript - Error-Free Version
console.log('🚀 Portfolio JavaScript Loading...');

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all features with error handling
    try {
        console.log('Initializing Portfolio Features...');
        
        initParticleSystem();
        initTypingEffect();
        initScrollEffects();
        initMouseParallax();
        initSmoothScrolling();
        initIntersectionObserver();
        initCounterAnimations();
        initModernEffects();
        initLoadingAnimation();
        
        console.log(' Portfolio Initialized Successfully!');
        
    } catch (error) {
        console.error('❌ Error initializing portfolio:', error);
    }
    
    // Particle System with Error Handling
    function initParticleSystem() {
        const particlesContainer = document.getElementById('particles');
        if (!particlesContainer) {
            console.warn('Particles container not found');
            return;
        }
        
        const particleCount = window.innerWidth > 768 ? 50 : 30;
        const colors = ['color-1', 'color-2', 'color-3', 'color-4', 'color-5'];
        
        function createParticle() {
            const particle = document.createElement('div');
            particle.classList.add('particle', colors[Math.floor(Math.random() * colors.length)]);
            
            // Random positioning and timing
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 10 + 's';
            particle.style.animationDuration = (Math.random() * 15 + 15) + 's';
            
            // Random size variation
            const size = Math.random() * 3 + 2;
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';
            
            // Random opacity
            particle.style.opacity = Math.random() * 0.6 + 0.4;
            
            particlesContainer.appendChild(particle);
            
            // Remove particle after animation with error handling
            setTimeout(() => {
                if (particle && particle.parentNode) {
                    particle.parentNode.removeChild(particle);
                }
            }, 30000); // 30 second cleanup
        }
        
        // Create initial particles
        for (let i = 0; i < particleCount; i++) {
            setTimeout(() => createParticle(), Math.random() * 5000);
        }
        
        // Continuously create new particles
        setInterval(createParticle, 300);
        
        console.log('🌟 Particle system initialized');
    }
    
    // Enhanced Typing Effect
    function initTypingEffect() {
        const typingElement = document.getElementById('typingText');
        if (!typingElement) {
            console.warn('Typing element not found');
            return;
        }
        
        const texts = [
            'Nirnaya',
            'an AI Developer',
            'a Problem Solver',
            'a Tech Innovator',
            'a Full-Stack Developer',
            'a Machine Learning Expert'
        ];
        
        let textIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        let typingSpeed = 100;
        
        function type() {
            if (!typingElement) return;
            
            const currentText = texts[textIndex];
            
            if (isDeleting) {
                typingElement.textContent = currentText.substring(0, charIndex - 1);
                charIndex--;
                typingSpeed = 50;
            } else {
                typingElement.textContent = currentText.substring(0, charIndex + 1);
                charIndex++;
                typingSpeed = 100;
            }
            
            if (!isDeleting && charIndex === currentText.length) {
                isDeleting = true;
                typingSpeed = 2000; // Pause before deleting
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                textIndex = (textIndex + 1) % texts.length;
                typingSpeed = 500; // Pause before typing next text
            }
            
            setTimeout(type, typingSpeed);
        }
        
        // Start typing effect
        setTimeout(type, 1000);
        console.log('⌨️ Typing effect initialized');
    }
    
    // Mouse Parallax Effect
    function initMouseParallax() {
        const hero = document.querySelector('.hero-section');
        const profileGlow = document.querySelector('.profile-glow');
        const geometricShapes = document.querySelectorAll('.geometric-shape');
        
        if (!hero) return;
        
        let mouseX = 0, mouseY = 0;
        let isMouseMoving = false;
        
        hero.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
            isMouseMoving = true;
            
            const { innerWidth, innerHeight } = window;
            const xPercent = (mouseX / innerWidth - 0.5) * 2;
            const yPercent = (mouseY / innerHeight - 0.5) * 2;
            
            // Profile glow parallax
            if (profileGlow) {
                const moveX = xPercent * 15;
                const moveY = yPercent * 15;
                profileGlow.style.transform = `translate(${moveX}px, ${moveY}px)`;
            }
            
            // Geometric shapes parallax
            geometricShapes.forEach((shape, index) => {
                const speed = (index + 1) * 0.5;
                const moveX = xPercent * speed;
                const moveY = yPercent * speed;
                shape.style.transform += ` translate(${moveX}px, ${moveY}px)`;
            });
        });
        
        hero.addEventListener('mouseleave', () => {
            isMouseMoving = false;
            
            // Reset transforms
            if (profileGlow) {
                profileGlow.style.transform = 'translate(0px, 0px)';
            }
            
            geometricShapes.forEach(shape => {
                shape.style.transform = shape.style.transform.replace(/translate\([^)]*\)/g, '');
            });
        });
        
        console.log('🎯 Mouse parallax initialized');
    }
    
    // Scroll Effects
    function initScrollEffects() {
        const scrollProgress = document.getElementById('scrollProgress');
        const scrollIndicator = document.getElementById('scrollIndicator');
        
        let ticking = false;
        
        function updateScrollProgress() {
            if (!scrollProgress) return;
            
            const scrollTop = window.pageYOffset;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const scrollPercent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
            
            scrollProgress.style.width = Math.min(scrollPercent, 100) + '%';
        }
        
        function handleScroll() {
            const scrolled = window.pageYOffset;
            const heroHeight = window.innerHeight;
            
            // Hide/show scroll indicator
            if (scrollIndicator) {
                if (scrolled > heroHeight * 0.2) {
                    scrollIndicator.style.opacity = '0';
                    scrollIndicator.style.transform = 'translateX(-50%) translateY(20px)';
                } else {
                    scrollIndicator.style.opacity = '0.8';
                    scrollIndicator.style.transform = 'translateX(-50%) translateY(0)';
                }
            }
            
            updateScrollProgress();
            ticking = false;
        }
        
        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(handleScroll);
                ticking = true;
            }
        }, { passive: true });
        
        // Scroll indicator click
        if (scrollIndicator) {
            scrollIndicator.addEventListener('click', () => {
                const skillsSection = document.getElementById('skills');
                if (skillsSection) {
                    skillsSection.scrollIntoView({ behavior: 'smooth' });
                }
            });
        }
        
        console.log('📜 Scroll effects initialized');
    }
    
    // Smooth Scrolling for Navigation
    function initSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const target = document.querySelector(targetId);
                
                if (target) {
                    const headerOffset = 80; // Account for any fixed header
                    const elementPosition = target.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                    
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
        
        console.log('🔗 Smooth scrolling initialized');
    }
    
    // Intersection Observer for Animations
    function initIntersectionObserver() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('visible')) {
                    const delay = entry.target.dataset.delay ? parseInt(entry.target.dataset.delay) : 0;
                    
                    setTimeout(() => {
                        entry.target.classList.add('visible');
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, delay);
                }
            });
        }, observerOptions);
        
        // Observe all animatable elements
        const elements = document.querySelectorAll('.animate-on-scroll, .skill-card, .education-card, .stat-card');
        elements.forEach(el => {
            if (el) observer.observe(el);
        });
        
        console.log('👁️ Intersection observer initialized');
    }
    
    // Counter Animations
    function initCounterAnimations() {
        const counters = document.querySelectorAll('.stat-number');
        
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                    entry.target.classList.add('counted');
                    animateCounter(entry.target);
                }
            });
        }, { threshold: 0.7 });
        
        counters.forEach(counter => {
            if (counter) counterObserver.observe(counter);
        });
        
        function animateCounter(counter) {
            const target = parseInt(counter.dataset.target) || 0;
            const duration = 2000;
            const start = 0;
            const increment = target / (duration / 16);
            let current = 0;
            
            const updateCounter = () => {
                if (current < target) {
                    current += increment;
                    counter.textContent = Math.min(Math.floor(current), target);
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target;
                }
            };
            
            updateCounter();
        }
        
        console.log('🔢 Counter animations initialized');
    }
    
    // Modern Button Effects
    function initModernEffects() {
        // Ripple effect for buttons
        const buttons = document.querySelectorAll('.modern-btn');
        
        buttons.forEach(btn => {
            btn.style.position = 'relative';
            btn.style.overflow = 'hidden';
            
            btn.addEventListener('click', function(e) {
                createRipple(e, this);
            });
            
            // Magnetic effect
            btn.addEventListener('mousemove', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                
                const moveX = x * 0.1;
                const moveY = y * 0.1;
                
                this.style.transform = `translate(${moveX}px, ${moveY}px)`;
            });
            
            btn.addEventListener('mouseleave', function() {
                this.style.transform = 'translate(0px, 0px)';
            });
        });
        
        // Social links enhanced effects
        const socialLinks = document.querySelectorAll('.social-link');
        socialLinks.forEach(link => {
            link.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-10px) scale(1.1) rotate(5deg)';
            });
            
            link.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1) rotate(0deg)';
            });
        });
        
        console.log('✨ Modern effects initialized');
    }
    
    function createRipple(e, button) {
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        const ripple = document.createElement('span');
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
            z-index: 1;
        `;
        
        button.appendChild(ripple);
        
        setTimeout(() => {
            if (ripple && ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        }, 600);
    }
    
    // Loading Animation
    function initLoadingAnimation() {
        document.body.classList.add('loading');
        
        window.addEventListener('load', () => {
            setTimeout(() => {
                document.body.classList.remove('loading');
                document.body.classList.add('loaded');
                
                // Trigger any additional entrance animations
                const heroElements = document.querySelectorAll('.hero-title, .hero-subtitle, .hero-description');
                heroElements.forEach((el, index) => {
                    if (el) {
                        setTimeout(() => {
                            el.style.opacity = '1';
                            el.style.transform = 'translateY(0)';
                        }, index * 200);
                    }
                });
                
            }, 100);
        });
        
        console.log('🎬 Loading animation initialized');
    }
    
    // Cursor Trail Effect (Desktop Only)
    function initCursorTrail() {
        if (window.innerWidth <= 768) return; // Skip on mobile
        
        const trail = [];
        const trailLength = 15;
        
        for (let i = 0; i < trailLength; i++) {
            const dot = document.createElement('div');
            dot.style.cssText = `
                position: fixed;
                width: 6px;
                height: 6px;
                background: rgba(102, 126, 234, 0.6);
                border-radius: 50%;
                pointer-events: none;
                z-index: 9999;
                transition: all 0.1s ease;
                transform: scale(0);
            `;
            document.body.appendChild(dot);
            trail.push(dot);
        }
        
        let mouseX = 0, mouseY = 0;
        
        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });
        
        function updateTrail() {
            trail.forEach((dot, index) => {
                const delay = index * 50;
                const scale = (trailLength - index) / trailLength;
                
                setTimeout(() => {
                    dot.style.left = mouseX + 'px';
                    dot.style.top = mouseY + 'px';
                    dot.style.transform = `scale(${scale * 0.8})`;
                    dot.style.opacity = scale * 0.8;
                }, delay);
            });
            
            requestAnimationFrame(updateTrail);
        }
        
        updateTrail();
        console.log('🖱️ Cursor trail initialized');
    }
    
    // Initialize cursor trail on desktop
    if (window.innerWidth > 768) {
        initCursorTrail();
    }
    
    // Performance optimization
    function optimizePerformance() {
        // Reduce effects on mobile
        if (window.innerWidth <= 768) {
            const particles = document.querySelectorAll('.particle');
            particles.forEach((particle, index) => {
                if (index > 20) particle.remove();
            });
        }
        
        // Disable animations for users who prefer reduced motion
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            document.documentElement.style.setProperty('--animation-duration', '0.01s');
        }
    }
    
    optimizePerformance();
    
    // Window resize handler
    window.addEventListener('resize', () => {
        optimizePerformance();
    });
    
    // Add CSS animations via JavaScript
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .skill-card.visible,
        .stat-card.visible,
        .education-card.visible {
            animation: slideInUp 0.6s ease forwards;
        }
    `;
    
    if (!document.head.querySelector('#portfolio-animations')) {
        style.id = 'portfolio-animations';
        document.head.appendChild(style);
    }
    
    // Console styling for development
    console.log('%c🎉 Portfolio Fully Loaded! 🎉', 'color: #667eea; font-size: 16px; font-weight: bold;');
    
});

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Portfolio Error:', e.error);
});

// Preload critical resources
window.addEventListener('load', () => {
    const criticalImages = [
        '{% static "IMG_3480.jpg" %}'
    ];
    
    criticalImages.forEach(src => {
        if (src && !src.includes('{%')) {
            const img = new Image();
            img.src = src;
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll(".education-image");

    images.forEach(img => {
        function fitImage() {
            img.style.width = "100%";
            img.style.height = "100%";
            img.style.objectFit = "cover"; // change to "contain" if you don’t want cropping
        }

        if (img.complete) {
            fitImage();
        } else {
            img.onload = fitImage;
        }

        window.addEventListener("resize", fitImage);
    });
});

