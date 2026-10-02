// Project Helix - Interactive UI Utilities
document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.getElementById('navLinks');

    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = mobileToggle.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-bars');
                icon.classList.toggle('fa-xmark');
            }
        });
    }

    // 2. Flash Message Auto-Dismiss and Manual Close
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(flash => {
        // Close button handler
        const closeBtn = flash.querySelector('.flash-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                flash.style.opacity = '0';
                flash.style.transform = 'translateX(40px)';
                setTimeout(() => flash.remove(), 300);
            });
        }

        // Auto dismiss after 5 seconds
        setTimeout(() => {
            if (flash && flash.parentNode) {
                flash.style.opacity = '0';
                flash.style.transform = 'translateX(40px)';
                setTimeout(() => flash.remove(), 300);
            }
        }, 5000);
    });

    // 3. Highlight Active Navigation Links automatically based on path
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('.nav-links a');

    links.forEach(link => {
        const href = link.getAttribute('href');
        if (href && href !== '#' && (currentPath === href || (href !== '/' && currentPath.startsWith(href)))) {
            link.classList.add('active');
        }
    });
});
