
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
                  console.log(data);
                },

                error: function(e) {
                  alert("ERROR: Data should be readable.(.json) ::"+e);
                }
              });
          })
    }
});