
const { Pool } = require("pg");
const pool = new Pool({
    //user: "postgres",
    user: "postgres",
<<<<<<< Updated upstream
    host: "172.31.13.187",
=======
    host: "localhost",
>>>>>>> Stashed changes
    //password: "password",
    password: "password",
    //host: "localhost",
    port: 5432,
    database: "postgres"
});

module.exports = pool;

