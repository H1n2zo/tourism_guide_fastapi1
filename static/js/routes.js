// Route management and display
let allRoutes = [];
let currentRoutingControl = null;

const transportIcons = {
    'jeepney': 'fa-bus',
    'taxi': 'fa-taxi',
    'bus': 'fa-bus-alt',
    'van': 'fa-shuttle-van',
    'tricycle': 'fa-motorcycle',
    'walking': 'fa-walking'
};

async function loadRoutes() {
    try {
        const response = await fetch('/api/routes');
        const data = await response.json();
        allRoutes = data.routes || [];
        displayRoutes(allRoutes);
    } catch (error) {
        console.error('Error loading routes:', error);
        document.getElementById('routesList').innerHTML = `
            <div class="no-routes">
                <i class="fas fa-exclamation-triangle fa-3x mb-3 text-warning"></i>
                <p>Unable to load routes. Please try again later.</p>
            </div>
        `;
    }
}

function displayRoutes(routes) {
    const container = document.getElementById('routesList');
    
    if (routes.length === 0) {
        container.innerHTML = `
            <div class="no-routes">
                <i class="fas fa-route fa-3x mb-3"></i>
                <p>No transportation routes found.</p>
                <small class="text-muted">Routes will be added by administrators.</small>
            </div>
        `;
        return;
    }

    let html = '';
    routes.forEach(route => {
        const icon = transportIcons[route.transport_mode] || 'fa-bus';
        const dbDistance = route.distance_km || 0;
        const dbTime = route.estimated_time_minutes || 0;
        const dbBaseFare = route.base_fare || 0;
        const dbFarePerKm = route.fare_per_km || 0;
        
        let totalFare = dbBaseFare;
        if (['taxi', 'van'].includes(route.transport_mode) && dbDistance > 0) {
            totalFare = dbBaseFare + (dbDistance * dbFarePerKm);
        }
        
        html += `
            <div class="route-card" onclick="showRouteOnMap(${route.id}, ${route.origin_id}, ${route.destination_id})">
                <div class="d-flex align-items-start">
                    <div class="transport-icon ${route.transport_mode}">
                        <i class="fas ${icon}"></i>
                    </div>
                    <div class="flex-grow-1">
                        <h5 class="mb-2">${route.route_name || 'Route'}</h5>
                        <p class="text-muted mb-2">
                            <strong>From:</strong> ${route.origin_name || 'N/A'} 
                            <i class="fas fa-arrow-right mx-2"></i> 
                            <strong>To:</strong> ${route.destination_name || 'N/A'}
                        </p>
                        <div class="mb-2">
                            <span class="route-info-badge badge-distance">
                                <i class="fas fa-road"></i> ${dbDistance > 0 ? dbDistance + ' km' : 'N/A'}
                            </span>
                            <span class="route-info-badge badge-time">
                                <i class="fas fa-clock"></i> ${dbTime > 0 ? dbTime + ' min' : 'N/A'}
                            </span>
                            <span class="route-info-badge badge-fare">
                                <i class="fas fa-money-bill-wave"></i> PHP ${totalFare.toFixed(2)}
                            </span>
                        </div>
                        ${route.description && route.description !== '0' ? `<p class="mb-0 small text-muted">${route.description}</p>` : ''}
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

function showRouteOnMap(routeId, originId, destinationId) {
    if (currentRoutingControl) {
        map.removeControl(currentRoutingControl);
    }

    document.querySelectorAll('.route-card').forEach(card => {
        card.classList.remove('selected');
    });
    event.currentTarget.classList.add('selected');
    
    const origin = destinationsMap[originId];
    const destination = destinationsMap[destinationId];
    
    if (!origin || !destination) {
        alert('Cannot display route - coordinates not available');
        return;
    }
    
    currentRoutingControl = L.Routing.control({
        waypoints: [
            L.latLng(origin.lat, origin.lng),
            L.latLng(destination.lat, destination.lng)
        ],
        routeWhileDragging: false,
        show: false,
        createMarker: function(i, waypoint, n) {
            return L.marker(waypoint.latLng, {
                icon: L.divIcon({
                    className: 'custom-route-marker',
                    html: `<div style="background: ${i === 0 ? '#28a745' : '#dc3545'}; color: white; padding: 8px 12px; border-radius: 8px; font-weight: bold; white-space: nowrap; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">${i === 0 ? 'Start: ' + origin.name : 'End: ' + destination.name}</div>`,
                    iconSize: [null, null],
                    iconAnchor: [0, 0]
                })
            });
        },
        lineOptions: {
            styles: [{color: '#667eea', opacity: 0.8, weight: 5}]
        }
    }).addTo(map);
    
    const bounds = L.latLngBounds([
        [origin.lat, origin.lng],
        [destination.lat, destination.lng]
    ]);
    map.fitBounds(bounds, { padding: [50, 50] });
    
    document.getElementById('mapI').scrollIntoView({behavior: 'smooth', block: 'center'});
}

function filterRoutes() {
    const destFilter = document.getElementById('destinationFilter').value;
    const transportFilter = document.getElementById('transportFilter').value;
    
    let filtered = allRoutes;
    
    if (destFilter) {
        filtered = filtered.filter(r => 
            r.origin_id == destFilter || r.destination_id == destFilter
        );
    }
    
    if (transportFilter) {
        filtered = filtered.filter(r => r.transport_mode === transportFilter);
    }
    
    displayRoutes(filtered);
}

function clearFilters() {
    document.getElementById('destinationFilter').value = '';
    document.getElementById('transportFilter').value = '';
    displayRoutes(allRoutes);
    
    if (currentRoutingControl) {
        map.removeControl(currentRoutingControl);
        currentRoutingControl = null;
    }
    
    document.querySelectorAll('.route-card').forEach(card => {
        card.classList.remove('selected');
    });
}