var input_box = $("#search_box #inputTarget");

$("#inputTarget").keypress(function(e){
  code = (e.keyCode ? e.keyCode : e.which);
  if (code == 13)
  {$(function(e) {    
              $.ajax({
                url: "http://127.0.0.1:8000/ear_data/",
                type: "GET",
                dataType: "json",
                data: {search:$("#inputTarget").val(),limit:"-1"},
                success: function(data) {
                  var i = 0;
                  //這裡改用.each這個函式來取出JData裡的物件
                  $.each(data, function() {
                    //呼叫方式也稍微改變了一下，意思等同於上述的的JData[i]["idx_Key"]
                    $("#JSON_table").append("<tr>" +
                                            "<td>" + JData[i].name   + "</td>" +
                                            "<td>" + JData[i].age    + "</td>" +
                                            "<td>" + JData[i].height + "</td>" +
                                            "</tr>");
                    i++;
                  });
                },

                error: function(e) {
                  alert("ERROR: Data should be readable.(.json) ::"+e);
                }
              });
          })
    }
});

