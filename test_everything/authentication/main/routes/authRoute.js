// authRoute.js

const express = require('express');
const AuthService = require('../service/AuthService');

const router = express.Router();
const authService = new AuthService('your-secret-key'); // Replace with your actual secret key
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
// Register a new user
router.post('/register', async (req, res) => {
    try {
        await authService.registerUser(req.body);
        const { Username, Password } = req.body;
        const token = await authService.authenticateUser(Username, Password);
        res.status(201).json({ code: 201, message: 'User registered successfully', token });
        // await sleep(2000);
        // res.status(201).json({ message: req.body });
    } catch (error) {
        console.log('Error registering user:', error);
        res.status(500).json({ error: 'Failed to register user' , code: 500});
    }
});

// Authenticate user and return JWT token
router.post('/login', async (req, res) => {
    try {

        const { Username, Password } = req.body;
        const token = await authService.authenticateUser(Username, Password);
        res.status(200).json({code: 200, token });
    } catch (error) {
        res.status(401).json({ error: 'Invalid credentials' , code: 401 });
    }
});

router.get('/validatetoken', async (req, res) => {
    try {
        const token = req.header('x-auth-token');
        const tokendata = await authService.verifyToken(token);
        res.status(200).json({
            code: 200,
            message: 'Token is valid',
            data: tokendata
        });
    } catch (error) {
        console.log('Error validating token:', error);
        res.status(401).json({ error: 'Invalid token', code: 401  });
    }

});

router.get('/getuserdetails/', async (req, res) => {
    try {
        const userID = req.query.userid || req.query.user_id;
        console.log('User ID:', userID)
        const user = await authService.getUserByID(userID);
        res.status(200).json(user);

    } catch (error) {
        console.log('Error getting user details:', error);
        res.status(500).json({ error: 'Failed to get user details' , code: 401 });
    }
});

// Secure route that requires a valid JWT token
router.get('/profile', async (req, res) => {
    try {
        const token = req.header('x-auth-token');
        const userID = await authService.verifyToken(token);
        // Fetch user profile based on userID
        // Return user data
    } catch (error) {
        res.status(401).json({ error: 'Unauthorized' });
    }
});

router.get('/multipleRegisterUser', async (req, res) => {
    try {
        await authService.multipleRegisterUser();
        res.status(200).json({ message: 'User registered successfully' });
        // Return user data
    } catch (error) {
        console.log(error)
        res.status(401).json({ error: 'Unauthorized' });
    }
});

router.get('/syncUserswithOutsystem', async (req, res) => {
    try {
        const users = await authService.syncUserswithOutsystem();
        res.status(200).json({ message: 'Synced Users', data: users });
        // Return user data
    } catch (error) {
        console.log(error)
        res.status(401).json({ error: 'Unauthorized' });
    }
});
router.post('/addRestaurent', async (req, res) => {
    try {
        // get data from request
        const userData = req.body.userData;
        const resturantData = req.body.resturantData;
        const resturant = await authService.registerRestuarentANDOUTSYSTEM(userData, resturantData);
        res.status(201).json({ message: 'data ', resturant });
    }
    catch (error) {
        console.log(error)
        res.status(401).json({ error: error });
    }
});
router.get('/registerRestuarentANDOUTSYSTEM', async (req, res) => {
    try {

        /*
        userData = {
            "Username": "asd",
            "Password": "asd",
            "Name": "asd",
            "Email": "asd",
            "UserType": "resturant_owner"
        }
        resturantData = {
            "username": "asd",
            "email": "asd",
            "Name": "",
            "Opening_hours": "asd",
            "Location": "east",
            "Cuisine": "Japanese",
            "Contact": "asd",
            "Title_image": ""
        };
        */
        const data = await authService.registerRestuarentANDOUTSYSTEM();
        res.status(200).json({ message: 'data ', data: data });
        // Return user data
    } catch (error) {
        console.log(error)
        res.status(401).json({ error: 'Unauthorized' });
    }
});
module.exports = router;
