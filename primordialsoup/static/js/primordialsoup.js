/* realtime time */
function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('time').innerHTML =
    h + ":" + m + ":" + s;
    var t = setTimeout(startTime, 500);
}

function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}


/* darkmode */
const darkBtn = document.querySelector('.darkmode-btn');
const bodyEl = document.querySelector('body');

const darkMode = () => {
    bodyEl.classList.toggle('dark')
}

darkBtn.addEventListener('click', () => {
    setDarkMode = localStorage.getItem('dark');

    if(setDarkMode !== "on") {
        darkMode();
        setDarkMode = localStorage.setItem('dark', 'on');
    } else {
        darkMode();
        setDarkMode = localStorage.setItem('dark', null);
    }
});

let setDarkMode = localStorage.getItem('dark');

if(setDarkMode === 'on') {
    darkMode();
}

/* ICS file generator */
/**
* Create and download a file on click
* @params {string} filename - The name of the file with the ending
* @params {string} filebody - The contents of the file
*/
function download(filename, fileBody) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(fileBody));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}


/**
* Returns a date/time in ICS format
* @params {Object} dateTime - A date object you want to get the ICS format for.
* @returns {string} String with the date in ICS format
*/
function convertToICSDate(dateTime) {
    const year = dateTime.getFullYear().toString();
    const month = (dateTime.getMonth() + 1) < 10 ? "0" + (dateTime.getMonth() + 1).toString() : (dateTime.getMonth() + 1).toString();
    const day = dateTime.getDate() < 10 ? "0" + dateTime.getDate().toString() : dateTime.getDate().toString();
    const hours = dateTime.getHours() < 10 ? "0" + dateTime.getHours().toString() : dateTime.getHours().toString();
    const minutes = dateTime.getMinutes() < 10 ? "0" +dateTime.getMinutes().toString() : dateTime.getMinutes().toString();

    return year + month + day + "T" + hours + minutes + "00";
}

/**
* Creates and downloads an ICS file
* @params {string} timeZone - In the format America/New_York
* @params {object} startTime - Vaild JS Date object in the event timezone
* @params {object} endTime - Vaild JS Date object in the event timezone
* @params {string} title
* @params {string} description
* @params {string} venueName
* @params {string} address
*/
function createDownloadICSFile(timezone, startTime, endTime, title, description, venueName, address) {
  const icsBody = 'BEGIN:VCALENDAR\n' +
  'VERSION:2.0\n' +
  'PRODID:Calendar\n' +
  'CALSCALE:GREGORIAN\n' +
  'METHOD:PUBLISH\n' +
  'BEGIN:VTIMEZONE\n' +
  'TZID:' + timezone + '\n' +
  'END:VTIMEZONE\n' +
  'BEGIN:VEVENT\n' +
  'SUMMARY:' + title + '\n' +
  'UID:@Default\n' +
  'SEQUENCE:0\n' +
  'STATUS:CONFIRMED\n' +
  'TRANSP:TRANSPARENT\n' +
  'DTSTART;TZID=' + timezone + ':' + convertToICSDate(startTime) + '\n' +
  'DTEND;TZID=' + timezone + ':' + convertToICSDate(endTime)+ '\n' +
  'DTSTAMP:'+ convertToICSDate(new Date()) + '\n' +
  'LOCATION:' + venueName + ' (' + address + ')\n' +
  'DESCRIPTION:' + description + '\n' +
  'END:VEVENT\n' +
  'END:VCALENDAR\n';

  download(title + '.ics', icsBody);
}

/* index horisontal sliders */

// Cache DOM elements
var eventsRow = document.getElementById('events-index-row');
var buttonOne = document.getElementById('slideOne');
var backOne = document.getElementById('slideBackOne');
var buttonTwo = document.getElementById('slideTwo');
var backTwo = document.getElementById('slideBackTwo');
var buttonThree = document.getElementById('slideThree');
var backThree = document.getElementById('slideBackThree');

// Calculate width once
var width = eventsRow.offsetWidth - 50;

// Consolidated event handler function
function setupSliderEvents(button, back, containerId) {
    button.onclick = function () {
        var container = document.getElementById(containerId);
        smoothScroll(container, 'right', width);
    };

    back.onclick = function () {
        var container = document.getElementById(containerId);
        smoothScroll(container, 'left', width);
    };
}

// Setup event listeners
setupSliderEvents(buttonOne, backOne, 'scroll-containerOne');
setupSliderEvents(buttonTwo, backTwo, 'scroll-containerTwo');
setupSliderEvents(buttonThree, backThree, 'scroll-containerThree');

// Easing function
function easeInOutQuad(t) {
    return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
}

// Smooth scroll function
function smoothScroll(element, direction, distance) {
    var start = element.scrollLeft;
    var startTime = performance.now();

    function scroll(time) {
        var elapsed = time - startTime;
        var progress = Math.min(elapsed / 500, 1); // Duration: 500ms

        if (direction === 'left') {
            element.scrollLeft = start - (distance * easeInOutQuad(progress));
        } else {
            element.scrollLeft = start + (distance * easeInOutQuad(progress));
        }

        if (progress < 1) {
            requestAnimationFrame(scroll);
        }
    }

    requestAnimationFrame(scroll);
}

/* index archive selector */
document.addEventListener("DOMContentLoaded", function() {
    const tabLinks = document.querySelectorAll(".tab-link");
    const imageContainers = document.querySelectorAll(".image-container-list");
    let currentIndex = 0;
    let timer; 

    // Function to show image container based on index
    function showImageByIndex(index) {
        tabLinks.forEach(function(link) {
            link.classList.remove("active");
        });
        tabLinks[index].classList.add("active");

        imageContainers.forEach(function(container) {
            container.classList.remove("active");
        });
        imageContainers[index].classList.add("active");
    }

    // Function to switch to the next tab and image container
    function switchToNextImage() {
        currentIndex = (currentIndex + 1) % tabLinks.length; // Increment index and wrap around
        showImageByIndex(currentIndex);
    }

    // Add mouseover event listener to tab links
    tabLinks.forEach(function(link, index) {
        link.addEventListener("mouseover", function(e) {
            e.preventDefault();
            currentIndex = index; // Update current index when mouseover occurs
            showImageByIndex(currentIndex);
        });
    });

    // Start the timer to switch images automatically every 5 seconds
    timer = setInterval(switchToNextImage, 5000);

    // Stop the timer when mouseover occurs on tab links
    tabLinks.forEach(function(link) {
        link.addEventListener("mouseover", function() {
            clearInterval(timer);
        });
    });

    // Restart the timer when mouse leaves the tab links
    tabLinks.forEach(function(link) {
        link.addEventListener("mouseleave", function() {
            timer = setInterval(switchToNextImage, 5000);
        });
    });
});
