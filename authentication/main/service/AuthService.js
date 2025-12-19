const jwt = require('jsonwebtoken');
const User = require('../model/user');
const bcrypt = require('bcrypt');
const { Op } = require('sequelize');
const axios = require('axios'); 
class AuthService {
    constructor(secretKey) {
        this.secretKey = secretKey;
    }

    generateToken(user) {
        console.log("Generating token ", user)
        const tokenData = {
            UserID: user.Username,
            UserType: user.UserType,
            Username: user.Username,
            Email: user.Email,
            Name: user.Name
        };
        return jwt.sign(tokenData, this.secretKey, { expiresIn: '1d' });
    }


    async generateSalt(password) {
        const saltRounds = 10;
        const salt = await bcrypt.genSalt(saltRounds);
        const hashedPassword = await bcrypt.hash(password, salt);
        return { salt, hashedPassword };
    }

    async verifyToken(token) {
        try {
            const decoded = jwt.verify(token, this.secretKey);
            console.log('Decoded token:', decoded);
            return decoded;
        } catch (error) {
            throw new Error('Invalid token');
        }
    }

    async getUserFromToken(token) {
        try {
            const decoded = await this.verifyToken(token);
            const user = await User.findOne({ where: { Username: decoded.UserID } });
            return user;
        } catch (error) {
            console.error('Error getting user from token:', error);
            throw new Error('Failed to get user from token');
        }
    }
    async getUserByID(UserID) {
        try {
            // find user by ID or username or email
            const user = await User.findOne({ where: { [Op.or]: [{ Username: UserID }, { Email: UserID }] } });
            
            return user;
        }
        catch (error) {
            console.error('Error getting user from token:', error);
            throw new Error('Failed to get user from token');
        }
    }


    async registerUser(userdata) {
        try {
            // Create a new user record in the database
            const { Username, Email, Name, Password, UserType } = userdata;
            const { salt, hashedPassword } = await this.generateSalt(Password);
            const userData ={
                Username: Username,
                Name: Name,
                Email: Email,
                UserType: UserType,
                PasswordHash: hashedPassword,
                PasswordSalt: salt,
            };
            const newUser = await User.create(userData);
            return newUser;
        }
        catch (error) {
            console.error('Error creating user:', error);
            throw new Error('Failed to create user');
        }


    }
    async multipleRegisterUser() {
        // read restuandata.csv file
        const csv = require('csv-parser');
        const fs = require('fs');
        const results = [];
        const { salt, hashedPassword } = await this.generateSalt("password");

        fs.createReadStream('restuandata.csv')
            .pipe(csv({ headers: false}))
            .on('data', (data) => {
                // convert data to json object

                const userData = {
                    Username: data['0'],
                    Name: data['1'],
                    Email: data['2'],
                    UserType: "restaurant_owner",
                    PasswordHash: hashedPassword,
                    PasswordSalt: salt,
                };
                results.push(userData);
            })
            .on('end', () => {
                console.log(results);
                const newUsers =  User.bulkCreate(results);

                return newUsers;
            });
        // Create a new user record in the database
        // const { Username, Email, Name, Password, UserType } = userdata;
        // const { salt, hashedPassword } = await this.generateSalt(Password);
        // const userData ={
        //     Username: Username,
        //     Name: Name,
        //     Email: Email,
        //     UserType: UserType,
        //     PasswordHash: hashedPassword,
        //     PasswordSalt: salt,
        // };
        // const newUser = await User.create(userData);
        // return newUser
    }
    
    async syncUserswithOutsystem() {
        try {
            let [usernamesSet, outsystemUsers] = await Promise.all([this.getAllRestaurantsUsername(), this.getAllRestaurantsOutsytem()]);
            var count = 0;
            const results = [];
            const { salt, hashedPassword } = await this.generateSalt("password");
            // check if user exists in the database
            for (var i in outsystemUsers) {
                if (!usernamesSet.has(outsystemUsers[i].username)) {
                    const userData = {
                        Username: outsystemUsers[i].username,
                        Name: outsystemUsers[i].Name,
                        Email: outsystemUsers[i].email,
                        UserType: "restaurant_owner",
                        PasswordHash: hashedPassword,
                        PasswordSalt: salt,
                    };
                    results.push(userData);
                }
            //         
                    
            //     // console.log(outsystemUsers[i].username , " already exists" , usernamesSet.has(outsystemUsers[i].username)); 
            //     }
                
                
            } 
            if(results.length > 0){
                // console.log(results);
                await  User.bulkCreate(results);
            }
            
            return count;
        } catch (error) {
            console.error('Error syncing users with external system:', error);
            throw new Error('Failed to sync users with external system');
        }
    }
    async getAllRestaurantsUsername() {
        const users = await User.findAll(
            {
                attributes: ['Username'],
                where: {
                    userType: 'restaurant_owner'
                }
            }
        );
        const usernamesSet = new Set(users.map((user) => {
            return user.Username;
        }));
        return usernamesSet;
    }
    async getAllRestaurantsOutsytem() {
        const response = await axios.get('https://personal-wh7faulr.outsystemscloud.com/RestaurantAPI/rest/v1/AllRestaurants');
        // const response = await axios.get('https://mocki.io/v1/e96670c9-9d8f-45b5-ae46-411154be43bc');
        const data = response.data.Restaurant;
        return data;
    }

    async authenticateUser(UsernameOrEmail, password) {
        try {
            console.log('Login request:', UsernameOrEmail + ' ' + password);
            // Verify credentials and return a JWT token
            const user = await User.findOne({ where: { [Op.or]: [{ Username: UsernameOrEmail }, { Email: UsernameOrEmail }] } });
            if (!user) {
                throw new Error('Invalid credentials');
            }
            const isPasswordValid = await bcrypt.compare(password, user.PasswordHash);
            if (!isPasswordValid) {
                throw new Error('Invalid credentials');
            }

            // Generate and return JWT token
            const token = this.generateToken(user);
            // Update token in user table
            await User.update({ Token: token }, { where: { Username: user.Username } });

            return token;
        }
        catch (error) {
            console.error('Error authenticating user:', error);
            throw new Error('Authentication failed');
        }
    }

    async registerRestuarentANDOUTSYSTEM(userData, resturantData) {
        try{
            const user = await this.registerUser(userData);
            const place_id_param = {
                inputtype: 'textquery',
                input: resturantData.Name,
                key: ''
            };
            const place_id_response = await axios.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json', { params: place_id_param });
           
            const placeId = place_id_response.data.candidates[0].place_id;
            const price_level_param = {
                place_id: placeId,
                fields: 'price_level',
                key: '' //Add key here
            };
            const price_level_response = await axios.get('https://maps.googleapis.com/maps/api/place/details/json', { params: price_level_param });
            
            const priceLevel = price_level_response.data.result.price_level;
            const restuarantPost = {
                username: userData.Username,
                email:resturantData.email,
                Name: resturantData.Name,
                Opening_hours: resturantData.Opening_hours,
                Location: resturantData.Location,
                Cuisine: resturantData.Cuisine,
                Contact: resturantData.Contact,
                Title_image: resturantData.Title_image,
                price_level: priceLevel,
                place_id: placeId
        };
            const posttoOutsystem = await axios.post('https://personal-wh7faulr.outsystemscloud.com/RestaurantAPI/rest/v1/AddRestaurants/', restuarantPost);

            return {
                restuarantPost
            }
        }
        catch (error) {
            console.log(error);
            return error.data;
            
        }
    }

    async AddUserRestaurantsOutsytem(userdata) {
    
    }

}


module.exports = AuthService;
