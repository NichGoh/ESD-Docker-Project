// index.js
const cors = require('cors');
const express = require('express');
const authRoute = require('./main/routes/authRoute');
const bodyparser = require('body-parser');
require('dotenv').config()

const app = express();
const PORT = process.env.PORT || 4000;
app.use(bodyparser.json());
app.use(bodyparser.urlencoded({extended: true}));
app.use(cors());

// Other middleware and routes...
// home page display app_test/index.html
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/app_test/index.html');
});
app.get('/login', (req, res) => {
    res.sendFile(__dirname + '/app_test/login.html');
});
app.get('/profile', (req, res) => {
    res.sendFile(__dirname + '/app_test/profile.html');
});
app.get('/register', (req, res) => {
    res.sendFile(__dirname + '/app_test/register.html');
});
app.use('/users', authRoute); // Use the auth route

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

