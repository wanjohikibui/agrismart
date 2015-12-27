var osmLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>',
	thunLink = '<a href="http://thunderforest.com/">Thunderforest</a>';

var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
	osmAttrib = '&copy; ' + osmLink + ' Contributors',
	landUrl = 'http://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png',
	thunAttrib = '&copy; '+osmLink+' Contributors & '+thunLink;

var mapUrl = 'http://otile4.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.png',
	mapAttrib = '&copy; ' + osmLink + ' Contributors';

var osmMap = L.tileLayer(osmUrl, {attribution: osmAttrib}),
	landMap = L.tileLayer(landUrl, {attribution: thunAttrib});

var aerial= L.tileLayer(mapUrl, {attribution: mapAttrib});

var dataurl = '/admin_data/'
var landuseurl = '/landuse_data/'
var soilurl = '/soil_data/'
var phurl = '/ph_data/'
var rainfallurl = '/rainfall_data/'
var temperatureurl = '/temperature_data/'
var elevationurl = '/elevation_data/'

var locations= L.geoJson();
var landuse= L.geoJson();
var soil= L.geoJson();
var ph = L.geoJson();
var rainfall= L.geoJson();
var temperature= L.geoJson();
var elevation = L.geoJson();

var redMarker = L.AwesomeMarkers.icon({
    icon: 'flag',
    markerColor: 'green'
  });

function elevationStyle(feature) {
	return {
		color: 'brown',
		weight: 1.6,
	};
}
function landuseStyle(feature) {
	switch (feature.properties.landuse){
		case 'built up':
			return {
				weight: 1.0,
				opacity: .5,
				color: 'red',
				dashArray: '3',
				fillOpacity: 0.7
			};
			break;
		case 'forest':
			return {
				weight: 1,
				opacity: .5,
				color: 'dark green',
				dashArray: '3',
				fillOpacity: 0.7
			};
			break;
		case 'vegetation':
			return {
				weight: 1,
				opacity: 0.5,
				color: 'lime green',
				dashArray: '3',
				fillOpacity: 0.7
			};
			break;
		case 'bare land':
			return {
				weight: 1,
				opacity: 0.5,
				color: 'yellow',
				dashArray: '3',
				fillOpacity: 0.7
			};
			break;
	}

}
function phStyle(feature) {
	switch (feature.properties.phaq){
		case '5.6':
			return {
				weight: 2.0,
				opacity: 1.0,
				color: 'orange',
				dashArray: '3',
				fillOpacity: 0.7
			};
			break;
		case '0.0':
			return {
				weight: 2,
				opacity: 1,
				color: 'purple',
				dashArray: '3',
				fillOpacity: 0.7
			};
			break;
	}

}
function soilStyle(feature) {
	switch (feature.properties.text_descr){
		case 'loamy':
			return {
				weight: 2.0,
				opacity: 1.0,
				color: 'brown',
				dashArray: '3',
				fillOpacity: 0.7
			};
			break;
		case 'clayey':
			return {
				weight: 2,
				opacity: 1,
				color: 'grey',
				dashArray: '3',
				fillOpacity: 0.7
			};
			break;
	}

}
function rainfallStyle(feature) {
	switch (feature.properties.type){
		case '1200-1600':
			return {
				weight: 2.0,
				opacity: 1.0,
				color: 'orange',
				dashArray: '3',
				fillOpacity: 0.7
			};
			break;
		case '800-1200':
			return {
				weight: 1,
				opacity: 1,
				color: 'orange',
				dashArray: '3',
				fillOpacity: 0.2
			};
			break;
	}

}
function temperatureStyle(feature) {
	switch (feature.properties.tem){
		case '18-20':
			return {
				weight: 1.0,
				opacity: 1.0,
				color: 'green',
				dashArray: '3',
				fillOpacity: 0.2
			};
			break;
		case '20-22':
			return {
				weight: 2,
				opacity: 1,
				color: 'green',
				dashArray: '3',
				fillOpacity: 0.7
			};
			break;
	}

}
function getstyle(feature) {
	switch (feature.properties.location_b){
		case 'MUHITO':
			return {
				weight: 2.0,
				opacity: 1.0,
				color: 'orange',
				dashArray: '3',
				fillOpacity: 0.7
			};
			break;
		case 'GAKINDU':
			return {
				weight: 2,
				opacity: 1,
				color: 'purple',
				dashArray: '3',
				fillOpacity: 0.7
			};
			break;
		case 'GITHII':
			return {
				weight: 2,
				opacity: 1,
				color: 'brown',
				dashArray: '3',
				fillOpacity: 0.7
			};
			break;
		case 'RUTUNE':
			return {
				weight: 2,
				opacity: 1,
				color: 'green',
				dashArray: '3',
				fillOpacity: 0.7
			};
			break;
		case 'GIKONDI':
			return {
				weight: 2,
				opacity: 1,
				color: 'grey',
				dashArray: '3',
				fillOpacity: 0.7
			};
			break;

	}

}
var markers = L.markerClusterGroup();
var markincident = L.markerClusterGroup();

var map = L.map('map',{
	layers: [osmMap],
	keyboard: true,
	boxZoom: true,
	zoomControl: false,
	//measureControl: true,
	doubleClickZoom: true,
	scrollWheelZoom: true,
	fullscreenControl: true,
	fullscreenControlOptions: {
		position: 'topleft'
	} 
	}).setView([-0.561360, 37.050093], 13);
	mapLink ='<a href="http://openstreetmap.org">OpenStreetMap</a>';
	L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
				attribution: 'Map data &copy; ' + mapLink,
			    maxZoom:32,
			    }).addTo(map);
				

// add the new control to the map
$("#printBtn").click(function(){
  $('#map').print();
});
map.addControl(new L.Control.ZoomMin())

var measureControl = L.control.measure({
	position: 'topleft',
	completedColor: '#C8F2BE'
});
measureControl.addTo(map);

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

var trainIcon = new L.icon({
  iconUrl: "img/alcohol.png",
});
// control that shows state info on hover
$.getJSON(dataurl, function (data) {
    locations.addData(data).setStyle(getstyle);
    locations.eachLayer(function (layer) { 
    layer.on('click', function (e) {
		var popup = "<strong>" + "Id : " + e.target.feature.properties.id + "<br>" + "kenya_id: " + e.target.feature.properties.kenya_id + "<br>" + " kenya_field : " + e.target.feature.properties.kenya_field +  "<br>" + "Location: " + e.target.feature.properties.location_b + "<br>" + "Female: " + e.target.feature.properties.females + "<br>" + "Male: " + e.target.feature.properties.males + "<br>" + "total: " + e.target.feature.properties.total + "</strong>";
		layer.bindPopup(popup).openPopup(e.latlng);
		//map.fitBounds(e.target.getBounds());
	});	
	//locations.bindLabel(feature.properties['location_b'], { 'noHide': true });

	});	
});
$.getJSON(landuseurl, function (data) {
    landuse.addData(data).setStyle(landuseStyle);
    landuse.eachLayer(function (layer) { 
    layer.on('click', function (e) {
		var popup = "<strong>" + "Id : " + e.target.feature.properties.id + "<br>" + "Grid Code : " + e.target.feature.properties.dn + "<br>" + " Landuse : " + e.target.feature.properties.landuse +  "<br>" + "</strong>";
		layer.bindPopup(popup).openPopup(e.latlng);
		//map.fitBounds(e.target.getBounds());
	});	
	//landuse.bindLabel(feature.properties['location_b'], { 'noHide': true });

	});	
});
$.getJSON(soilurl, function (data) {
    soil.addData(data).setStyle(soilStyle);
    soil.eachLayer(function (layer) { 
    layer.on('click', function (e) {
		var popup = "<strong>" + "Id : " + e.target.feature.properties.id + "<br>" + "Drainage: " + e.target.feature.properties.drai_descr + "<br>" + " Type : " + e.target.feature.properties.text_descr +  "<br>" + "</strong>";
		layer.bindPopup(popup).openPopup(e.latlng);
		//map.fitBounds(e.target.getBounds());
	});	
	//soil.bindLabel(feature.properties['location_b'], { 'noHide': true });

	});	
});
$.getJSON(elevationurl, function (data) {
    elevation.addData(data).setStyle(elevationStyle);
    elevation.eachLayer(function (layer) { 
    layer.on('mouseover', function (e) {
		var popup = "<strong>" + "Id : " + e.target.feature.properties.id + "<br>" + "Elevation: " + e.target.feature.properties.elev + "<br>" +"</strong>";
		layer.bindPopup(popup).openPopup(e.latlng);
		//map.fitBounds(e.target.getBounds());
	});

	//elevation.bindLabel(feature.properties['location_b'], { 'noHide': true });

	});	
});
$.getJSON(phurl, function (data) {
    ph.addData(data).setStyle(phStyle);
    ph.eachLayer(function (layer) { 
    layer.on('click', function (e) {
		var popup = "<strong>" + "Id : " + e.target.feature.properties.id + "<br>" + "Phaq: " + e.target.feature.properties.phaq + "<br>" + "</strong>";
		layer.bindPopup(popup).openPopup(e.latlng);
		//map.fitBounds(e.target.getBounds());
	});	
	//ph.bindLabel(feature.properties['location_b'], { 'noHide': true });

	});	
});
$.getJSON(rainfallurl, function (data) {
    rainfall.addData(data).setStyle(rainfallStyle);
    rainfall.eachLayer(function (layer) { 
    layer.on('click', function (e) {
		var popup = "<strong>" + "Id : " + e.target.feature.properties.id + "<br>" + "Rainfall: " + e.target.feature.properties.rainfall_field + "<br>" + " Rain Type : " + e.target.feature.properties.type +  "<br>" + "</strong>";
		layer.bindPopup(popup).openPopup(e.latlng);
		//map.fitBounds(e.target.getBounds());
	});	
	//rainfall.bindLabel(feature.properties['location_b'], { 'noHide': true });

	});	
});
$.getJSON(temperatureurl, function (data) {
    temperature.addData(data).setStyle(temperatureStyle);
    temperature.eachLayer(function (layer) { 
    layer.on('click', function (e) {
		var popup = "<strong>" + "Id : " + e.target.feature.properties.id + "<br>" + "Average temp : " + e.target.feature.properties.avg + "<br>" + " Temperature Type : " + e.target.feature.properties.tem +  "<br>" + "</strong>";
		layer.bindPopup(popup).openPopup(e.latlng);
		//map.fitBounds(e.target.getBounds());
	});	
	//temperature.bindLabel(feature.properties['location_b'], { 'noHide': true });

	});	
});

var legend = L.control({position:'bottomleft'});
legend.onAdd = function (map) {
	var div = L.DomUtil.create('div','info legend');
	div.innerHTML = "<h3>Legend</h3><table></table>";
	return div;
}
legend.addTo(map);
map.addLayer(locations)
//map.addLayer(landuse)
//map.addLayer(soil)
//map.addLayer(ph)
//map.addLayer(rainfall)
//map.addLayer(temperature)

var baseLayers = {
	"OSM Mapnik": osmMap,
	"Landscape": landMap,
	"Aerial":aerial
};

var overlays = {
	"Admin Sections": locations,
	"Landuse": landuse,
	"Soil data": soil,
	"Soil PH": ph,
	"Rainfall Distribution": rainfall,
	"Temperature Ranges": temperature,
	"Elevation": elevation
};

L.control.layers(baseLayers,overlays,{collapsed:false}).addTo(map);
L.control.scale({position:"bottomleft"}).addTo(map);
var routing = L.Routing.control({
	    waypoints: [
	        L.latLng(-0.561360, 37.050093),
	        L.latLng(-0.567360, 37.052393)
	    ],
	    routeWhileDragging: true,
	    geocoder: L.Control.Geocoder.nominatim()
	});
L.easyButton('fa-compass',
  function (){
    $('.leaflet-routing-container').is(':visible') ? routing.removeFrom(map) : routing.addTo(map)
  },
  'Routing'
).addTo(map);


function createButton(label, container) {
    var btn = L.DomUtil.create('button', '', container);
    btn.setAttribute('type', 'button');
    btn.innerHTML = label;
    return btn;
}
/*var startBtn;
var destBtn;
map.on('click', function(e) {
    var container = L.DomUtil.create('div'),
        startBtn = createButton('Start from this location', container),
        destBtn = createButton('Go to this location', container);

    L.popup()
        .setContent(container)
        .setLatLng(e.latlng)
        .openOn(map);
});
 L.DomEvent.on(startBtn, 'click', function() {
        control.spliceWaypoints(0, 1, e.latlng);
        map.closePopup();
    });
L.DomEvent.on(destBtn, 'click', function() {
        control.spliceWaypoints(control.getWaypoints().length - 1, 1, e.latlng);
        map.closePopup();
    });
var turf = require('turf') // this line is for node.js, but you do not need it in the browser
var pt = {
  type: 'Feature',
  geometry: {
    type: 'Point',
    coordinates: [-0.561360, 37.050093]
  },
  properties: {}
};
var unit = 'meters'

// 10 mile ring
var buffered = turf.buffer(pt, 10, unit)
L.geoJson(buffered).addTo(map);*/