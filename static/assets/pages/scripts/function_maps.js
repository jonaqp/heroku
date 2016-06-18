$(document).ready(function () {
    var map;
    this.map = L.map('mapid').setView([52.0, -11.0], 5);

    var mbUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw';
    var grayscale = L.tileLayer(mbUrl, {id: 'mapbox.light'}),
        streets = L.tileLayer(mbUrl, {id: 'mapbox.streets'});
    var layer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png', {
        maxZoom: 15,
        layers: [grayscale],
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    }).addTo(this.map);
    var googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
        maxZoom: 15,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    });
    var googleHybrid = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
        maxZoom: 15,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    });
    var googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
        maxZoom: 15,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    });
    var googleTerrain = L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}', {
        maxZoom: 15,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    });
    var baseLayers = {
        "Grayscale": grayscale,
        "Streets": streets,
        "G. Streets": googleStreets,
        "G. Hybrid": googleHybrid,
        "G. Satelital": googleSat,
        "G. Terrain": googleTerrain
    };
    L.control.layers(baseLayers).addTo(this.map);

    map = this.map;

    var multiCoords1 = [
        [[47.5468, -0.7910], [48.8068, -0.1318], [49.1242, 1.6699], [49.4966, 3.2958], [51.4266, 2.8564], [51.7542, 2.1093]],
        [[48.0193, -2.8125], [46.3165, -2.8564], [44.9336, -1.0107], [44.5278, 1.5820], [44.8714, 3.7353], [45.8287, 5.1855], [48.1953, 5.1416]],
        [[45.9205, 0.4394], [46.7699, 0.9228], [47.6061, 2.5488], [47.7540, 3.3837]]
    ];
    var plArray = [];
    for (var i = 0; i < multiCoords1.length; i++) {
        plArray.push(L.polyline(multiCoords1[i]).addTo(map));
    }
    L.polylineDecorator(multiCoords1, {
        patterns: [
            {
                offset: 25,
                repeat: 50,
                symbol: L.Symbol.arrowHead({pixelSize: 15, pathOptions: {fillOpacity: 1, weight: 0}})
            }
        ]
    }).addTo(map);

});