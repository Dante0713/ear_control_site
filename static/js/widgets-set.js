// draggable_sortable_widgets
var headers = $('#accordion .accordion-header');
var contentAreas = $('#accordion .ui-accordion-content ').hide();
// var expandLink = $('.accordion-expand-all');
var draggable_sortable_widgets = $("#col_right,#col_middle,#col_left");
var draggable_sortable_widgets_name = "#col_right,#col_middle,#col_left";
function load(){
  if ( window.ActiveXObject || "ActiveXObject" in window ){
    document.getElementById('bar-chart').id='IEcanvas';
    document.getElementById('pie-chart').id='IEcanvas';
  }
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
}


// add the accordion functionality
headers.click(function() {
    var panel = $(this).next();
    var isOpen = panel.is(':visible');
 
    // open or close as necessary
    panel[isOpen? 'slideUp': 'slideDown']()
        // trigger the correct custom event
        .trigger(isOpen? 'hide': 'show');

    // stop the link from causing a pagescroll
    return false;
});

// // hook up the expand/collapse all
// expandLink.click(function(){
//     var isAllOpen = $(this).data('isAllOpen');
    
//     contentAreas[isAllOpen? 'hide': 'show']()
//         .trigger(isAllOpen? 'hide': 'show');
// });

// // when panels open or close, check to see if they're all open
// contentAreas.on({
//     // whenever we open a panel, check to see if they're all open
//     // if all open, swap the button to collapser
//     show: function(){
//         var isAllOpen = !contentAreas.is(':hidden');   
//         if(isAllOpen){
//             expandLink.text('全部收合')
//                 .data('isAllOpen', true);
//         }
//     },
//     // whenever we close a panel, check to see if they're all open
//     // if not all open, swap the button to expander
//     hide: function(){
//         var isAllOpen = !contentAreas.is(':hidden');
//         if(!isAllOpen){
//             expandLink.text('全部展開')
//             .data('isAllOpen', false);
//         } 
//     }
// });

$(function () {
    draggable_sortable_widgets.sortable({
            opacity: 0.6,
            connectWith: draggable_sortable_widgets_name,
            start: function (event, ui) {
                    ui.item.toggleClass("highlight");
            },
            stop: function (event, ui) {
                    ui.item.toggleClass("highlight");
            }
    });
    draggable_sortable_widgets.disableSelection();
});

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