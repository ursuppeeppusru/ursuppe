let map = L.map('map').setView([56.26904388487482, 10.755436652621228], 7);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);


// Improvement: adjust spiderify to exact coordinates
// Improvement: Hide cluster icon when clicked
let markers = L.markerClusterGroup({
    iconCreateFunction: function (cluster) {
        var markers = cluster.getAllChildMarkers();
        var html = '<div class="circle">' + markers.length + '</div>';
        return L.divIcon({ html: html, className: 'mycluster', iconSize: L.point(0, 40) });
    },
    spiderfyOnMaxZoom: true, showCoverageOnHover: false, zoomToBoundsOnClick: true,
    maxClusterRadius: 60,
    
});

const jsonUrl = 'http://127.0.0.1:8000/events/json';

// Fetch data from JSONPlaceholder API
fetch(jsonUrl)
    .then(response => response.json())
    .then(data => {
        // Loop through the data
        data.event_submissions.forEach(event => {
            let id = event.id;
            let eventImageId = event.calendar_id;
            let latitude = parseFloat(event.latitude);
            let longitude = parseFloat(event.longitude);
//            console.log('Event ID: ' + id + '\n' + 'Event Image ID: ' + eventImageId);
//            console.log('latitude: ' + latitude + 'longitude: ' + longitude)

            let marker = L.marker([latitude, longitude], {icon: soupIcon});
            marker.bindPopup(`<img style="border-radius: 50%;" src="https://kunsten.nu/wp-content/uploads/2024/03/gaza-18-904x603.jpg">`);
            // 'src' should be event_submission_images.calendar_id corresponding to event_submissions.id
            // How can this be done....... 
            
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


// Improvement: Click or hover to wake map - see: http://cliffcloud.github.io/Leaflet.Sleep/#summary 
// map.on('click', function () {
//     if (map.scrollWheelZoom.enabled()) {
//         map.scrollWheelZoom.disable();
//     }
//     else {
//         map.scrollWheelZoom.enable();
//     }
// });

// Improvement: get EventDetails based on cards. Kan man bruge django templating i js?
function showEventDetails(event) {
    const eventDetailsDiv = document.getElementById('eventDetails');
    eventDetailsDiv.innerHTML = `
        <div class="row content events-list-card">
            <div class="col-4 ">
                <p>${event.artists}</p>
                <a class="event-project-title-link" href="/events/${event.id}-${event.slug}">
                    <h2 class="text-uppercase is-large event_project_title">${event.project_title}</h2>
                </a>
                <img class="event-submission-image-list" src="{event.images.all.0.image.url}" alt="{event.images.all.0.image.caption}">
                <br/>
                <p>Curated by ${event.curators}</p>
                <br/>
                <p><small>${event.event_type}</small></p>
            </div>
            <div class="col-4">
                <h4>${event.exhibition_opening} → ${event.exhibition_end}</h4>
                <br/>
                <p>Weekly opening hours:</p>
                <p>${event.opening_hours}</p>
                <br/>
                <h4>Opening/vernissage: ${event.opening}</h4>
                <br/>
                <p>Opening hours for opening/vernissage:</p>
                <p>${event.opening_hours_for_opening_date}</p>
            </div>
            <div class="col-4">
                <h4>${event.location}</h4>
                <p>${event.location_address}</p>
                <br/>
                <p><small><a href="${event.link_to_location}" target="_blank">${event.link_to_location}</a></small></p>
                <br/>
                <p><small>Admission:</small></p>
                <p><small>${event.admission}</small></p>
            </div>
        </div>
    `;
    eventDetailsDiv.style.display = 'block';
}

// Event listener for closing the post details
map.on('popupclose', function() {
    var eventDetailsDiv = document.getElementById('eventDetails');
    eventDetailsDiv.style.display = 'none';
});

// marker icons
const soupIcon = L.divIcon({
    className: 'soup',
    html: '<div class="circle"></div>',
    iconAnchor:   [20, 20], // point of the icon which will correspond to marker's location
    popupAnchor:  [0, 0] // point from which the popup should open relative to the iconAnchor
});


// html id: event-detail-map 
const eventDetailMap  = L.map('eventDetailMap').setView([56.26904388487482, 10.755436652621228], 12);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(eventDetailMap);
