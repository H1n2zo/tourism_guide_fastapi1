// Main initialization and UI interactions

function initBackToTop() {
    const backToTopBtn = document.getElementById('backToTop');
    
    if (!backToTopBtn) return;
    
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    });
    
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({top: 0, behavior: 'smooth'});
    });
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initBackToTop();
    
    // Initialize map if element exists
    if (document.getElementById('map')) {
        initMap();
    }
    
    // Load routes if element exists
    if (document.getElementById('routesList')) {
        loadRoutes();
    }
});