
var map_data=null;
var info_base = '<div id="content">'+
                  '<div id="siteNotice"></div>'+
                  '<h1 id="firstHeading" class="firstHeading">ear_pos</h1>'+
                  '<div id="bodyContent">'+
                    '<p><b>編號</b>: earthquake_id</p>'+
                    '<p><b>地震編號</b>: ear_id</p>'+
                    '<p><b>台灣時間</b>: s_year年ear_time</p>'+
                    '<p><b>經度</b>: ear_longitude</p>'+
                    '<p><b>緯度</b>: ear_latitude</p>'+
                    '<p><b>規模</b>: ear_scale</p>'+
                    '<p><b>深度</b>: ear_deep</p>'+
                  '</div>'+
                '</div>';
var locations = [];
function load(){
  $.ajax({
  url: "../ear_data/",
  type: "GET",
  dataType: "json",
  data: {limit:"-1"},
  success: function(data) {
    locations=[];
    console.log(data['rows']);
    map_data = data['rows'];
    for (var i = 0; i < map_data.length; i++) {
      temp = replace_ear_string(info_base,"ear_pos", i);
      locations.push({
          lat: map_data[i]['earthquake_ear_latitude'],
          lng: map_data[i]['earthquake_ear_longitude'],
          info: temp
      });
    }
    update();
  },

  error: function(e) {
    alert("錯誤: 資料來源錯誤(.json) ::"+e);
  }
});
}

//ajax
$("#inputTarget").keypress(function(e){
  code = (e.keyCode ? e.keyCode : e.which);
  if (code == 13)
  {$(function(e) {    
              $.ajax({
                url: "../ear_data/",
                type: "GET",
                dataType: "json",
                data: {search:$("#inputTarget").val(),limit:"-1"},
                success: function(data) {
                  locations=[];
                  console.log(data['rows']);
                  map_data = data['rows'];
                  document.getElementById("searchCount").innerHTML="搜尋結果: 共有 <strong>"+data['total']+"</strong> 筆符合項目";
                  for (var i = 0; i < map_data.length; i++) {
                    temp = replace_ear_string(info_base,"ear_pos", i);
                    locations.push({
                        lat: map_data[i]['earthquake_ear_latitude'],
                        lng: map_data[i]['earthquake_ear_longitude'],
                        info: temp
                    });
                  }
                  update();
                },

                error: function(e) {
                  alert("錯誤: 資料來源錯誤(.json) ::"+e);
                }
              });
          })
    }
});

function replace_ear_string(infowindow_base, word, index){
    temp = infowindow_base;
    temp = temp.split("ear_pos")[0] + map_data[index]['earthquake_ear_epicenter_pos'] + temp.split("ear_pos")[1];
    temp = temp.split("earthquake_id")[0] + map_data[index]['earthquake_id'] + temp.split("earthquake_id")[1];
    temp = temp.split("ear_id")[0] + map_data[index]['earthquake_ear_id'] + temp.split("ear_id")[1];
    temp = temp.split("s_year")[0] + map_data[index]['earthquake_s_year'] + temp.split("s_year")[1];
    temp = temp.split("ear_time")[0] + map_data[index]['earthquake_ear_time'] + temp.split("ear_time")[1];
    temp = temp.split("ear_longitude")[0] + map_data[index]['earthquake_ear_longitude'] + temp.split("ear_longitude")[1];
    temp = temp.split("ear_latitude")[0] + map_data[index]['earthquake_ear_latitude'] + temp.split("ear_latitude")[1];
    temp = temp.split("ear_scale")[0] + map_data[index]['earthquake_ear_scale'] + temp.split("ear_scale")[1];
    temp = temp.split("ear_deep")[0] + map_data[index]['earthquake_ear_deep'] + temp.split("ear_deep")[1];
    return temp;
}

new google.maps.event.addDomListener(window, "load", initMap);

var map;
var markers;
var markerCluster;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 8,
    center: {
      lat: 23.88,
      lng: 121.04
    }
  });
  var infoWin = new google.maps.InfoWindow();
  // Add some markers to the map.
  // Note: The code uses the JavaScript Array.prototype.map() method to
  // create an array of markers based on a given "locations" array.
  // The map() method here has nothing to do with the Google Maps API.
  markers = locations.map(function(location, i) {
    var marker = new google.maps.Marker({
      position: location
    });
    google.maps.event.addListener(marker, 'click', function(evt) {
      infoWin.setContent(location.info);
      infoWin.open(map, marker);
    })
    return marker;
  });

  // markerCluster.setMarkers(markers);
  // Add a marker clusterer to manage the markers.
  markerCluster = new MarkerClusterer(map, markers, {
    imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
  });

}

function update() {
  for(var i = 0; i<markers.length;i++){
    markers[i].setMap(null);
  }
  markerCluster.clearMarkers();
  markers = null;

  var infoWin = new google.maps.InfoWindow();

  markers = locations.map(function(location, i) {
    var marker = new google.maps.Marker({
      position: location
    });
    google.maps.event.addListener(marker, 'click', function(evt) {
      infoWin.setContent(location.info);
      infoWin.open(map, marker);
    })
    return marker;
  });

  markerCluster = new MarkerClusterer(map, markers, {
    imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
  });
}