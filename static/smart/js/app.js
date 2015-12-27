var map, featureList, eventSearch = [], incidenceSearch = [], locationSearch = [];

$(window).resize(function() {
  sizeLayerControl();
});

$(document).on("click", ".feature-row", function(e) {
  $(document).off("mouseout", ".feature-row", clearHighlight);
  sidebarClick(parseInt($(this).attr("id"), 10));
});

$(document).on("mouseover", ".feature-row", function(e) {
  highlight.clearLayers().addLayer(L.circleMarker([$(this).attr("lat"), $(this).attr("lng")], highlightStyle));
});

$(document).on("mouseout", ".feature-row", clearHighlight);

$("#about-btn").click(function() {
  $("#aboutModal").modal("show");
  $(".navbar-collapse.in").collapse("hide");
  return false;
});

$("#full-extent-btn").click(function() {
  map.fitBounds(incidences.getBounds());
  $(".navbar-collapse.in").collapse("hide");
  return false;
});

$("#legend-btn").click(function() {
  $("#legendModal").modal("show");
  $(".navbar-collapse.in").collapse("hide");
  return false;
});

$("#login-btn").click(function() {
  $("#loginModal").modal("show");
  $(".navbar-collapse.in").collapse("hide");
  return false;
});

$("#list-btn").click(function() {
  $('#sidebar').toggle();
  map.invalidateSize();
  return false;
});

$("#nav-btn").click(function() {
  $(".navbar-collapse").collapse("toggle");
  return false;
});

$("#sidebar-toggle-btn").click(function() {
  $("#sidebar").toggle();
  map.invalidateSize();
  return false;
});

$("#sidebar-hide-btn").click(function() {
  $('#sidebar').hide();
  map.invalidateSize();
});

function sizeLayerControl() {
  $(".leaflet-control-layers").css("max-height", $("#map").height() - 50);
}

function clearHighlight() {
  highlight.clearLayers();
}

function sidebarClick(id) {
  var layer = markerClusters.getLayer(id);
  map.setView([layer.getLatLng().lat, layer.getLatLng().lng], 17);
  layer.fire("click");
  /* Hide sidebar and go to the map on small screens */
  if (document.body.clientWidth <= 767) {
    $("#sidebar").hide();
    map.invalidateSize();
  }
}
var eventsIcon = STATIC_URL + '/smart/img/snow.png';
var incidenceIcon = STATIC_URL + '/smart/img/magicshow.png';
function syncSidebar() {
  /* Empty sidebar features */
  $("#feature-list tbody").empty();
  /* Loop through events layer and add only features which are in the map bounds */
  events.eachLayer(function (layer) {
    if (map.hasLayer(eventsLayer)) {
      if (map.getBounds().contains(layer.getLatLng())) {
        $("#feature-list tbody").append('<tr class="feature-row" id="' + L.stamp(layer) + '" lat="' + layer.getLatLng().lat + '" lng="' + layer.getLatLng().lng + '"><td style="vertical-align: middle;"><img width="16" height="18" src= '+eventsIcon+'></td><td class="feature-name">' + layer.feature.properties.name + '</td><td style="vertical-align: middle;"><i class="fa fa-chevron-right pull-right"></i></td></tr>');
      }
    }
  });
  /* Loop through incidence layer and add only features which are in the map bounds */
  incidences.eachLayer(function (layer) {
    if (map.hasLayer(incidenceLayer)) {
      if (map.getBounds().contains(layer.getLatLng())) {
        $("#feature-list tbody").append('<tr class="feature-row" id="' + L.stamp(layer) + '" lat="' + layer.getLatLng().lat + '" lng="' + layer.getLatLng().lng + '"><td style="vertical-align: middle;"><img width="16" height="18" src= '+incidenceIcon+'></td><td class="feature-name">' + layer.feature.properties.incidence_title + '</td><td style="vertical-align: middle;"><i class="fa fa-chevron-right pull-right"></i></td></tr>');
      }
    }
  });
  /* Update list.js featureList */
  featureList = new List("features", {
    valueNames: ["feature-name"]
  });
  featureList.sort("feature-name", {
    order: "asc"
  });
}

/* Basemap Layers */
var mapquestOSM = L.tileLayer("http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png", {
  maxZoom: 19,
  subdomains: ["otile1", "otile2", "otile3", "otile4"],
  attribution: 'Tiles courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png">. Map data (c) <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> contributors, CC-BY-SA.'
});
var mapquestOAM = L.tileLayer("http://{s}.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpg", {
  maxZoom: 18,
  subdomains: ["oatile1", "oatile2", "oatile3", "oatile4"],
  attribution: 'Tiles courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a>. Portions Courtesy NASA/JPL-Caltech and U.S. Depart. of Agriculture, Farm Service Agency'
});
var mapquestHYB = L.layerGroup([L.tileLayer("http://{s}.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpg", {
  maxZoom: 18,
  subdomains: ["oatile1", "oatile2", "oatile3", "oatile4"]
}), L.tileLayer("http://{s}.mqcdn.com/tiles/1.0.0/hyb/{z}/{x}/{y}.png", {
  maxZoom: 19,
  subdomains: ["oatile1", "oatile2", "oatile3", "oatile4"],
  attribution: 'Labels courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png">. Map data (c) <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> contributors, CC-BY-SA. Portions Courtesy NASA/JPL-Caltech and U.S. Depart. of Agriculture, Farm Service Agency'
})]);

/* Overlay Layers */

var highlight = L.geoJson(null);
var highlightStyle = {
  stroke: false,
  fillColor: "#00FFFF",
  fillOpacity: 0.7,
  radius: 14
};
var dataurl = 'http://localhost:8000/admin_data/'
$.getJSON(dataurl, function (data) {
    locations.addData(data);
});
var locations = L.geoJson(null,{
  style: function getstyle(feature) {
    switch (feature.properties.location_b){
      case 'MUHITO':
        return {
          weight: 0,
          color: 'orange',
          fillOpacity: 0.7
        };
        break;
      case 'GAKINDU':
        return {
          weight: 0,
          color: 'purple',
          fillOpacity: 0.7
        };
        break;
      case 'GITHII':
        return {
          weight: 0,
          color: 'brown',
          fillOpacity: 0.7
        };
        break;
      case 'RUTUNE':
        return {
          weight: 0,
          color: 'green',
          fillOpacity: 0.7
        };
        break;
      case 'GIKONDI':
        return {
          weight: 0,
          color: 'grey',
          fillOpacity: 0.7
        };
        break;

    }
  },
  onEachFeature: function (feature, layer) {
      layer.on('click', function (e) {
      var popup = "<strong>" + "Id : " + e.target.feature.properties.id + "<br>" + "kenya_id: " + e.target.feature.properties.kenya_id + "<br>" + " kenya_field : " + e.target.feature.properties.kenya_field +  "<br>" + "Location: " + e.target.feature.properties.location_b + "<br>" + "Female: " + e.target.feature.properties.females + "<br>" + "Male: " + e.target.feature.properties.males + "<br>" + "total: " + e.target.feature.properties.total + "</strong>";
      layer.bindPopup(popup).openPopup(e.latlng);
      //map.fitBounds(e.target.getBounds());
    });
    locationSearch.push({
      name: layer.feature.properties.location_b,
      source: "Locations",
      id: L.stamp(layer),
      bounds: layer.getBounds()
    });
  }
});
var eventsLayer = L.geoJson(null);
var events = L.geoJson(null,{
  pointToLayer: function (feature, latlng) {
    return L.marker(latlng, {
      icon: L.icon({
        iconUrl: STATIC_URL + '/smart/img/magicshow.png',
        iconSize: [24, 28],
        iconAnchor: [12, 28],
        popupAnchor: [0, -25]
      }),
      title: feature.properties.name,
      riseOnHover: true
    });
  },
  style: function (feature) {
    return {
      color: "green",
      fill: true,
      opacity: 1,
      clickable: true
    };
  },
  onEachFeature: function (feature, layer) {
    if (feature.properties) {
      layer.on('click', function (e) {
      var popup = "<strong>" + "Name : " + e.target.feature.properties.name + "<br>" + "Organizers: " + e.target.feature.properties.organizers + "<br>" + " Event Type : " + e.target.feature.properties.event_type +  "<br>" + "Location: " + e.target.feature.properties.location + "<br>" + "Venue: " + e.target.feature.properties.venue + "<br>" + "Date: " + e.target.feature.properties.date + "<br>" + "Contacts: " + e.target.feature.properties.contacts + "</strong>";
      layer.bindPopup(popup).openPopup(e.latlng);
      highlight.clearLayers().addLayer(L.circleMarker([feature.geometry.coordinates[1], feature.geometry.coordinates[0]], highlightStyle));

      //map.fitBounds(e.target.getBounds());
    });
    $("#feature-list tbody").append('<tr class="feature-row" id="' + L.stamp(layer) + '" lat="' + layer.getLatLng().lat + '" lng="' + layer.getLatLng().lng + '"><td style="vertical-align: middle;"><img width="16" height="18" src='+ eventsIcon+'>' + layer.feature.properties.name + '</td><td style="vertical-align: middle;"><i class="fa fa-chevron-right pull-right"></i></td></tr>'); 
    eventSearch.push({
      name: layer.feature.properties.name,
      address: layer.feature.properties.event_type,
      source: "Events",
      id: L.stamp(layer),
      lat: layer.feature.geometry.coordinates[1],
      lng: layer.feature.geometry.coordinates[0]
    });
  }
}
});
var incidenceLayer = L.geoJson(null);
var incidences = L.geoJson(null,{
  pointToLayer: function (feature, latlng) {
    return L.marker(latlng, {
      icon: L.icon({
        iconUrl: STATIC_URL + '/smart/img/snow.png',
        iconSize: [24, 28],
        iconAnchor: [12, 28],
        popupAnchor: [0, -25]
      }),
      title: feature.properties.incidence_title,
      riseOnHover: true
    });
  },
  style: function (feature) {
    switch (feature.properties.status){
    case 'Average':
      return {
        color: "blue",
        weight: 0,
        fillOpacity: 0.6
      };
      break;
    case 'Bad':
     return {
        color: "orange",
        weight: 0,
        fillOpacity: 0.6
      };
      break;
    case 'Very Bad':
      return {
        color: "red",
        weight: 0,
        fillOpacity: 0.6
      };
      break;
    case 'Unknown':
      return {
        color: "grey",
        weight: 0,
        fillOpacity: 0.6
      };
      break;
  }
  },
  onEachFeature: function (feature, layer) {
    if (feature.properties) {
    layer.on('click', function (e) {
      var popup = "<strong>" + "Title : " + e.target.feature.properties.incidence_title + "<br>" + "Category: " + e.target.feature.properties.category + "<br>" + " County : " + e.target.feature.properties.county +  "<br>" + "Closest Town: " + e.target.feature.properties.closest_town + "<br>" + "status: " + e.target.feature.properties.status + "<br>" + "Date Reported: " + e.target.feature.properties.date_applied + "</strong>";
      layer.bindPopup(popup).openPopup(e.latlng);
      highlight.clearLayers().addLayer(L.circleMarker([feature.geometry.coordinates[1], feature.geometry.coordinates[0]], highlightStyle));

      //map.fitBounds(e.target.getBounds());
    }); 
    $("#feature-list tbody").append('<tr class="feature-row" id="' + L.stamp(layer) + '" lat="' + layer.getLatLng().lat + '" lng="' + layer.getLatLng().lng + '"><td style="vertical-align: middle;"><img width="16" height="18" src='+incidenceIcon+'></td><td class="feature-name">' + layer.feature.properties.incidence_title + '</td><td style="vertical-align: middle;"><i class="fa fa-chevron-right pull-right"></i></td></tr>');
    incidenceSearch.push({
        name: layer.feature.properties.incidence_title,
        address: layer.feature.properties.status,
        source: "Incidences",
        id: L.stamp(layer),
        lat: layer.feature.geometry.coordinates[1],
        lng: layer.feature.geometry.coordinates[0]
      });

  }
}

});
$.getJSON("http://localhost:8000/events_data/", function (data) {
  events.addData(data);
  map.addLayer(eventsLayer);
});
$.getJSON("http://localhost:8000/incidence_data/", function (data) {
  incidences.addData(data);
  map.addLayer(incidenceLayer);
});

/* Single marker cluster layer to hold all clusters */
var markerClusters = new L.MarkerClusterGroup({
  spiderfyOnMaxZoom: true,
  showCoverageOnHover: false,
  zoomToBoundsOnClick: true,
  disableClusteringAtZoom: 16
});

map = L.map("map", {
  zoom: 13,
  center: [-0.561360, 37.050093],
  layers: [mapquestOSM, markerClusters,highlight],
  zoomControl: false,
  attributionControl: false
});

/* Layer control listeners that allow for a single markerClusters layer */
map.on("overlayadd", function(e) {
  if (e.layer === eventsLayer) {
    markerClusters.addLayer(events);
    syncSidebar();
  }
  if (e.layer === incidenceLayer) {
    markerClusters.addLayer(incidences);
    syncSidebar();
  }
});
map.on("overlayremove", function(e) {
  if (e.layer === eventsLayer) {
    markerClusters.removeLayer(events);
    syncSidebar();
  }
  if (e.layer === incidenceLayer) {
    markerClusters.removeLayer(incidences);
    syncSidebar();
  }
});

/* Filter sidebar feature list to only show features in current map bounds */
map.on("moveend", function (e) {
  syncSidebar();
});

/* Clear feature highlight when map is clicked */
map.on("click", function(e) {
  highlight.clearLayers();
});

/* Attribution control */
function updateAttribution(e) {
  $.each(map._layers, function(index, layer) {
    if (layer.getAttribution) {
      $("#attribution").html((layer.getAttribution()));
    }
  });
}
map.on("layeradd", updateAttribution);
map.on("layerremove", updateAttribution);

var attributionControl = L.control({
  position: "bottomright"
});
attributionControl.onAdd = function (map) {
  var div = L.DomUtil.create("div", "leaflet-control-attribution");
  div.innerHTML = "<span class='hidden-xs'>Developed by <a href='http://wanjohikibui.blogspot.com'>wanjohikibui</a> | </span><a href='#' onclick='$(\"#attributionModal\").modal(\"show\"); return false;'>Attribution</a>";
  return div;
};
map.addControl(attributionControl);

var zoomControl = L.control.zoom({
  position: "topleft"
}).addTo(map);

/* GPS enabled geolocation control set to follow the user's location */
var locateControl = L.control.locate({
  position: "topleft",
  drawCircle: true,
  follow: true,
  setView: true,
  keepCurrentZoomLevel: true,
  markerStyle: {
    weight: 1,
    opacity: 0.8,
    fillOpacity: 0.8
  },
  circleStyle: {
    weight: 1,
    clickable: false
  },
  icon: "fa fa-location-arrow",
  metric: false,
  strings: {
    title: "My location",
    popup: "You are within {distance} {unit} from this point",
    outsideMapBoundsMsg: "You seem located outside the boundaries of the map"
  },
  locateOptions: {
    maxZoom: 18,
    watch: true,
    enableHighAccuracy: true,
    maximumAge: 10000,
    timeout: 10000
  }
}).addTo(map);
//map.addLayer(locations);
/* Larger screens get expanded layer control and visible sidebar */
if (document.body.clientWidth <= 767) {
  var isCollapsed = true;
} else {
  var isCollapsed = false;
}

var baseLayers = {
  "Street Map": mapquestOSM,
  "Aerial Imagery": mapquestOAM,
  "Imagery with Streets": mapquestHYB
};

var groupedOverlays = {
  "Locational Info": {
    "Locations": locations,
  },
  "App Layers": {
    "<img src= '+eventsIcon+' width='24' height='28'>&nbsp;Incidences": incidenceLayer,
    "<img src='+eventsIcon+' width='24' height='28'>&nbsp;Events": eventsLayer
  }
};

var layerControl = L.control.groupedLayers(baseLayers, groupedOverlays, {
  collapsed: isCollapsed
}).addTo(map);

/* Highlight search box text on click */
$("#searchbox").click(function () {
  $(this).select();
});

/* Prevent hitting enter from refreshing the page */
$("#searchbox").keypress(function (e) {
  if (e.which == 13) {
    e.preventDefault();
  }
});
$("#printBtn").click(function(){
  $('#map').print();
});
$("#featureModal").on("hidden.bs.modal", function (e) {
  $(document).on("mouseout", ".feature-row", clearHighlight);
});

/* Typeahead search functionality */
$(document).one("ajaxStop", function () {
  $("#loading").hide();
  sizeLayerControl();
  /* Fit map to location bounds */
  map.fitBounds(locations.getBounds());
  featureList = new List("features", {valueNames: ["feature-name"]});
  featureList.sort("feature-name", {order:"asc"});

  var locationBH = new Bloodhound({
    name: "Location",
    datumTokenizer: function (d) {
      return Bloodhound.tokenizers.whitespace(d.name);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: locationSearch,
    limit: 10
  });

  var eventsBH = new Bloodhound({
    name: "Events",
    datumTokenizer: function (d) {
      return Bloodhound.tokenizers.whitespace(d.name);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: eventSearch,
    limit: 10
  });

  var incidenceBH = new Bloodhound({
    name: "Incidences",
    datumTokenizer: function (d) {
      return Bloodhound.tokenizers.whitespace(d.name);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: incidenceSearch,
    limit: 10
  });
  
  locationBH.initialize();
  eventsBH.initialize();
  incidenceBH.initialize();

  /* instantiate the typeahead UI */
  $("#searchbox").typeahead({
    minLength: 3,
    highlight: true,
    hint: true
  }, 
   {
    name: "Locations",
    displayKey: "location_b",
    source: locationBH.ttAdapter(),
    templates: {
      header: "<h4 class='typeahead-header'>Location</h4>",
      suggestion: Handlebars.compile(["{{name}}<br>&nbsp;<small>{{address}}</small>"].join(""))
    }
  },{
    name: "Events",
    displayKey: "name",
    source: eventsBH.ttAdapter(),
    templates: {
      header: "<h4 class='typeahead-header'><img src='+eventsIcon+' width='24' height='28'>Events</h4>"
    }
  }, {
    name: "Incidences",
    displayKey: "incidence_title",
    source: incidenceBH.ttAdapter(),
    templates: {
      header: "<h4 class='typeahead-header'><img src='+eventsIcon+' width='24' height='28'>&nbsp;incidences</h4>",
      suggestion: Handlebars.compile(["{{name}}<br>&nbsp;<small>{{address}}</small>"].join(""))
    }
  }).on("typeahead:selected", function (obj, datum) {
    if (datum.source === "Locations") {
      map.fitBounds(datum.bounds);
    }
    if (datum.source === "Incidences") {
      if (!map.hasLayer(incidenceLayer)) {
        map.addLayer(incidenceLayer);
      }
      map.setView([datum.lat, datum.lng], 17);
      if (map._layers[datum.id]) {
        map._layers[datum.id].fire("click");
      }
    }
     if (datum.source === "Events") {
      if (!map.hasLayer(eventsLayer)) {
        map.addLayer(eventsLayer);
      }
      map.setView([datum.lat, datum.lng], 17);
      if (map._layers[datum.id]) {
        map._layers[datum.id].fire("click");
      }
    }
    if ($(".navbar-collapse").height() > 50) {
      $(".navbar-collapse").collapse("hide");
    }
  }).on("typeahead:opened", function () {
    $(".navbar-collapse.in").css("max-height", $(document).height() - $(".navbar-header").height());
    $(".navbar-collapse.in").css("height", $(document).height() - $(".navbar-header").height());
  }).on("typeahead:closed", function () {
    $(".navbar-collapse.in").css("max-height", "");
    $(".navbar-collapse.in").css("height", "");
  });
  $(".twitter-typeahead").css("position", "static");
  $(".twitter-typeahead").css("display", "block");
});

// Leaflet patch to make layer control scrollable on touch browsers
var container = $(".leaflet-control-layers")[0];
if (!L.Browser.touch) {
  L.DomEvent
  .disableClickPropagation(container)
  .disableScrollPropagation(container);
} else {
  L.DomEvent.disableClickPropagation(container);
}
