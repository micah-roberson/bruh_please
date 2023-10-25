
const { Pool } = require("pg");
const pool = new Pool({
    //user: "postgres",
    user: "postgres",
    host: "localhost",
    //password: "password",
    password: "password",
    //host: "localhost",
    port: 5432,
    database: "einstein"
});

module.exports = pool;

