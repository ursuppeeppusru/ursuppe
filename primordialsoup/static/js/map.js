// Define position of map
const zoom = 6;
const center = [56.26904388487482, 10.755436652621228];

// Declaring map
const map = L.map('map', {center: center, zoom: zoom,
    // Stop zoom interferring with scroll on mobile
    dragging: !L.Browser.mobile,
    tap: !L.Browser.mobile,
});

// Tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Cluster settings
const clusterSettings = {
    iconCreateFunction: function (cluster) {
        const markers = cluster.getAllChildMarkers();
        const html = '<div class="circle"><p>' + markers.length + '</p></div>';
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
    maxClusterRadius: 30,
}

// Layer groups
const allEvents = L.markerClusterGroup(clusterSettings);
const upcomingEvents = L.featureGroup.subGroup(allEvents);
const currentEvents = L.featureGroup.subGroup(allEvents);
allEvents.addTo(map);

// Layer control 
const control = L.control.layers(null, null, { collapsed: false});
control.addOverlay(upcomingEvents, "Upcoming events");
control.addOverlay(currentEvents, "Current events");
control.addTo(map);
  
// Fetch JSON
const jsonUrl = '/events/json';
fetch(jsonUrl).then(response => response.json()).then(data => {
        data.event_submissions.forEach(event => {
            const id = event.calendar__id; 
            const image = event.image;
            const eventOpening = formatJsonDate(event.calendar__exhibition_opening);
            const latitude = parseFloat(event.calendar__latitude);
            const longitude = parseFloat(event.calendar__longitude);
            const marker = L.marker([latitude, longitude], {icon: soupIcon});

            marker.bindPopup(`<img style="border-radius: 50%;" src="/media/${image}">`);

            if (new Date(eventOpening) > new Date()) {
                upcomingEvents.addLayer(marker);
            } else {
                currentEvents.addLayer(marker);
            };
            
            marker.on('click', function() {
                showEventDetails(event);
            });

            upcomingEvents.addTo(map);
            currentEvents.addTo(map);
        });
    })
    .catch(error => {
        console.error('Error fetching data:', error);
});

// Formating JSON date for event details
function formatJsonDate(jsonDate) {
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
    const eventOpening = formatJsonDate(event.calendar__exhibition_opening);
    const eventEnd = formatJsonDate(event.calendar__exhibition_end);
    const vernissage = formatJsonDate(event.calendar__opening);
    const eventDetailsDiv = document.getElementById('event-details');
    const eventDetailBlankPlaceholder = document.getElementById('event-details-placeholder');
    const today = new Date().setHours(0,0,0,0);
    const twoWeeks = new Date(Date.now() + 12096e5).setHours(0,0,0,0);    
    
    if (new Date(eventOpening).getTime() == today) {
        eventStatus = "OPENING TODAY";
    } else if (new Date(eventOpening) < today && new Date(eventEnd) < twoWeeks) {
        eventStatus = "CLOSING SOON";
    } else if (new Date(eventOpening) < today) {
        eventStatus = "CURRENT";
    } else {
        eventStatus = "UPCOMING";
    };

    // Event Details card
    if (event.calendar__curators) {
        eventDetailsDiv.innerHTML = `
        <div class="row content events-list-card">
            <div class="col-4">
            <span class="event-detail-status-label">${eventStatus}</span>
                <p>${event.calendar__artists}</p>
                <a class="event-project-title-link" href="/events/${event.calendar__id}-${event.calendar__slug}">
                    <h2 class="text-uppercase is-large event_project_title">${event.calendar__project_title}</h2>
                </a>
                <br/>
                <p>Curated by ${event.calendar__curators}</p>
                <br/>
                <p><small>${event.calendar__event_type}</small></p>
                <br/>
            </div>
            <div class="col-4">
                <h4>${eventOpening} → ${eventEnd}</h4>
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
    } else {
        eventDetailsDiv.innerHTML = `
        <div class="row content events-list-card">
            <div class="col-4">
            <span class="event-detail-status-label">${eventStatus}</span>
                <p>${event.calendar__artists}</p>
                <a class="event-project-title-link" href="/events/${event.calendar__id}-${event.calendar__slug}">
                    <h2 class="text-uppercase is-large event_project_title">${event.calendar__project_title}</h2>
                </a>
                <br/>
                <p><small>${event.calendar__event_type}</small></p>
            </div>
            <div class="col-4">
                <h4>${eventOpening} → ${eventEnd}</h4>
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
    };
    
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

// Map view center of map and/or show all visible markers
L.Control.ViewAll = L.Control.extend({
    options: {
        position: 'topleft',
        forceSeparateButton: false,
    },

    onAdd: function(map) {
        const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
        const button = L.DomUtil.create('a', 'leaflet-view-all', container);
        button.title = 'Show all markers';
        button.innerHTML = `<a>&bigcirc; <br> &bigcirc; <br> &bigcirc;</a>`;       
        L.DomEvent.disableClickPropagation(button);
        L.DomEvent.on(button, 'click', function(){
            map.fitBounds(allEvents.getBounds());
            console.log(zoom);
        })

        return container;
    },

    onRemove: function (map) {
        // Nothing to do here
    },
});

L.control.ViewAll = function(options) {
    return new L.Control.ViewAll(options);
}

L.control.ViewAll({
}).addTo(map);