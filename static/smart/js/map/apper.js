var center = [-0.561360, 37.050093];
        var zoom = 12;
        var before = L.map('before', {
                attributionControl: false,
                inertia: false,
                minZoom: 12
            }).setView(center, zoom);
            
        var after = L.map('after', {
                inertia: false,
                minZoom: 12
            }).setView(center, zoom);
L.tileLayer("http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png", {
  subdomains: ["otile1", "otile2", "otile3", "otile4"],
  attribution: 'Tiles courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png">. Map data (c) <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> contributors, CC-BY-SA.'
}).addTo(before);
L.tileLayer("http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png", {
  subdomains: ["otile1", "otile2", "otile3", "otile4"],
  attribution: 'Tiles courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png">. Map data (c) <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> contributors, CC-BY-SA.'
}).addTo(after);
function bStyle(feature) {
  return {
    icon:'glass',
    markerColor: 'red'
  };
}
$("#analyze-btn").click(function() {
  $("#analyzeModal").modal("show");
  $(".navbar-collapse.in").collapse("hide");
  return false;
});
function aStyle(feature) {
  return {
    icon:'glass',
    markerColor: 'blue'
  };
}

var incidenceLayer0 = L.geoJson(null,{
  pointToLayer: function (feature, latlng) {
    return L.marker(latlng, {
      icon: L.icon({
        iconUrl: STATIC_URL + '/smart/img/alcohol.png',
        iconSize: [26, 30],
        iconAnchor: [12, 28],
        popupAnchor: [0, -25]
      }),
      title: feature.properties.incidence_title,
      riseOnHover: true
    });
  },
  filter: function(feature, layer) {
                return (feature.properties.incidence_id <= 15);
            }
}).addTo(before);
var incidenceLayer1 = L.geoJson(null,{
  pointToLayer: function (feature, latlng) {
    return L.marker(latlng, {
      icon: L.icon({
        iconUrl: STATIC_URL + '/smart/img/alcohol.png',
        iconSize: [26, 30],
        iconAnchor: [12, 28],
        popupAnchor: [0, -25]
      }),
      title: feature.properties.incidence_title,
      riseOnHover: true
    });
     
  },
  filter: function(feature, layer) {
                return (feature.properties.incidence_id > 10);
            }
  }).addTo(after);
$.getJSON("http://localhost:8000/incidence_data/", function (data) {
  incidenceLayer0.addData(data).setStyle(bStyle);  
});
$.getJSON("http://localhost:8000/incidence_data/", function (data) {
  incidenceLayer1.addData(data).setStyle(aStyle);  
});
//map.addLayer(incidenceLayer);
$('#map-container').beforeAfter(before, after);