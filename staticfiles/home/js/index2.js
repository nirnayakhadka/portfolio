// Portfolio JavaScript for Enhanced Animations and Interactions
// File: /home/nirnaya/myportfolio/home/static/home/js/index2.js

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all animations and interactions
    initLoader();
    createParticles();
    initScrollAnimations();
    initSmoothScroll();
    initParallaxEffect();
    initProfileImageEffects();
    initSkillCardAnimations();
    initProjectCardAnimations();
    initTypewriterEffect();
    initMouseTracker();
    initScrollIndicator();
});

// Loading Screen Animation
function initLoader() {
    const loader = document.getElementById('loadingScreen');
    
    // Simulate loading time
    setTimeout(() => {
        loader.classList.add('hidden');
        // Trigger entry animations
        triggerEntryAnimations();
    }, 2000);
}

// Create animated particles
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        createParticle(particlesContainer);
    }
    
    // Continuously create new particles
    setInterval(() => {
        if (particlesContainer.children.length < particleCount) {
            createParticle(particlesContainer);
        }
    }, 300);
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    
    // Random starting position
    particle.style.left = Math.random() * 100 + 'vw';
    particle.style.animationDelay = Math.random() * 15 + 's';
    particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
    
    // Random size and opacity
    const size = Math.random() * 4 + 1;
    particle.style.width = size + 'px';
    particle.style.height = size + 'px';
    particle.style.opacity = Math.random() * 0.8 + 0.2;
    
    container.appendChild(particle);
    
    // Remove particle after animation
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
        }
    }, 25000);
}

// Scroll-triggered animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe all animatable elements
    document.querySelectorAll('.skill-card, .project-card').forEach(el => {
        observer.observe(el);
    });
}

// Smooth scrolling for navigation
function initSmoothScroll() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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

// Parallax scrolling effects
function initParallaxEffect() {
    let ticking = false;
    
    function updateParallax() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.hero-bg, .floating-elements');
        
        parallaxElements.forEach(el => {
            const speed = el.dataset.speed || 0.5;
            const yPos = -(scrolled * speed);
            el.style.transform = `translate3d(0, ${yPos}px, 0)`;
        });
        
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestTick);
}

// Enhanced profile image effects
function initProfileImageEffects() {
    const profileImage = document.querySelector('.profile-image');
    const profileContainer = document.querySelector('.profile-container');
    
    if (!profileImage || !profileContainer) return;
    
    // Mouse tracking for 3D tilt effect
    profileContainer.addEventListener('mousemove', (e) => {
        const rect = profileContainer.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        const mouseX = e.clientX - centerX;
        const mouseY = e.clientY - centerY;
        
        const rotateX = (mouseY / rect.height) * -10;
        const rotateY = (mouseX / rect.width) * 10;
        
        profileImage.style.transform = `
            perspective(1000px) 
            rotateX(${rotateX}deg) 
            rotateY(${rotateY}deg) 
            scale(1.05)
        `;
    });
    
    profileContainer.addEventListener('mouseleave', () => {
        profileImage.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale(1)';
    });
    
    // Glowing effect on hover
    profileContainer.addEventListener('mouseenter', () => {
        profileImage.style.boxShadow = '0 20px 60px rgba(100, 255, 218, 0.6)';
        profileImage.style.borderColor = 'rgba(100, 255, 218, 0.8)';
    });
    
    profileContainer.addEventListener('mouseleave', () => {
        profileImage.style.boxShadow = '0 20px 60px rgba(100, 255, 218, 0.3)';
        profileImage.style.borderColor = 'rgba(100, 255, 218, 0.3)';
    });
}

// Skill card hover animations
function initSkillCardAnimations() {
    const skillCards = document.querySelectorAll('.skill-card');
    
    skillCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-15px) scale(1.02)';
            this.style.boxShadow = '0 25px 80px rgba(100, 255, 218, 0.3)';
            
            const icon = this.querySelector('.skill-icon i');
            if (icon) {
                icon.style.transform = 'scale(1.2) rotate(5deg)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 10px 40px rgba(100, 255, 218, 0.1)';
            
            const icon = this.querySelector('.skill-icon i');
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }
        });
        
        // Add random animation delay for staggered entrance
        card.style.animationDelay = Math.random() * 0.5 + 's';
    });
}

// Project card animations
function initProjectCardAnimations() {
    const projectCards = document.querySelectorAll('.project-card');
    
    projectCards.forEach((card, index) => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-15px) rotate(2deg) scale(1.02)';
            
            const projectImage = this.querySelector('.project-image');
            if (projectImage) {
                projectImage.style.transform = 'scale(1.1)';
                projectImage.style.filter = 'brightness(1.1) saturate(1.2)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) rotate(0deg) scale(1)';
            
            const projectImage = this.querySelector('.project-image');
            if (projectImage) {
                projectImage.style.transform = 'scale(1)';
                projectImage.style.filter = 'brightness(1) saturate(1)';
            }
        });
        
        // Staggered animation entrance
        card.style.animationDelay = (index * 0.2) + 's';
    });
}

// Typewriter effect for dynamic text
function initTypewriterEffect() {
    const roles = ['Full-Stack Developer', 'Python Expert', 'Django Specialist', 'Problem Solver'];
    const subtitleElement = document.querySelector('.subtitle');
    
    if (!subtitleElement) return;
    
    let roleIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingSpeed = 100;
    
    function typeEffect() {
        const currentRole = roles[roleIndex];
        const currentText = isDeleting 
            ? currentRole.substring(0, charIndex - 1)
            : currentRole.substring(0, charIndex + 1);
        
        subtitleElement.textContent = currentText;
        
        if (!isDeleting && charIndex === currentRole.length) {
            // Pause before deleting
            setTimeout(() => {
                isDeleting = true;
                typeEffect();
            }, 2000);
            return;
        }
        
        if (isDeleting && charIndex === 0) {
            isDeleting = false;
            roleIndex = (roleIndex + 1) % roles.length;
            typingSpeed = 100;
        }
        
        charIndex += isDeleting ? -1 : 1;
        typingSpeed = isDeleting ? 50 : 100;
        
        setTimeout(typeEffect, typingSpeed);
    }
    
    // Start typewriter effect after initial delay
    setTimeout(typeEffect, 3000);
}

// Mouse cursor tracker with glowing trail
function initMouseTracker() {
    const cursor = document.createElement('div');
    cursor.className = 'cursor-glow';
    cursor.style.cssText = `
        position: fixed;
        width: 20px;
        height: 20px;
        background: radial-gradient(circle, rgba(100, 255, 218, 0.6) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 9999;
        mix-blend-mode: screen;
        transition: all 0.1s ease;
    `;
    document.body.appendChild(cursor);
    
    let mouseX = 0;
    let mouseY = 0;
    let cursorX = 0;
    let cursorY = 0;
    
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });
    
    function animateCursor() {
        cursorX += (mouseX - cursorX) * 0.1;
        cursorY += (mouseY - cursorY) * 0.1;
        cursor.style.left = cursorX + 'px';
        cursor.style.top = cursorY + 'px';
        requestAnimationFrame(animateCursor);
    }
    
    animateCursor();
    
    // Hide cursor on touch devices
    if ('ontouchstart' in window) {
        cursor.style.display = 'none';
    }
}

// Scroll indicator animation
function initScrollIndicator() {
    const scrollIndicator = document.getElementById('scrollIndicator');
    
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', () => {
            document.getElementById('skills').scrollIntoView({
                behavior: 'smooth'
            });
        });
        
        // Hide scroll indicator when scrolling
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 100) {
                scrollIndicator.style.opacity = '0';
            } else {
                scrollIndicator.style.opacity = '1';
            }
        });
    }
}

// Trigger entry animations after loading
function triggerEntryAnimations() {
    // Add entrance animations to elements
    const animatedElements = document.querySelectorAll('.hero-text h1, .hero-text .subtitle, .hero-text .description, .hero-buttons');
    
    animatedElements.forEach((el, index) => {
        setTimeout(() => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 200);
    });
    
    // Animate profile image entrance
    setTimeout(() => {
        const profileContainer = document.querySelector('.profile-container');
        if (profileContainer) {
            profileContainer.style.opacity = '1';
            profileContainer.style.transform = 'scale(1)';
        }
    }, 800);
}

// Add CSS for dynamic animations
const dynamicStyles = `
    .cursor-glow {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.5); opacity: 0.5; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .skill-card, .project-card {
        opacity: 0;
        transform: translateY(50px);
        transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .skill-card.animate-in, .project-card.animate-in {
        opacity: 1;
        transform: translateY(0);
    }
    
    .profile-container {
        opacity: 0;
        transform: scale(0.8);
        transition: all 1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .skill-icon i, .project-image {
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .btn-modern {
        position: relative;
        overflow: hidden;
    }
    
    .btn-modern::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .btn-modern:hover::before {
        left: 100%;
    }
`;

// Inject dynamic styles
const styleSheet = document.createElement('style');
styleSheet.textContent = dynamicStyles;
document.head.appendChild(styleSheet);

// Performance optimization
function debounce(func, wait) {
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

// Optimized scroll handler
const optimizedScrollHandler = debounce(() => {
    // Handle scroll-based animations here
    const scrolled = window.pageYOffset;
    const heroSection = document.getElementById('hero');
    
    if (heroSection) {
        const opacity = Math.max(0, 1 - scrolled / window.innerHeight);
        heroSection.style.opacity = opacity;
    }
}, 10);

window.addEventListener('scroll', optimizedScrollHandler);

// Resize handler for responsive adjustments
window.addEventListener('resize', debounce(() => {
    // Recalculate animations on resize
    const profileContainer = document.querySelector('.profile-container');
    if (profileContainer && window.innerWidth < 768) {
        // Adjust animations for mobile
        profileContainer.style.transform = 'scale(0.8)';
    }
}, 250));



console.log('🚀 Portfolio animations initialized successfully!');