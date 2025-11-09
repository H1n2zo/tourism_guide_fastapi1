// Map initialization and marker management
let map;
let markersMap = {};
const destinationsMap = {};

function initMap() {
    map = L.map('map').setView([11.0059, 124.6075], 13);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);

    addDestinationMarkers();
}

function addDestinationMarkers() {
    if (!window.destinations) return;
    
    window.destinations.forEach(dest => {
        if (dest.latitude && dest.longitude) {
            destinationsMap[dest.id] = {
                lat: dest.latitude,
                lng: dest.longitude,
                name: dest.name
            };
            
            const marker = L.marker([dest.latitude, dest.longitude]).addTo(map);
            const popupContent = createPopupContent(dest);
            
            marker.bindPopup(popupContent, {
                maxWidth: 320,
                className: 'custom-popup'
            });
            
            markersMap[dest.id] = marker;
        }
    });
}

function createPopupContent(dest) {
    const imageUrl = dest.image_path 
        ? window.UPLOAD_URL + dest.image_path
        : `https://via.placeholder.com/300x200?text=${encodeURIComponent(dest.name)}`;
    
    const ratingHtml = dest.review_count > 0 
        ? `<div style="color: #ffc107; font-size: 0.9rem; margin: 8px 0;">
               ${'★'.repeat(Math.round(dest.avg_rating))}${'☆'.repeat(5-Math.round(dest.avg_rating))}
               <span style="color: #666; margin-left: 5px;">${dest.avg_rating} (${dest.review_count} reviews)</span>
           </div>`
        : '<div style="color: #999; font-style: italic; margin: 8px 0;">Not rated yet</div>';
    
    const description = dest.description && dest.description.length > 120 
        ? dest.description.substring(0, 120) + '...' 
        : (dest.description || 'No description available');
    
return `
    <div style="min-width: 280px; max-width: 320px; padding: 12px 16px; background: #fff; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
        <img src="${imageUrl}" 
             style="width: 100%; height: 180px; object-fit: cover; border-radius: 8px; margin-bottom: 10px;" 
             alt="${dest.name}">
        <h6 style="margin: 0 0 5px 0; font-size: 1.1rem; font-weight: bold; color: #333;">${dest.name}</h6>
        <div style="background: #f0f0f0; padding: 4px 10px; border-radius: 12px; display: inline-block; margin-bottom: 8px; font-size: 0.85rem;">
            <i class="fas ${dest.icon || 'fa-map-pin'}"></i> ${dest.category_name || 'General'}
        </div>
        ${ratingHtml}
        <p style="margin: 10px 0; color: #555; font-size: 0.9rem; line-height: 1.4;">${description}</p>
        <a href="/destination/${dest.id}" 
           class="btn btn-primary btn-sm" 
           style="display: inline-block; width: 100%; text-align: center; padding: 8px; background: linear-gradient(135deg, #132365ff 0%, #4b59a3ff 100%); color: white; text-decoration: none; border-radius: 6px; font-weight: 600; margin-top: 8px;">
            <i class="fas fa-info-circle"></i> View Details
        </a>
    </div>
`;

}

function showOnMap(lat, lng, destId) {
    if (!lat || !lng) return;
    
    map.setView([lat, lng], 15);
    document.getElementById('mapI').scrollIntoView({behavior: 'smooth'});
    
    setTimeout(() => {
        const dest = window.destinations.find(d => 
            Math.abs(d.latitude - lat) < 0.0001 && 
            Math.abs(d.longitude - lng) < 0.0001
        );
        
        if (dest && markersMap[dest.id]) {
            markersMap[dest.id].openPopup();
        }
    }, 500);
}