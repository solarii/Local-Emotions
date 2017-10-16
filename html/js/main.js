// The Map
var mymap = L.map('mapid', {
	zoom: 12,
	center: [60.1699, 24.9348]
});

// Function for loading the HeatMap with Data
function setHeatMapData(mapData){

	data.data = mapData;
	heatmapLayer.setData(data);

}

function onEachFeature(feature, layer) {
    // bind the text to the popup
   	layer.bindPopup(feature['properties']['text'] + '<p>' + feature['properties']['screen_name'] + ' (' + feature['properties']['name'].join(' ') + ' )</p>' + '<p>' + feature['properties']['gender'] + ', ' + feature['properties']['age'] + '</p>');
}

// Add the tile layer
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
	maxZoom: 18,
	id: 'mapbox.streets',
	accessToken: 'YOUR ACCESS TOKEN'
}).addTo(mymap);

// Heatmap options
var cfg = {
  radius: 15,
  maxOpacity: .8, 
  scaleRadius: false, 
  useLocalExtrema: false,
  latField: 'latitude',
  lngField: 'longitude',
  valueField: 'value'
};

// Constructing the heatlayer
var heatmapLayer = new HeatmapOverlay(cfg);
heatmapLayer.addTo(mymap);

// Constructing the markerlayer
var markerLayer = L.geoJSON(false, {
	onEachFeature: onEachFeature
});

// Set up the data for Heatmap
var data = {
	max: 15,
	min: 0,
	data: []
}

// Initialize some variables
var intervalCounter = 10;
var today;


// Get our JSON data
var goodData = [];
$.getJSON('data/tweets_weekend32_positive_demographics.json', function(rawData){

	// Assign each point an initial value of zero and label them "fresh"
	for (var i = 0; i < rawData.features.length; i++) {
		rawData.features[i].value = 0;
		rawData.features[i].fresh = true;
		rawData.features[i].latitude = rawData.features[i].geometry.coordinates[1];
		rawData.features[i].longitude = rawData.features[i].geometry.coordinates[0];
		rawData.features[i].date = new Date(rawData.features[i].properties.time);
		goodData.push(rawData.features[i]);
	}

	// This is needed for later in the animation (sets the start for the timer)
	today = goodData[0].date;

	// Add the markers
	markerLayer.addData(rawData);

});

// Iterator
var timer;

// This is the function that animates the data
function animator(){

	// Get new day's data every 10 intervals
	if (intervalCounter == 10) {
		intervalCounter = 0;
		getAnotherHour();
	} else {
		intervalCounter++;
	}

	// Create a new array for the next frame's points, remove old points, add new points, then update and push to map
	var newData = [];
	for (var j = 0; j < data.data.length; j++) {

		var point = data.data[j];
		if (point.value >= 10) {
			point.fresh = false;
		}

		// Start fading in the fresh points, and fading out the old points
		if (point.fresh) {
			point.value = point.value + .8;
		} else {
			point.value = point.value - .1;
		}

		if (point.value > 0) {
			newData.push(data.data[j]);
		}

	}

	setHeatMapData(newData);

}

// This the helper function for the animator
// It gets more data from the json file based on the time
function getAnotherHour() {

	// Add up the timer with 1 hour
	today.setHours(today.getHours() + 1);

	for (var index = 0; index < goodData.length; index++) {
		if (goodData[index].date <= today) {
			data.data.push(goodData[index]);
		}
	}

	//console.log(today);
	document.getElementById('timer').innerHTML = today;

} 

// Let's also draw a marker so we can see what time it is
L.Control.Timer = L.Control.extend({
    onAdd: function(map) {
        var div = L.DomUtil.create('div');

        div.innerHTML = '<img style="max-width:10%;" src="img/ami_logo.png"><h3 id="timer">Weekend 32</h3>';

        return div;
    },

    onRemove: function(map) {
        // Nothing to do here
    }
});

L.control.timer = function(opts) {
    return new L.Control.Timer(opts);
}

L.control.timer({ position: 'bottomleft' }).addTo(mymap);

// Add the playback buttons
var pauseAndPLay = L.easyButton({

	states: [{
		stateName: 'play',
		icon: 'fa-play',
		title: 'Play animation',
		onClick: function(control){
			if(!timer){
				timer = setInterval(animator, 100);
			}
			control.state('pause');
		}
	}, {
		stateName: 'pause',
		icon: 'fa-pause',
		title: 'Pause animation',
		onClick: function(control){
			if(timer){
				clearInterval(timer);
				timer = null;
			}
			control.state('play');
		}
	}]

});
pauseAndPLay.addTo(mymap);

// Add the marker control
var toggle = L.easyButton({
  states: [{
    stateName: 'add-markers',
    icon: 'fa-map-marker',
    title: 'add random markers',
    onClick: function(control) {
      mymap.addLayer(markerLayer);
      control.state('remove-markers');
    }
  }, {
    icon: 'fa-undo',
    stateName: 'remove-markers',
    onClick: function(control) {
      mymap.removeLayer(markerLayer);
      control.state('add-markers');
    },
    title: 'remove markers'
  }]
});
toggle.addTo(mymap);

// Add the demographics layer
var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

	var div = L.DomUtil.create('div', 'info legend');

	div.innerHTML = '<h2>Demographics</h2>' + '<h4>Total: 409 positive</h4>' + '<p>' + 'Age: 12-20 , 21-30, 31-44, 45-54, 55-65,' + '</p>' + '<p>' + 'Gender: males 142 (33%), females 123 (29%), unknown: 163 (38%)' + '</p>';

	return div;

};

legend.addTo(mymap);