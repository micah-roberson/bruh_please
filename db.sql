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

DROP TABLE IF EXISTS recipes_macros;


CREATE TABLE recipes_macros (
    "recipe name" VARCHAR(255),
    Category VARCHAR(255),
    Description TEXT,
    Instructions TEXT,
    "Grocery Items" TEXT,
    "Grocery Quantities" TEXT,
    "Grocery Types" TEXT,
    "Total Time" VARCHAR(40),
    "Serving Size" INT,
    "Fused Grocery" TEXT,
    "Total Calories" DECIMAL(10,2),
    "Total Protein" DECIMAL(10,2),
    "Total Fat" DECIMAL(10,2),
    "Total Carbs" DECIMAL(10,2),
    "Total Cost" DECIMAL(10,2),
    "Recipe Filter" VARCHAR(255),
    "Total Time Mins" INT
);


-- Drop the meal_plan_20k table if it exists
DROP TABLE meal_plan_20k;

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
    "Total Cost" numeric,
    "Total Time" numeric,
    "Total Servings" numeric,
    "Unique Grocery Items" text,
    "Filter" text,
    "Calories Ratio" text,
    "Unique Items Count" numeric
);
DROP TABLE IF EXISTS recipes_page;

CREATE TABLE recipes_page (
    type VARCHAR(255),
    title VARCHAR(255),
    info JSON,
    recipes JSON
);

DROP TABLE IF EXISTS meal_plan_page;

CREATE TABLE meal_plan_page (
    title VARCHAR(255),
    type VARCHAR(255),
    info JSON,
    meal_plans JSON,
    dinner_1_list JSON,
);

\copy recipes_page FROM '/home/ec2-user/bruh_please/recipes_page.csv' DELIMITER ',' CSV HEADER;

\copy meal_plan_page FROM '/home/ec2-user/bruh_please/mealplan_page2.csv' DELIMITER ',' CSV HEADER;


\copy meal_plan_20k FROM '/home/ec2-user/bruh_please/meal_plans_final_v1_names.csv' DELIMITER ',' CSV HEADER;

\copy recipes_macros FROM '/home/ec2-user/bruh_please/recipes_with_macros_filter.csv' DELIMITER ',' CSV HEADER;

