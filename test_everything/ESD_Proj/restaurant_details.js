

const app = Vue.createApp({
    data() {
        return {
            name:"",
            cuisine:"", 
            location:"",
            operating_hours:"",
            image:"",
            email:"",
            contact:"", 
            restaurant_username:"",
            googleMapsPlaceId: "", 
            googleMapsKey: "", //Enter api key here
            mapEmbedUrl: "",
            user_username: ""
        };
    },
    methods: {
        async fetchRestaurantDetails() {
            const url = `https://personal-wh7faulr.outsystemscloud.com/RestaurantAPI/rest/v1/Restaurant/${this.restaurant_username}/`;
            const response = fetch(url).then(response => response.json())
            .then(data => {
                result = data["Restaurant"];
                console.log(result)
                this.operating_hours = result.Opening_hours;
                this.location = result.Location;
                this.name = result.Name;
                this.email = result.email;
                this.cuisine = result.Cuisine;
                this.image = result.Title_image;
                this.contact = result.Contact
                this.googleMapsPlaceId = result.place_id;
                this.mapEmbedUrl ="https://www.google.com/maps/embed/v1/place?key=" + this.googleMapsKey + "&q=place_id:" + this.googleMapsPlaceId;
                localStorage.setItem("restaurant_name",this.name)
            })
        },
    },
    created(){
        this.restaurant_username = localStorage.getItem('restaurant_username')
        console.log(this.restaurant_username)
        var token = localStorage.getItem('token');
        fetch('http://localhost:4000/users/validatetoken', {
            method: 'GET',
            headers: {
                'x-auth-token': token,
            },
        })
            .then(response => response.json())
            .then(data => {
                this.user_username = data.data.Username;
                // Assuming successful login, display user token
              //assign to variable
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    },
    mounted() {
        this.fetchRestaurantDetails();
    }
})
app.mount('#app');
