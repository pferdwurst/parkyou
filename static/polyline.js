

function initialize(center, reglines) {
  
  var mapOptions = {
    zoom: 3,
    center: center,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  };

  var map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);

  
    for (var  line in reglines) {
    var path = [];  
    
      
    for (var point in line) {
        path.push( new google.maps.LatLng( point.latitude, point.longnitude ));
    }
    
    var polypath = new google.maps.Polyline( {
        path: path,
        geodesic: true,
        strokeColor: "#ccc000",
        strokeOpacity: 4.0,  
        strokeWeight: 1
    });
    polypath.setMap(map);
  }

}


