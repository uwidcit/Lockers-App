const map = L.map('map', {
   center: [10.64234,-61.39773],
   zoom: 17
   });
   L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' }).addTo(map);

   var popup = L.popup();

var markers;
web_lat = document.getElementById('lat_stat')
web_lng = document.getElementById('long_stat')

var mod_lat;
var mod_long;

function setModal(input_field_lat, input_field_long){
   mod_lat = document.getElementById(input_field_lat)
   mod_long = document.getElementById(input_field_long)
}

function onMapClick(e) {
   if (markers){
      markers.remove()
   }
   markers = L.marker(e.latlng).addTo(map)
   web_lat.innerHTML= " Latitude:  " + e.latlng.lat
   mod_lat.value = e.latlng.lat
   web_lng.innerHTML = "Longitude: "+e.latlng.lng
   mod_long.value = e.latlng.lng
}



map.on('click', onMapClick);
