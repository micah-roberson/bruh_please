const express = require("express");
const app = express();
const cors = require("cors");
const pool = require("./db");
const e = require("express");
const fetch = require('node-fetch');


// //middleware 
app.use(cors());
app.use(express.json());
global.grocery_flag = 1;

async function update_pricing(){
    if (global.grocery_flag==1){
        try {
            global.grocery_flag=0
            const alldata = await pool.query("select * from grocery")
            let op = alldata.rows
            //console.log(op)
            const store = await fetch('https://einstein-server.onrender.com/get_one/Kroger',{
                        method: "GET"
                    })
            var store_op = await store.json()
            var store_id = store_op[0]["sid"]
            //console.log(store_id)
            for(var i=0;i<op.length;i++){
                var output = 0
                try {
                    var gro_name = op[i]["name"]
                    //console.log(gro_name)
                    //console.log(op[i])
                    const updt = await fetch(`https://prices-backend.onrender.com/kroger/${gro_name}`,{
                        method: "GET"
                    })
                     output = await updt.json()
                    //console.log("output")
                    //console.log(output)
                } catch (error) {
                    output=0;
                    
                    console.log("grocery_not found")
                    continue
                    //console.log(error)
                }
                const newdata = await pool.query(" insert into prices  (price,groid,sid) values($1,$2,$3) on CONFLICT(groid) DO UPDATE SET price=EXCLUDED.price, sid = EXCLUDED.sid",[parseFloat(output["programming_languages"][0]),op[i]["groid"],parseInt(store_id)]);
            }

        } catch (error) {
            console.log(error.message);
            
        }
    }
}

//update_pricing()
// stores
//add
app.post("/add_store", async(req, res) => {
    try{
        const item = req.body;// check dupes in future
        const newdata = await pool.query(" insert into store (name) values($1) returning *",[item['name']]);
        
        res.json(newdata);
        return;
    }catch (err){
        console.log(err.message);
    }
});


// return all 
app.get("/get_stores",async(req,res) => {
    try {
        const alldata = await pool.query("select * from store")
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})
//return one
app.get("/get_one/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query("select * from store where name=$1",[data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})
//remove
app.delete("/remove_item/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query("delete from store where name=$1",[data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})

// grocery
//create
app.post("/add_grocery", async(req, res) => {
    try{
        const item = req.body;// check dupes in future
        const newdata = await pool.query(" insert into grocery (name,calories) values($1,$2) returning *",[item['name'],item['calories']]);
        res.json(newdata);
        global.grocery_flag= 1
        return;
    }catch (err){
        console.log(err.message);
    }
});
//read all
app.get("/get_groceries",async(req,res) => {
    try {
        const alldata = await pool.query("select * from grocery")
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})


//read one item
app.get("/get_one_grocery/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query("select * from grocery where name=$1",[data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})
//Read one grocery by id
app.get("/get_one_grocery_id/:id",async(req,res) => {
    try {
        const data = req.params["id"]
        const alldata = await pool.query("select name from grocery where groid=$1",[data])
        console.log(alldata)
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})
//read one calorie
app.get("/get_one_grocery_calorie/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query("select * from grocery where calories=$1",[data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})
//update 
app.put("/update_one_grocery_calorie/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const val = req.body["calories"];
        const alldata = await pool.query("update grocery set calories=$1 where name=$2",[val,data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})
//delete 
app.delete("/remove_grocery/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query("delete from grocery where name=$1",[data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})

//prices 
//recipes 
app.post("/add_recipe", async(req, res) => {
    try{
        const item = req.body;
        const num_gro = item["grocery"].length;
        
        for (let i=0;i<num_gro;i++){
            const groid = await pool.query("select groid from grocery where name = $1",[item["grocery"][i]["name"]]);
            //console.log("outside")
            //console.log(groid.rows.length)
            if(groid.rows.length==0){
                const val = await pool.query(" insert into grocery (name) values($1) returning *",[item["grocery"][i]['name']]);}
                const groid_new = await pool.query("select groid from grocery where name = $1",[item["grocery"][i]['name']]);
                //console.log("Entering grocery")
                //console.log(groid_new.rows);
                const newdata = await pool.query(" insert into recipes (name,groid,qty) values($1,$2,$3) returning *",[item['name'],groid_new.rows[0]['groid'],item['grocery'][i]["qty"]]);
            
            
    
        }
        //console.log(item["grocery"].length);
        //const newdata = await pool.query(" insert into recipes (name,calories) values($1,$2) returning *",[item['name'],item['calories']]);
        res.json(num_gro);
        return;
    }catch (err){
        console.log(err.message);
    }
});
//read all
app.get("/get_recipes",async(req,res) => {
    try {
        //const gid = await pool.query("select groid from ")
        const alldata = await pool.query("select * from recipes")
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})

app.get("/get_distinct_recipes",async(req,res) => {
    try {
        const alldata = await pool.query("select distinct name from recipes")
        res.json(alldata.rows)
    } catch(error) {
        console.log(error.message);
    }
})
//read one item
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}
app.get("/get_one_recipes_name/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query("select * from recipes where LOWER(name)=$1",[data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})

app.get("/get_one_grocery_list/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query("select g.groid,g.name,r.qty from grocery g, recipes r where LOWER(r.name)=$1 and g.groid=r.groid",[data])
        res.json(alldata.rows)
    } catch (error){
        console.log(error.message);
    }
})

//update 
app.put("/update_one_recipe_qty/:reciid",async(req,res) => {
    try {
        //const data = req.params["name"]
        const val = req.body["qty"];
        const data = req.params["reciid"]
        const alldata = await pool.query("update recipes set qty=$1 where reciid=$2",[val,data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})
app.put("/update_one_recipe_unit/:reciid",async(req,res) => {
    try {
        //const data = req.params["name"]
        const val = req.body["unit"];
        const data = req.params["reciid"]
        const alldata = await pool.query("update recipes set unit=$1 where reciid=$2",[val,data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})

//delete 
app.delete("/remove_recipe/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query("delete from recipes where reciid=$1",[data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})
//meal_plan
app.post("/add_meal_plan", async(req, res) => {
    try{
        const item = req.body;
        //console.log(item);
        const num_reci = item["recipes"].length;
        var rec = 100;
        for (let i=0;i<num_reci;i++){
            const reciid = await pool.query("select name from recipes where name = $1",[item["recipes"][i]["name"]]);
            rec = reciid
            if (reciid.rows.length!=0){
                const add_recipes = await pool.query("insert into meal_plan(name,reci_name) values($1,$2)",[item["name"],item["recipes"][i]["name"]])
            }
        }
        //res.json("done bitch");
        res.json(num_reci)
        return;
    }catch (err){
        console.log(err.message);
    }
});
//read all
app.get("/get_meal_plans",async(req,res) => {
    try {
        //const gid = await pool.query("select groid from ")
        const alldata = await pool.query("select * from meal_plan")
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})
//read all distinct 
app.get("/get_meal_plans_distinct",async(req,res) => {
    try {
        //const gid = await pool.query("select groid from ")
        const alldata = await pool.query("select distinct name from meal_plan")
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})

// read one meal plan
app.get("/get_one_meal_plan/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query("select * from meal_plan where name=$1",[data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})
// get grocery list
app.get("/get_meal_plan_grocery_list/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query("select g.name,sum(r.qty),r.unit from grocery g,recipes r,meal_plan m where m.name=$1 and m.reci_name=r.name and g.groid = r.groid group by g.name,r.unit;",[data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})

//delete 
//all items 
app.delete("/remove_meal_plan/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query("delete from meal_plan where name=$1",[data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
});
//delete one recipe
app.delete("/remove_one_meal_plan_recipe/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const val = req.body["recipe"]
        const alldata = await pool.query("delete from meal_plan where name=$1 and reci_name = $2",[data,val])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
});
//add recipe description
app.post("/add_recipe_description",async(req,res) => {
    try {
        const item = req.body
        //console.log(item)
        const reciname = item['recipes']
        const desc = item['descr']
        //console.log(reciname)
        //console.log(desc)
        const newdata = await pool.query(" insert into descriptor (reciname,descr) values ($1,$2) on conflict(reciname) do update set descr=EXCLUDED.descr",[reciname,desc])
        res.json(newdata.rows)
    } catch (error) {
        console.log(error.message);
    }
})
// get descriptions
app.get("/get_description/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query("select descr from descriptor where reciname=$1",[data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})

//make groups
app.post("/add_groups",async(req,res) => {
    try {
        const item = req.body
        //console.log(item)
        const reciname = item['name']
        const desc = item['meal']
        //console.log(reciname)
        //console.log(desc)
        const newdata = await pool.query(" insert into groups (name,meal) values ($1,$2) ",[reciname,desc])
        res.json(newdata.rows)
    } catch (error) {
        console.log(error.message);
    }
})

// new recipes

app.get("/send_everything_in_name/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query(`select * from recipes_motherload where "recipe name" =$1`,[data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})

// all meal plans



// macros

app.get("/macros_per_recipe/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query(`select * from recipes_macros where "recipe name" =$1`,[data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})

// ingredients

app.get("/ingredients_split/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query(`select * from recipes_ingredients where "Ingredient" =$1`,[data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})

// ingredients

app.get("/meal_plan_20k/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query(`select * from meal_plan_20k where "Names"=$1`,[data])
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})

app.get("/",async(req,res) => {
    try {
        
        const alldata = await pool.query(`select distinct("recipe name") as names from recipes_macros;`)
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})

app.get("/meal_plans_list",async(req,res) => {
    try {
        
        const alldata = await pool.query(`select distinct("Names") as names from meal_plan_20k;`)
        res.json(alldata.rows)
    } catch (error) {
        console.log(error.message);
    }
})

app.get("/meal_plans_within_limit/:param1/:param2", async (req, res) => {
    try {
        const param1 = req.params["param1"];
        const param2 = req.params["param2"];
        //const param3 = req.params["param3"];
        
        const alldata = await pool.query(
            `select * from meal_plan_20k where "Total Cost">$1 and "Total Cost"< $2`,
            [param1, param2]
        );

        res.json(alldata.rows);
    } catch (error) {
        console.log(error.message);
        res.status(500).send("Internal Server Error");
    }
});


app.get("/meal_plans_paginated/:items_per_page/:page", async (req, res) => {
  try {
    const itemsPerPage = req.params["items_per_page"]; // Number of items to display per page
    const currentPage = req.params["page"] || 1; // Get the page number from query parameters

    const offset = (currentPage - 1) * itemsPerPage;

    const query = `
      SELECT *
      FROM meal_plan_20k
      LIMIT $1
      OFFSET $2;
    `;

    const { rows } = await pool.query(query, [itemsPerPage, offset]);

    res.json(rows);
  } catch (error) {
    console.error(error);
    res.status(500).send("Internal Server Error");
  }
});

// protein 
app.get("/by_protein/:items_per_page/:page", async (req, res) => {
  try {
    const itemsPerPage = req.params["items_per_page"]; // Number of items to display per page
    const currentPage = req.params["page"] || 1; // Get the page number from query parameters

    const offset = (currentPage - 1) * itemsPerPage;

    const query = `
      SELECT *
      FROM meal_plan_20k
      order by "Total Protein" DESC
      LIMIT $1
      OFFSET $2;
    `;

    const { rows } = await pool.query(query, [itemsPerPage, offset]);

    res.json(rows);
  } catch (error) {
    console.error(error);
    res.status(500).send("Internal Server Error");
  }
});


app.get("/grocery_ingredients/:name",async(req,res) => {
    try {
        const data = req.params["name"]
        const alldata = await pool.query(`select * from recipes_macros where "recipe name" =$1`,[data])
        const k = alldata.rows 
        //console.log(k[0]['Grocery Items'])
        const items = k[0]["Grocery Items"].split("\n");
        const fuseditems = k[0]["Fused Grocery"].split("\n")
        const quantities = JSON.parse(k[0]["Grocery Quantities"]);

    const output = [];
    for (let i = 0; i < items.length; i++) {
        output.push({
        "uid": i,
        "fused_grocery": fuseditems[i],
        "ingredient name": items[i],
        "quantity": quantities[i]
        });
    }
    //console.log(JSON.stringify(output, null, 2))
        res.json(output)
    } catch (error) {
        console.log(error.message);
    }
})



app.listen(5002, () => {
    console.log("working bitch")
})
