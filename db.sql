create database einstein;
create table store(
    sid SERIAL PRIMARY KEY,
    name varchar(50)
);

create table grocery(
    groid serial primary key,
    name varchar(255),
    calories integer
);



create table descriptor(
    did serial primary key,
    reciname varchar(255) unique,
    descr varchar(1024000)
);

create table allergen(
    aid serial primary key,
    name varchar(10) unique
);

create table groups(
    gid serial primary key,
    name varchar(30),
    meal varchar(255)
);

create table prices(
    priid serial primary key,
    price float,
    groid integer UNIQUE,
    sid integer,
    qty float,
    unit varchar(50)
);

create table recipes(
    reciid serial primary key,
    name varchar(255),
    --list_id integer,
    groid integer,
    qty float
);

create table recipes_list(
    list_id serial primary key,
    recipe name, 'Category', 'Description', 'Instructions',
       'Grocery Items', 'Grocery Quantities', 'Grocery Types', 'Total Time',
       'Serving Size', 'Total Calories', 'Total Protein (grams)',
       'Total Fats (grams)', 'Total Carbs (grams)', 'Total Price'
);

create table meal_plan(
    mealid serial primary key,
    name varchar(255),
    reci_name varchar(255)
);

CREATE TABLE recipes_ingredients (
    Ingredient text,
    dollar numeric,
    Calorie numeric,
    protein numeric,
    fat numeric,
    carbs numeric
);


CREATE TABLE recipes_macros (
    "recipe name" text,
    "Category" text,
    "Description" text,
    "Instructions" text,
    "Grocery Items" text,
    "Grocery Quantities" text,
    "Grocery Types" text,
    "Total Time" text,
    "Serving Size" integer,
    "Fused Grocery" text,
    "Total Calories" numeric,
    "Total Protein" numeric,
    "Total Fat" numeric,
    "Total Carbs" numeric,
    "Total Cost" numeric
);


CREATE TABLE meal_plan_20k (
    "Names" text,
    "Breakfast 1" text,
    "Breakfast 2" text,
    "Lunch 1" text,
    "Lunch 2" text,
    "Lunch 3" text,
    "Lunch 4" text,
    "Dinner 1" text,
    "Dinner 2" text,
    "Dinner 3" text,
    "Dinner 4" text,
    "Total Calories" numeric,
    "Total Protein" numeric,
    "Total Fat" numeric,
    "Total Carbs" numeric,
    "Total Cost" numeric
);

COPY recipes_macros FROM 'C:/Users/thebr/OneDrive/Desktop/Clever Cart/Clever Cart Code/bruh_please/ingredients_of_macros copy.csv' DELIMITER ',' CSV HEADER;

COPY meal_plan_20k FROM 'C:/Users/thebr/OneDrive/Desktop/Clever Cart/Clever Cart Code/bruh_please/meal_plans_20k copy.csv' DELIMITER ',' CSV HEADER;

COPY recipes_ingredients FROM 'C:/Users/thebr/OneDrive/Desktop/Clever Cart/Clever Cart Code/bruh_please/recipes_with_macros copy.csv' DELIMITER ',' CSV HEADER;
