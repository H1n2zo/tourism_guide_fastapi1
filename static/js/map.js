let map;
let markersMap = {};
const destinationsMap = {};

function initMap() {
    // Wait for map element to exist
    const mapElement = document.getElementById('map');
    if (!mapElement) {
        console.error('Map element not found');
        return;
    }
    
    // Initialize map centered on Ormoc City
    map = L.map('map').setView([11.0059, 124.6075], 13);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);

    // Add markers after map is ready
    setTimeout(addDestinationMarkers, 100);
}

function addDestinationMarkers() {
    // Validate destinations data exists
    if (!window.destinations || !Array.isArray(window.destinations)) {
        console.error('Destinations data not available');
        return;
    }
    
    console.log('Adding markers for', window.destinations.length, 'destinations');
    
    window.destinations.forEach(dest => {
        // Validate coordinates
        if (!dest.latitude || !dest.longitude) {
            console.warn('Skipping destination without coordinates:', dest.name);
            return;
        }
        
        // Convert to numbers
        const lat = parseFloat(dest.latitude);
        const lng = parseFloat(dest.longitude);
        
        // Validate parsed coordinates
        if (isNaN(lat) || isNaN(lng)) {
            console.warn('Invalid coordinates for:', dest.name);
            return;
        }
        
        // Store in destinationsMap for route drawing
        destinationsMap[dest.id] = {
            lat: lat,
            lng: lng,
            name: dest.name
        };
        
        // Create marker
        const marker = L.marker([lat, lng]).addTo(map);
        const popupContent = createPopupContent(dest);
        
        marker.bindPopup(popupContent, {
            maxWidth: 320,
            className: 'custom-popup'
        });
        
        markersMap[dest.id] = marker;
    });
    
    console.log('destinationsMap populated with', Object.keys(destinationsMap).length, 'destinations');
}

function createPopupContent(dest) {
    const imageUrl = dest.image_path 
        ? window.UPLOAD_URL + dest.image_path
        : `https://via.placeholder.com/300x200?text=${encodeURIComponent(dest.name)}`;
    
    const ratingHtml = dest.review_count > 0 
        ? `
               ${'★'.repeat(Math.round(dest.avg_rating))}${'☆'.repeat(5-Math.round(dest.avg_rating))}
               ${dest.avg_rating.toFixed(1)} (${dest.review_count} reviews)
           `
        : 'Not rated yet';
    
    const description = dest.description && dest.description.length > 120 
        ? dest.description.substring(0, 120) + '...' 
        : (dest.description || 'No description available');
    
    return `
        
            
            ${dest.name}
            
                 ${dest.category_name || 'General'}
            
            ${ratingHtml}
            ${description}
            
                 View Details
            
        
    `;
}

function showOnMap(lat, lng, destName) {
    if (!map) {
        console.error('Map not initialized');
        return;
    }
    
    if (!lat || !lng) {
        console.warn('Invalid coordinates');
        return;
    }
    
    // Convert to numbers
    lat = parseFloat(lat);
    lng = parseFloat(lng);
    
    if (isNaN(lat) || isNaN(lng)) {
        console.warn('Cannot parse coordinates');
        return;
    }
    
    // Center map on location
    map.setView([lat, lng], 15);
    
    // Scroll to map
    document.getElementById('mapI').scrollIntoView({behavior: 'smooth'});
    
    // Find and open marker popup
    setTimeout(() => {
        const dest = window.destinations.find(d => 
            Math.abs(parseFloat(d.latitude) - lat) < 0.0001 && 
            Math.abs(parseFloat(d.longitude) - lng) < 0.0001
        );
        
        if (dest && markersMap[dest.id]) {
            markersMap[dest.id].openPopup();
        }
    }, 500);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        if (document.getElementById('map')) {
            initMap();
        }
    });
} else {
    if (document.getElementById('map')) {
        initMap();
    }
}