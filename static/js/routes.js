// routes.js - Complete Route Management System
// Handles route display, filtering, and map visualization

let allRoutes = [];
let currentRoutingControl = null;

// Transport mode icon mapping
const transportIcons = {
    'jeepney': 'fa-bus',
    'taxi': 'fa-taxi',
    'bus': 'fa-bus-alt',
    'van': 'fa-shuttle-van',
    'tricycle': 'fa-motorcycle',
    'walking': 'fa-walking'
};

// Transport mode colors
const transportColors = {
    'jeepney': '#ff6b6b',
    'taxi': '#feca57',
    'bus': '#48dbfb',
    'van': '#1dd1a1',
    'tricycle': '#ee5a6f',
    'walking': '#54a0ff'
};

/**
 * Load routes from API
 */
async function loadRoutes() {
    try {
        const response = await fetch('/api/routes');
        
        if (!response.ok) {
            throw new Error('Failed to load routes');
        }
        
        const data = await response.json();
        allRoutes = data.routes || [];
        
        console.log('Routes loaded:', allRoutes.length);
        displayRoutes(allRoutes);
        
    } catch (error) {
        console.error('Error loading routes:', error);
        showRoutesError('Unable to load routes. Please try again later.');
    }
}

/**
 * Display routes as cards
 */
function displayRoutes(routes) {
    const container = document.getElementById('routesList');
    
    if (!container) {
        console.error('Routes container not found');
        return;
    }
    
    if (routes.length === 0) {
        container.innerHTML = `
            
                
                No transportation routes found.
                Routes will be added by administrators.
            
        `;
        return;
    }

    let html = '';
    routes.forEach(route => {
        const icon = transportIcons[route.transport_mode] || 'fa-bus';
        const color = transportColors[route.transport_mode] || '#999';
        
        // CRITICAL FIX: Proper fare calculation with null checks
        const dbDistance = parseFloat(route.distance_km) || 0;
        const dbTime = parseInt(route.estimated_time_minutes) || 0;
        const dbBaseFare = parseFloat(route.base_fare) || 0;
        const dbFarePerKm = parseFloat(route.fare_per_km) || 0;
        
        let totalFare = dbBaseFare;
        if (['taxi', 'van'].includes(route.transport_mode) && dbDistance > 0 && dbFarePerKm > 0) {
            totalFare = dbBaseFare + (dbDistance * dbFarePerKm);
        }
        
        // Format display values
        const distanceDisplay = dbDistance > 0 ? `${dbDistance.toFixed(1)} km` : 'N/A';
        const timeDisplay = dbTime > 0 ? `${dbTime} min` : 'N/A';
        const fareDisplay = totalFare > 0 ? `PHP ${totalFare.toFixed(2)}` : 'N/A';
        
        html += `
            
                
                    
                        
                    
                    
                        ${route.route_name || 'Route'}
                        
                            From: ${route.origin_name || 'N/A'} 
                             
                            To: ${route.destination_name || 'N/A'}
                        
                        
                            
                                 ${distanceDisplay}
                            
                            
                                 ${timeDisplay}
                            
                            
                                 ${fareDisplay}
                            
                        
                        ${route.description && route.description !== '0' && route.description !== 'null' ? 
                            ` ${route.description}` 
                            : ''}
                    
                
            
        `;
    });
    
    container.innerHTML = html;
}

/**
 * Show error message in routes container
 */
function showRoutesError(message) {
    const container = document.getElementById('routesList');
    if (container) {
        container.innerHTML = `
            <div class="no-routes">
                <i class="fas fa-exclamation-triangle fa-3x mb-3 text-warning"></i>
                <p class="text-danger">${message}</p>
                <button class="btn btn-primary btn-sm" onclick="loadRoutes()">
                    <i class="fas fa-redo"></i> Try Again
                </button>
            </div>
        `;
    }
}

/**
 * Show route on map using Leaflet Routing Machine
 */
function showRouteOnMap(routeId, originId, destinationId) {
    // Remove previous routing control
    if (currentRoutingControl) {
        map.removeControl(currentRoutingControl);
        currentRoutingControl = null;
    }

    // Remove selected class from all route cards
    document.querySelectorAll('.route-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Add selected class to clicked card
    if (event && event.currentTarget) {
        event.currentTarget.classList.add('selected');
    }
    
    // CRITICAL FIX: Validate destinationsMap exists
    if (!destinationsMap || Object.keys(destinationsMap).length === 0) {
        console.error('destinationsMap not initialized');
        alert('Map data not loaded. Please refresh the page.');
        return;
    }
    
    // Get origin and destination coordinates
    const origin = destinationsMap[originId];
    const destination = destinationsMap[destinationId];
    
    // CRITICAL FIX: Better error handling
    if (!origin || !destination) {
        console.error('Missing coordinates:', { 
            originId, 
            destinationId, 
            origin, 
            destination,
            availableDestinations: Object.keys(destinationsMap)
        });
        alert('Cannot display route - location coordinates not available');
        return;
    }
    
    // Validate coordinates are valid numbers
    if (!origin.lat || !origin.lng || !destination.lat || !destination.lng) {
        alert('Invalid coordinates for one or both locations');
        return;
    }
    
    console.log('Drawing route:', {
        from: origin.name,
        to: destination.name,
        originCoords: [origin.lat, origin.lng],
        destCoords: [destination.lat, destination.lng]
    });
    
    // Create routing control
    currentRoutingControl = L.Routing.control({
        waypoints: [
            L.latLng(origin.lat, origin.lng),
            L.latLng(destination.lat, destination.lng)
        ],
        routeWhileDragging: false,
        show: false, // Hide the instruction panel
        addWaypoints: false,
        draggableWaypoints: false,
        createMarker: function(i, waypoint, n) {
            // Custom markers for start and end
            return L.marker(waypoint.latLng, {
                icon: L.divIcon({
                    className: 'custom-route-marker',
                    html: `<div style="
                        background: ${i === 0 ? '#28a745' : '#dc3545'}; 
                        color: white; 
                        padding: 8px 12px; 
                        border-radius: 8px; 
                        font-weight: bold; 
                        white-space: nowrap; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                        font-size: 0.9rem;
                    ">
                        ${i === 0 ? '🚩 ' + origin.name : '🏁 ' + destination.name}
                    </div>`,
                    iconSize: [null, null],
                    iconAnchor: [0, 0]
                })
            });
        },
        lineOptions: {
            styles: [{
                color: '#667eea', 
                opacity: 0.8, 
                weight: 6
            }]
        }
    }).addTo(map);
    
    // Fit map to show entire route
    const bounds = L.latLngBounds([
        [origin.lat, origin.lng],
        [destination.lat, destination.lng]
    ]);
    map.fitBounds(bounds, { 
        padding: [50, 50],
        maxZoom: 14
    });
    
    // Scroll to map
    document.getElementById('mapI').scrollIntoView({
        behavior: 'smooth', 
        block: 'center'
    });
}

/**
 * Filter routes by destination and transport mode
 */
function filterRoutes() {
    const destFilter = document.getElementById('destinationFilter').value;
    const transportFilter = document.getElementById('transportFilter').value;
    
    let filtered = allRoutes;
    
    // Filter by destination
    if (destFilter) {
        filtered = filtered.filter(r => 
            r.origin_id == destFilter || r.destination_id == destFilter
        );
    }
    
    // Filter by transport mode
    if (transportFilter) {
        filtered = filtered.filter(r => r.transport_mode === transportFilter);
    }
    
    console.log(`Filtered routes: ${filtered.length} of ${allRoutes.length}`);
    displayRoutes(filtered);
}

/**
 * Clear all filters and reset view
 */
function clearFilters() {
    // Reset filter dropdowns
    const destFilter = document.getElementById('destinationFilter');
    const transportFilter = document.getElementById('transportFilter');
    
    if (destFilter) destFilter.value = '';
    if (transportFilter) transportFilter.value = '';
    
    // Display all routes
    displayRoutes(allRoutes);
    
    // Remove routing control from map
    if (currentRoutingControl) {
        map.removeControl(currentRoutingControl);
        currentRoutingControl = null;
    }
    
    // Remove selected state from route cards
    document.querySelectorAll('.route-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    console.log('Filters cleared');
}

/**
 * Get route statistics
 */
function getRouteStats() {
    if (allRoutes.length === 0) return null;
    
    const stats = {
        total: allRoutes.length,
        byMode: {},
        totalDistance: 0,
        avgDistance: 0
    };
    
    allRoutes.forEach(route => {
        // Count by transport mode
        const mode = route.transport_mode;
        stats.byMode[mode] = (stats.byMode[mode] || 0) + 1;
        
        // Sum distances
        if (route.distance_km) {
            stats.totalDistance += parseFloat(route.distance_km);
        }
    });
    
    stats.avgDistance = stats.total > 0 ? (stats.totalDistance / stats.total).toFixed(2) : 0;
    
    return stats;
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        if (document.getElementById('routesList')) {
            loadRoutes();
        }
    });
} else {
    // DOM already loaded
    if (document.getElementById('routesList')) {
        loadRoutes();
    }
}