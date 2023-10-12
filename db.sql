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