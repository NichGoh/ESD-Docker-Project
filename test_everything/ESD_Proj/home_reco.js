
const main = Vue.createApp({
  // Data Properties
  data() {
      return {
          reco_restaurants : [],
          all_restaurants : [],
          user_username : "",
          recodone: false
      }
  },
  methods:{
        getuserdetails() {
          var token = localStorage.getItem('token');
          fetch('http://localhost:4000/users/validatetoken', {
              method: 'GET',
              headers: {
                  'x-auth-token': token,
              },
          })
          .then(response => response.json())
          .then(data => {
              console.log('Success:', data);
              // Assuming successful login, display user token
              // this.userData = data.data;
              this.user_username = data.data.Username;
              console.log(this.user_username)
              this.reco();
          })
          .catch((error) => {
              console.error('Error:', error);
          });
      },      
      reco(){
          console.log("helloo")
          fetch(`http://localhost:5101/recommend/${this.user_username}`,
              {
                  method:"GET",
                  headers: {
                      "Content-type": "application/json"
                  }
              })
              .then(response => response.json())
              .then(data => {
                  console.log(data)
                  console.log(data.data.all_restaurant)
                  console.log(data.data.reco_restaurant)
                  reco = data.data.reco_restaurant
                  all_rest = data.data.all_restaurant
                  this.reco_restaurants = reco;
                  this.all_restaurants = all_rest;
                  console.log("hello")
                  console.log(this.reco_restaurants.length == 0)
                  if (this.reco_restaurants.length == 0) {
                    this.recodone = false
                  } else {
                    this.recodone = true
                  }   
              })
      },
      storeData(restaurant_username){
        localStorage.setItem("restaurant_username",restaurant_username)
      }
  },
  created () {
    // Check if token exists in local storage
    const token = localStorage.getItem('token');
    if (token) {
        // Perform necessary actions if token exists
        console.log('Token exists:', token);
        this.getuserdetails();
        // Add your code here to handle the token
    } else {
        // Redirect to login page if token does not exist
        console.log('Token does not exist');
        window.location.href = './login';
    }
  }
  
})
main.component('reco-component', {

    props: [ 'name', 'cuisine', 'location', 'operating_hours','image','email','contact', 'restaurant_username'],

    template: `
    <div class="carousel-item">
      <div class="card mb-3 p-0" style="width: 650px; height:200px">
        <div class="row g-0">
          <div class="col-md-6">
            <img :src="image" class="rounded-start" style="width: 100%; height: 200px;" alt="">
          </div>
          <div class="col-md-6">
            <div class="card-body">
              <h6 class="card-title">{{name}}</h6>
              <div>
                <span class="badge badge-pill badge-secondary">{{location}}</span>
                <span class="badge badge-pill badge-secondary">{{cuisine}}</span>
              </div>
              <h6 class="card-text" style="font-size:12px">Phone: {{contact}}</h6>
              <h6 class="card-text" style="font-size:12px">Email: {{email}}</h6>
              <h6 class="card-text" style="font-size:12px">Operating hours: {{operating_hours}}</h6>
              <a href="restaurant_details.html" class="stretched-link"></a>
            </div>
          </div>
        </div>
      </div>
    </div>
    `

})

main.component('main-display-component', {
    props: ['name', 'cuisine', 'location', 'operating_hours','image','email','contact', 'restaurant_username'],

    template: `
      <div class="card mb-3 p-0" style="max-width: 650px; height:200px;">
      <div class="row g-0">
              <div class="col-md-6">
                <div class="container" style="padding:0">
                  <img :src="image" class="rounded-start"  style="width: 100%; height: 200px;" style alt="...">
                </div>  
              </div>
              <div class="col-md-6">
                  <div class="card-body">
                      <h6 class="card-title">{{name}}</h6>
                      <div>
                          <span class="badge badge-pill badge-secondary">{{location}}</span>
                          <span class="badge badge-pill badge-secondary">{{cuisine}}</span>
                      </div>
                      <h6 class="card-text" style="font-size:12px">Phone: {{contact}}</h6>
                      <h6 class="card-text" style="font-size:12px">Email: {{email}}</h6>
                      <h6 class="card-text" style="font-size:12px">Operating hours: {{operating_hours}}</h6>
                      <a href="restaurant_details.html" class="stretched-link"></a>
                  </div>
              </div>
              </div>
      </div>
    `

})
main.mount("#main")

