/*
 * Leaflet.Sleep from https://github.com/CliffCloud/Leaflet.Sleep 
 */

/*
 * Default Button (touch devices only)
 */

L.Control.SleepMapControl = L.Control.extend({

    initialize: function(opts){
        L.setOptions(this,opts);
    },
  
    options: {
        position: 'topright',
        prompt: 'disable map',
        styles: {
            'backgroundColor': 'white',
            'padding': '5px',
            'border': '2px solid gray'
        }
    },
  
    buildContainer: function(){
        var self = this;
        var container = L.DomUtil.create('p', 'sleep-button');
        var boundEvent = this._nonBoundEvent.bind(this);
        container.innerHTML = this.options.prompt;
        L.DomEvent.addListener(container, 'click', boundEvent);
        L.DomEvent.addListener(container, 'touchstart', boundEvent);
    
        Object.keys(this.options.styles).map(function(key) {
            container.style[key] = self.options.styles[key];
        });
  
        return (this._container = container);
    },
  
    onAdd: function () {
        return this._container || this.buildContainer();
    },

    _nonBoundEvent: function(e) {
        L.DomEvent.stop(e);
        if (this._map) this._map.sleep._sleepMap();
        return false;
    }
    
});

L.Control.sleepMapControl = function(){
    return new L.Control.SleepMapControl();
};


/*
 * The Sleep Handler
 */

L.Map.mergeOptions({
    sleep: true,
    sleepTime: 750,
    wakeTime: 750,
    wakeMessageTouch: 'Touch to Wake',
    sleepNote: true,
    hoverToWake: true,
    sleepOpacity:.7,
    sleepButton: L.Control.sleepMapControl
});

L.Map.Sleep = L.Handler.extend({

    addHooks: function () {
        var self = this;
        this.sleepNote = L.DomUtil.create('p', 'sleep-note', this._map._container);
        this._enterTimeout = null;
        this._exitTimeout = null;
  
        /*
        * If the device has only a touchscreen we will never get
        * a mouseout event, so we add an extra button to put the map
        * back to sleep manually.
        *
        * a custom control/button can be provided by the user
        * with the map's `sleepButton` option
        */
        this._sleepButton = this._map.options.sleepButton();
    
        if (this._map.tap) {
            this._map.addControl(this._sleepButton);
        }
    
        var mapStyle = this._map._container.style;
        mapStyle.WebkitTransition += 'opacity .5s';
        mapStyle.MozTransition += 'opacity .5s';
    
        this._setSleepNoteStyle();
        this._sleepMap();
    },
  
    removeHooks: function () {
        if (!this._map.scrollWheelZoom.enabled()){
            this._map.scrollWheelZoom.enable();
        }
        if (this._map.tap) {
            this._map.touchZoom.enable();
            this._map.dragging.enable();
            this._map.tap.enable();
        }
        L.DomUtil.setOpacity( this._map._container, 1);
        L.DomUtil.setOpacity( this.sleepNote, 0);
        this._removeSleepingListeners();
        this._removeAwakeListeners();
    },
  
    _setSleepNoteStyle: function() {
        var noteString = '';
        var style = this.sleepNote.style;
    
        if(this._map.tap) {
            noteString = this._map.options.wakeMessageTouch;
        } else if (this._map.options.wakeMessage) {
            noteString = this._map.options.wakeMessage;
        } else if (this._map.options.hoverToWake) {
            noteString = 'click or hover to wake';
        } else {
            noteString = 'click to wake';
        }
    
      if( this._map.options.sleepNote ){
        this.sleepNote.innerHTML = noteString;
        style.pointerEvents = 'none';
        style.maxWidth = '150px';
        style.transitionDuration = '.2s';
        style.zIndex = 5000;
        style.margin = 'auto';
        style.textAlign = 'center';
        style.borderRadius = '4px';
        style.top = '50%';
        style.position = 'relative';
        style.padding = '5px';
        style.border = 'solid 2px black';
        style.background = 'white';
  
            if(this._map.options.sleepNoteStyle) {
                var noteStyleOverrides = this._map.options.sleepNoteStyle;
                Object.keys(noteStyleOverrides).map(function(key) {
                    style[key] = noteStyleOverrides[key];
                });
            }
        }
    },
  
    _wakeMap: function (e) {
        this._stopWaiting();
        this._map.scrollWheelZoom.enable();
        if (this._map.tap) {
            this._map.touchZoom.enable();
            this._map.dragging.enable();
            this._map.addControl(this._sleepButton);
        }
        L.DomUtil.setOpacity( this._map._container, 1);
        this.sleepNote.style.opacity = 0;
        this._addAwakeListeners();
    },
  
    _sleepMap: function () {
        this._stopWaiting();
        this._map.scrollWheelZoom.disable();
    
        if (this._map.tap) {
            this._map.touchZoom.disable();
            this._map.dragging.disable();
            this._map.tap.disable();
            this._map.removeControl(this._sleepButton);
        }
  
        L.DomUtil.setOpacity( this._map._container, this._map.options.sleepOpacity);
        this.sleepNote.style.opacity = this._map.options.sleepNoteStyle && this._map.options.sleepNoteStyle.opacity ? this._map.options.sleepNoteStyle.opacity : .6;
        this._addSleepingListeners();
    },
  
    _wakePending: function () {
        this._map.once('mousedown', this._wakeMap, this);
        if (this._map.options.hoverToWake){
            var self = this;
            this._map.once('mouseout', this._sleepMap, this);
            self._enterTimeout = setTimeout(function(){
                self._map.off('mouseout', self._sleepMap, self);
                self._wakeMap();
            } , self._map.options.wakeTime);
        }
    },
  
    _sleepPending: function () {
        var self = this;
        self._map.once('mouseover', self._wakeMap, self);
        self._exitTimeout = setTimeout(function(){
            self._map.off('mouseover', self._wakeMap, self);
            self._sleepMap();
        } , self._map.options.sleepTime);
    },
  
    _addSleepingListeners: function(){
        this._map.once('mouseover', this._wakePending, this);
        this._map.tap &&
            this._map.once('click', this._wakeMap, this);
    },
  
    _addAwakeListeners: function(){
        this._map.once('mouseout', this._sleepPending, this);
    },
  
    _removeSleepingListeners: function(){
        this._map.options.hoverToWake &&
            this._map.off('mouseover', this._wakePending, this);
        this._map.off('mousedown', this._wakeMap, this);
        this._map.tap &&
            this._map.off('click', this._wakeMap, this);
    },
  
    _removeAwakeListeners: function(){
        this._map.off('mouseout', this._sleepPending, this);
    },
  
    _stopWaiting: function () {
        this._removeSleepingListeners();
        this._removeAwakeListeners();
        var self = this;
        if(this._enterTimeout) clearTimeout(self._enterTimeout);
        if(this._exitTimeout) clearTimeout(self._exitTimeout);
        this._enterTimeout = null;
        this._exitTimeout = null;
        }
  });
  
  L.Map.addInitHook('addHandler', 'sleep', L.Map.Sleep);

/*
 * Event Map View
 */


// Define position of map
const zoom = 6;
const center = [56.26904388487482, 10.755436652621228];

// Declaring map
const map = L.map('map', {center: center, zoom: zoom,
    // Stop zoom interferring witrh scroll on mobile
    dragging: !L.Browser.mobile,
    tap: !L.Browser.mobile,

    // false if you want an unruly map
    sleep: true,

    // time(ms) until map sleeps on mouseout
    sleepTime: 750,

    // time(ms) until map wakes on mouseover
    wakeTime: 750,

    // should the user receive wake instructions?
    sleepNote: false,

    // should hovering wake the map? (non-touch devices only)
    hoverToWake: false,

    // a message to inform users about waking the map
    wakeMessage: '',

    // a constructor for a control button
    sleepButton: L.Control.sleepMapControl,

    // opacity for the sleeping map
    sleepOpacity: .8
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
    maxClusterRadius: 30,
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
    const eventOpening = formatJsonDate(event.calendar__exhibition_opening);
    const eventEnd = formatJsonDate(event.calendar__exhibition_end);
    const vernissage = formatJsonDate(event.calendar__opening);
    const eventDetailsDiv = document.getElementById('event-details');
    const eventDetailBlankPlaceholder = document.getElementById('event-details-placeholder');
    if (new Date(eventEnd) <= new Date(Date.now() + 12096e5)) {
        eventStatus = "CLOSING SOON";
    } else if (new Date(eventOpening) < new Date()) {
        eventStatus = "CURRENT";
    } else {
        eventStatus = "UPCOMING";
    };

    // Event Details card
    if (typeof event.calendar__curators !== 'undefined') {
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