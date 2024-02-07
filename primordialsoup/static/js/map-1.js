var map = L.map('map').setView([56.26904388487482, 10.755436652621228], 7);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// fetching locations and creating markers from /events/json
var jsonUrl = ("http://127.0.0.1:8000/events/json");


fetch(jsonUrl).then(function (response) {
    return response.json();
}).then (function (obj) {
    for (var i = 0; i < obj.event_submissions_json.length; i ++) {
        const eventId = (obj.event_submissions_json[i].id);
        var eventLat = (obj.event_submissions_json[i].latitude);
        var eventLng = (obj.event_submissions_json[i].longitude);
        var location = (obj.event_submissions_json[i].location);
        var project = (obj.event_submissions_json[i].project_title);
        var locationAddress = (obj.event_submissions_json[i].location_address);
        
        // marker
        const eventMarker = L.marker([eventLat, eventLng]).addTo(map);
        eventMarker.bindPopup(
            "<b>" + project + "</b></br> " + 
            location + "</br>" + 
            locationAddress + "</br>" +
            "ID: " + eventId
            );
    }
    console.log(obj.event_submissions_json.length + " markers loaded.");
}).catch(function (error) {
    console.error('Something went wrong with retrieving the event!');
    console.error(error);
});

var testMarker = L.marker([54.9685620000, 11.5619980000]).addTo(map);
testMarker.bindPopup("Let's make this responsive!").on('click', function(e) {
    console.log(e.latlng);
});





// er det bedst at kalde JSON to gange eller pushe til array udenfor fetch-funktion

// trigger html event based on leflet markers
// when marker is clicked, console.log(eventId)
// use eventId to filter div-containers in html
// display corresponging div-container
