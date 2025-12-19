const get_all_surveys_URL = "http://localhost:5004/survey";
const app = Vue.createApp({
    data() {
        return {
            username: "",
            pref_cuisine: "",
            pref_price: "",
            pref_location: "",
            newSurvey: true,
            message: "There is trouble retrieving pref data, please try again"
        };
    },
    methods: {
        getPrefbyUsername () {
            const response = 
                fetch(`${get_all_surveys_URL}/${this.username}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.code === 404) {
                            //no user pref in db
                            this.message = data.message
                            this.newSurvey = true
                        } else {
                            this.newSurvey = false
                        }
                    })
                    .catch(error => {
                        console.log(this.message + error)
                    })
        },
        createUserPref () {
            let jsonData = JSON.stringify({
                username: this.username,
                pref_cuisine: this.pref_cuisine,
                pref_location: this.pref_location,
                pref_price: this.pref_price
            })

            fetch(`${get_all_surveys_URL}`,
                {
                    method: "POST",
                    headers: {
                        "Content-type": "application/json"
                    },
                    body: jsonData
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    result = data.data;
                    console.log(result);
                })
        },
        updateUserPref () {
            let jsonData = JSON.stringify({
                username: this.username,
                pref_cuisine: this.pref_cuisine,
                pref_location: this.pref_location,
                pref_price: this.pref_price
            })

            fetch(`${get_all_surveys_URL}/${this.username}`,
                {
                    method: "PUT",
                    headers: {
                        "Content-type": "application/json"
                    },
                    body: jsonData
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    result = data.data;
                    console.log(result);
                })
        }
    },
    created() {
        var token = localStorage.getItem('token');
        fetch('http://localhost:4000/users/validatetoken', {
            method: 'GET',
            headers: {
                'x-auth-token': token,
            },
        })
            .then(response => response.json())
            .then(data => {
                this.username = data.data.Username;
                console.log(this.username)
                this.getPrefbyUsername();
                // Assuming successful login, display user token
              //assign to variable
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        
        
    }
});
app.mount('#app')