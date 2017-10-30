var map_data=null
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
                    console.log(map_data[i]['earthquake_id']);
                    temp = info_base;
                    temp.replace('ear_pos',map_data[i]['earthquake_ear_epicenter_pos']);
                    locations.push({
                        lat: map_data[i]['earthquake_ear_latitude'],
                        lng: map_data[i]['earthquake_ear_longitude'],
                        info: temp
                    });
                    console.log(locations);
                  }
                  new google.maps.event.addDomListener(window, "load", initMap);
                },

                error: function(e) {
                  alert("錯誤: 資料來源錯誤(.json) ::"+e);
                }
              });
          })
    }
});



new google.maps.event.addDomListener(window, "load", initMap);