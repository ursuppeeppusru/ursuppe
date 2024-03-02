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
  'LOCATION:' + venueName + '\\n' + address + '\n' +
  'DESCRIPTION:' + description + '\n' +
  'END:VEVENT\n' +
  'END:VCALENDAR\n';

  download(title + '.ics', icsBody);
}