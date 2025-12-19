require('dotenv').config()
const { Sequelize, DataTypes } = require('sequelize');
const db = {};

const DBNAME = process.env.DBNAME ;
const DBUSER = process.env.DBUSER;
const DBPASS = process.env.DBPASS ;
const DBHOST = process.env.DBHOST;
const sequelize = new Sequelize(DBNAME, DBUSER, DBPASS, {
    host: DBHOST,
    dialect: 'mysql',
});

sequelize
  .authenticate()
  .then(() => {
    console.log('Connection has been established successfully.');
  })
  .catch(err => {
    console.error('Unable to connect to the database:', err);
    const DBNAME = process.env.DBNAME;
    const DBUSER = process.env.DBUSER ;
    const DBPASS = process.env.DBPASS ;
    const DBHOST = process.env.DBHOST ;
    console.log(DBNAME);
    console.log(DBUSER);
    console.log(DBPASS);
    console.log(DBHOST);
  });
  db.sequelize = sequelize;
  db.Sequelize = Sequelize;
  module.exports = db;