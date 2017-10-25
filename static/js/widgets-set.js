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
                  console.log(data['rows']);
                  document.getElementById("searchCount").innerHTML="搜尋結果: 共有 <strong>"+data['total']+"</strong> 筆符合項目";
                },

                error: function(e) {
                  alert("ERROR: Data should be readable.(.json) ::"+e);
                }
              });
          })
    }
});


//drag & drop & sort
var dragapproved = false; 
var dragObj;
var dBack; 
var offX,offY;
var group1 = document.getElementById("group1");
var group2 = document.getElementById("group2");
var group3 = document.getElementById("group3");
document.onmousedown = beginDrag; 
document.onmouseup = function() {
  if (dragapproved == true) {
    dragapproved = false;
    dragObj.className = "drag";
    dBack.parentNode.replaceChild(dragObj,dBack);
    // rememberLayout();
  } 
} 
document.onmousemove = dragDrop; 
function dragDrop(evt) { 
  if (dragapproved) { 
    var e = evt || window.event;
    var x = e.clientX - offX + document.body.scrollLeft;
    var y = e.clientY - offY + document.body.scrollTop;
    dragObj.style.left = x; 
    dragObj.style.top = y;
    var group1Pos = getObjPosition(group1);
    var group2Pos = getObjPosition(group2);
    var group3Pos = getObjPosition(group3);
    if (x >= group1Pos.x && x <= group1Pos.x + group1.offsetWidth) {  
      moveDBack(group1,y);
    } else if (x >= group2Pos.x && x <= group2Pos.x + group2.offsetWidth) {
      moveDBack(group2,y);
    } else if (x >= group3Pos.x && x <= group3Pos.x + group3.offsetWidth) {
      moveDBack(group3,y);
    }         
  } 
} 
function beginDrag(evt) { 
  dragObj = window.event ? event.srcElement.parentNode : evt.target.parentNode; 
  if (dragapproved == false && dragObj.className == "drag") {
    dBack = dragObj.cloneNode(false);
    dBack.className = "dBack";  
    var pos = getObjPosition(dragObj);
    dragObj.className = "draging";
    dragObj.style.left = pos.x;
    dragObj.style.top = pos.y;
    offX = window.event ? event.offsetX : evt.clientX - pos.x; 
    offY = window.event ? event.offsetY : evt.clientY - pos.y;
    dragObj.parentNode.insertBefore(dBack,dragObj);
    dragapproved = true;  
  } 
}
function moveDBack(obj,y) {
  var length = obj.childNodes.length;
  var index = length;
  for (var i=0;i<length;i++) {
    var childPos = getObjPosition(obj.childNodes[i]);
    if (obj.childNodes[i] == dragObj) continue;
    if (y <= childPos.y + Math.floor(obj.childNodes[i].offsetHeight/2)) {
      index = i;
      break;
    } 
  }
  if (index < length) {
    obj.insertBefore(dBack,obj.childNodes[index]);
  } else {
    obj.appendChild(dBack);
  }
}
function Point(_x,_y) {    
  this.x = _x;    
  this.y = _y;    
}    
function getObjPosition(obj) {    
  var pos = new Point(0,0);    
  while (obj) {    
    pos.x += obj.offsetLeft;    
    pos.y += obj.offsetTop;    
    obj = obj.offsetParent;    
  }    
  return pos;    
}
var ctx = document.getElementById("myChart").getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});

// function rememberLayout() {
//   var str = "";
//   for (var i=1;i<=3;i++) {
//     var group = document.getElementById("group"+i);
//       var arr = new Array();
//     for (var j=0;j<group.childNodes.length;j++) {
//       arr.push(group.childNodes[j].id);
//     }
//     str += arr.join(",") + (i == 3 ? "" : ":");
//   }
//   setDashboardOrder("iGoogle",str,30);
// }

// function setDashboardOrder(cookieName,cookieValue,nDays) { //nDays:有效天數    
//     var today = new Date();    
//     var expire = new Date();    
//     if (nDays != null && nDays > 0) {    
//         expire.setTime(today.getTime() + 3600000*24*nDays);    
//         document.cookie = cookieName + "=" + escape(cookieValue) + ";expires=" + expire.toUTCString();    
//     } else {    
//         document.cookie = cookieName + "=" + escape(cookieValue);    
//     }       
// }

// function setLayout() {
//   var str = getDashboardOrder("iGoogle");
//   if (str == undefined) return;
//   var arr1 = str.split(":");
//   for (var i=0;i<arr1.length;i++) {
//     var arr2 = arr1[i].split(",");
//     for (var j=0;j<arr2.length;j++) {
//       document.getElementById("group"+(i+1)).appendChild(document.getElementById(arr2[j]));
//     }
//   }
// }

// function getDashboardOrder(cookieName) {    
//   var allcookies = document.cookie;    
//     cookieName += "=";    
//     var pos = allcookies.indexOf(cookieName);    
//     if( pos != -1) {    
//         var start = pos + cookieName.length;    
//         var end = allcookies.indexOf(";",start);    
//         if(end == -1) end = allcookies.length;    
//         return unescape(allcookies.substring(start,end));     
//     }    
// }
// setLayout();