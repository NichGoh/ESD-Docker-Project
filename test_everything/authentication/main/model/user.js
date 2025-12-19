const { Sequelize, DataTypes } = require('sequelize');
const db = require("../database/db");

// Define User model
const User = db.sequelize.define('users', {
    Username: {
        type: DataTypes.STRING,
        primaryKey: true,
    },
    Email: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    Name: {
        type: DataTypes.STRING,
    },
    PasswordHash: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    PasswordSalt: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    UserType: {
        type: DataTypes.ENUM("restaurant_owner", "user"),
        allowNull: false,
    },
    Token: {
        type: DataTypes.STRING,
    },
});

module.exports = User;