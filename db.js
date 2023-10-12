//const { Pool } = require("pg");

const Pool = require("pg").Pool;
const pool = new Pool({
    //user: "postgres",
    user: "clevercart",
    host: "localhost",
    //password: "password",
    password: "password1234",
    //host: "localhost",
    port: 5432,
    database: "einstein"
});

module.exports = pool;
