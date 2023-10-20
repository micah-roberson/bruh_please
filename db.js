
const Pool = require("pg").Pool;
const pool = new Pool({
    //user: "postgres",
    user: "postgres",
    host: "172.31.13.187",
    //password: "password",
    password: "password",
    //host: "localhost",
    port: 5432,
    database: "postgres"
});

module.exports = pool;

