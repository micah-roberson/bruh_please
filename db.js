//const { Pool } = require("pg");

const Pool = require("pg").Pool;
const pool = new Pool({
    //user: "postgres",
    user: "clevercart",
    host: "clevercart-app.cfmc8shzhut6.us-east-2.rds.amazonaws.com",
    //password: "password",
    password: "password1234",
    //host: "localhost",
    port: 5432,
    database: "einstein"
});

module.exports = pool;
