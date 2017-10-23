

var search_box = new Vue({
    el:"#app",
    data:{
      search_word: ""
    },
    delimiters: ["[[","]]"],

    methods: {
      submit: function (msg) {
        axios.get("../ear_data",{
        params: {
          search: this.search_word
        }
        }).then(response => this.items = response.data.datalist);
        
      }
    }
   
  })

//http://127.0.0.1:8000/ear_data/?search=28&order=asc&offset=0&limit=10
//http://127.0.0.1:8000/ear_data/?search=28&order=asc&offset=0&limit=10
//http://127.0.0.1:8000/ear_data/?search=%s&order=asc&limit=10