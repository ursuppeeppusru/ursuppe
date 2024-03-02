// Initialize Leaflet map
var map = L.map('map').setView([56.26904388487482, 10.755436652621228], 7);

// Add base map layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Create a marker cluster group
var markers = L.markerClusterGroup({
    spiderfyOnMaxZoom: false,
    showCoverOnHover: false,
    zoomToBoundsOnClick: false
});


// // Click or hover to wake map - see: http://cliffcloud.github.io/Leaflet.Sleep/#summary 
// map.on('click', function () {
//     if (map.scrollWheelZoom.enabled()) {
//         map.scrollWheelZoom.disable();
//     }
//     else {
//         map.scrollWheelZoom.enable();
//     }
// });



const jsonUrl = 'http://127.0.0.1:8000/events/json';

// Fetch data from JSONPlaceholder API
fetch(jsonUrl)
    .then(response => response.json())
    .then(data => {
        // Loop through the data
        data.event_submissions_json.forEach(event => {
            // Extract necessary information
            var id = event.id;
            var latitude = parseFloat(event.latitude);
            var longitude = parseFloat(event.longitude);

            // Create marker
            console.log('latitude: ' + latitude + 'longitude: ' + longitude)
            var marker = L.marker([latitude, longitude], {icon: soupIcon}).addTo(map);
            marker.bindPopup(`Event ID: ${id}`);

            // Add marker to the marker cluster group
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

// Function to show event details
function showEventDetails(event) {
    // Hide all event details divs
    var eventDetailsDiv = document.getElementById('eventDetails');
    eventDetailsDiv.innerHTML = `
    <div class="row content">
    <div class="col-4">
    <br/>
    <br/>
        <h4>${event.location }</h4>
        <p>${event.location_address}</p>
        <br/>
        <p><small><a href="${event.link_to_location}" target="_blank"> ${event.link_to_location }</a></small></p>
    </div>
    <div class="col-4 text-center">
    <br/>
    <br/>
        <p>${event.artists}</p>
        <a class="event_project_title_link" href="{% url 'event_detail' event_id=submission.id event_project_title=submission.slug %}">
            <h2 class="text-uppercase is-large event_project_title">${event.project_title }</h2>
            <img class="event-submission-image-list" src="{{ submission.images.all.0.image.url }}" alt="{{ submission.images.all.0.image.caption }}">
        </a>
        <br/>
        <p>Curated by ${event.curators}</p>
        <br/>
        <p><small>${event.event_type }</small></p>
    </div>
    <div class="col-4 text-right">
    <br/>
    <br/>
        <h4>${event.exhibition_opening} – ${event.exhibition_end}</h4>
        <br/>
        <p>Opening hours:</p>
        <p>${event.opening_hours}</p>
        <br/>
        <p><small>Admission:</small></p>
        <p><small>${event.admission }</small></p>
        </div>
        </div>
        <hr/>
    `;
    eventDetailsDiv.style.display = 'block';
}

// Event listener for closing the post details
map.on('popupclose', function() {
    var eventDetailsDiv = document.getElementById('eventDetails');
    eventDetailsDiv.style.display = 'none';
});


// marker icons
const soupIcon = L.icon({
    iconUrl: '../media/images/icons/circle.png',
    iconSize:     [, 40], // size of the icon
    iconAnchor:   [20, 8], // point of the icon which will correspond to marker's location
    popupAnchor:  [0, 0] // point from which the popup should open relative to the iconAnchor
});