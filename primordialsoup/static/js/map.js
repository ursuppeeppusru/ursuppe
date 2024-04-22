// Declaring map
const map = L.map('map', {
    center: [56.26904388487482, 10.755436652621228],
    zoom: 6,
    dragging: !L.Browser.mobile,
    tap: !L.Browser.mobile
});

// Tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Clustering
const markers = L.markerClusterGroup({
    iconCreateFunction: function (cluster) {
        var markers = cluster.getAllChildMarkers();
        var html = '<div class="circle">' + markers.length + '</div>';
        return L.divIcon({ 
            html: html,
            className: 'mycluster', 
            iconSize: L.point(0, 40),
            iconAnchor: [20, 20],
         });
    },
    spiderfyOnMaxZoom: true,
    showCoverageOnHover: false, 
    zoomToBoundsOnClick: true,
    maxClusterRadius: 60,
});

// Fetch JSON
const jsonUrl = '/events/json';
fetch(jsonUrl).then(response => response.json()).then(data => {
        // Loop through the data
        data.event_submissions.forEach(event => {
            const id = event.calendar__id; 
            const image = event.image;
            const latitude = parseFloat(event.calendar__latitude);
            const longitude = parseFloat(event.calendar__longitude);
            const marker = L.marker([latitude, longitude], {icon: soupIcon});
            
            // Image as popup
            marker.bindPopup(`<img style="border-radius: 50%;" src="/media/${image}">`);
            
            // Add marker to the markwer cluster group
            markers.addLayer(marker);

            // Event listener for marker click
            marker.on('click', function() {
                showEventDetails(event);
            });

            // Add marker cluster group to the map
            map.addLayer(markers);
        });
    })
    .catch(error => {
        console.error('Error fetching data:', error);
});

// Formating JSON date for event details
const formatJsonDate = (jsonDate) => {
    const date = new Date(jsonDate);
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    };
    const formattedDate = date.toLocaleDateString('en-US', options);
    return formattedDate;
};

// Show event details when marker is selected
function showEventDetails(event) {
    const exhibitionOpening = formatJsonDate(event.calendar__exhibition_opening);
    const exhibitionEnd = formatJsonDate(event.calendar__exhibition_end);
    const vernissage = formatJsonDate(event.calendar__opening);
    const eventDetailsDiv = document.getElementById('event-details');
    const eventDetailBlankPlaceholder = document.getElementById('event-details-placeholder');
    
    // Event Details 'card'
    eventDetailsDiv.innerHTML = `
        <div class="row content events-list-card">
            <div class="col-4">
                <p>${event.calendar__artists}</p>
                <a class="event-project-title-link" href="/events/${event.calendar__id}-${event.calendar__slug}">
                    <h2 class="text-uppercase is-large event_project_title">${event.calendar__project_title}</h2>
                </a>
                <br/>
                <p>Curated by ${event.calendar__curators}</p>
                <br/>
                <p><small>${event.calendar__event_type}</small></p>
            </div>
            <div class="col-4">
                <h4>${exhibitionOpening} → ${exhibitionEnd}</h4>
                <br/>
                <p>${event.calendar__opening_hours}</p>
                <br/>
                <h4>Opening/Vernissage: </h4>
                <br/>
                <p>${vernissage}, ${event.calendar__opening_hours_for_opening_date}</p>
                <br/>
            </div>
            <div class="col-4">
                <h4>${event.calendar__location}</h4>
                <p>${event.calendar__location_address}</p>
                <br/>
                <p><small><a href="${event.calendar__link_to_location}" target="_blank">${event.calendar__link_to_location}</a></small></p>
                <br/>
                <p><small>Admission: ${event.calendar__admission}</small></p>
            </div>
        </div>`;
        
    // Toggle display
    eventDetailsDiv.style.display = 'block';
    eventDetailBlankPlaceholder.style.display = 'none';
};

// Hide event details when marker is deselected
map.on('popupclose', function() {
    const eventDetailsDiv = document.getElementById('event-details');
    const eventDetailBlankPlaceholder = document.getElementById('event-details-placeholder');

    // Toggle display
    eventDetailsDiv.style.display = 'none';
    eventDetailBlankPlaceholder.style.display = 'block';
});

// Marker and cluster icon is defined in CSS
const soupIcon = L.divIcon({
    className: 'soup',
    html: '<div class="circle"></div>',
    iconAnchor:   [20, 20], 
    popupAnchor:  [0, -40] 
});