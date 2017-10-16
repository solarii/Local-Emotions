// The Map
var mymap = L.map('mapid', {
	zoom: 12,
	center: [60.1699, 24.9348]
});

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
  valueField: 'value',
  gradient: {
  	'.5' : 'blue',
  	'.95' : 'violet'
  }
};

// Constructing the heatlayer
var heatmapLayer = new HeatmapOverlay(cfg);
heatmapLayer.addTo(mymap);

// Set up the data for Heatmap
var data = {
	max: 15,
	min: 0,
	data: []
}

// Initialize some variables
var intervalCounter = 10;
var today;

// Function for loading the HeatMap with Data
function setHeatMapData(mapData){

	data.data = mapData;
	heatmapLayer.setData(data);

}


// Get our JSON data
var goodData = [];
$.getJSON('data/twitterstream_weekend_negative.geojson', function(rawData){

	// Assign each point an initial value of zero and label them "fresh"
	for (var i = 0; i < rawData.features.length; i++) {
		rawData.features[i].value = 0;
		rawData.features[i].fresh = true;
		rawData.features[i].latitude = rawData.features[i].geometry.coordinates[1];
		rawData.features[i].longitude = rawData.features[i].geometry.coordinates[0];
		rawData.features[i].date = new Date(rawData.features[i].properties.time);
		goodData.push(rawData.features[i]);
	}

	// Link it to the Heatmap
	//setHeatMapData(goodData);

	// This is needed for later
	today = goodData[0].date;

});

// Iterator
setInterval(function(){

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

}, 100);


function getAnotherHour() {

	// Add up the timer with 1 hour
	today.setHours(today.getHours() + 1);

	for (var index = 0; index < goodData.length; index++) {
		if (goodData[index].date <= today) {
			data.data.push(goodData[index]);
		}
	}

	console.log(today);

} 

// Let's also draw a marker so we can see what time it is
L.Control.Timer = L.Control.extend({
    onAdd: function(map) {
        var div = L.DomUtil.create('div');

        div.innerHTML = '<h1>TIMER!</h1>';

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
