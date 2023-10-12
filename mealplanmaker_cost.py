import random
import csv

def load_recipes(file_path):
    recipes = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            recipes.append(row)
    return recipes

def create_meal_plan(recipes, meal_type, count):
    sorted_recipes = sorted(recipes, key=lambda x: float(x['price']))  # Sort recipes by price in ascending order
    meal_plan = sorted_recipes[:count]
    for recipe in meal_plan:
        recipe['Category'] = meal_type
    return meal_plan

def generate_weekly_meal_plan(recipes):
    breakfasts = [recipe for recipe in recipes if recipe['Category'] == 'breakfast']
    lunches = [recipe for recipe in recipes if recipe['Category'] == 'lunch']
    dinners = [recipe for recipe in recipes if recipe['Category'] == 'dinner']
    
    meal_plan = []
    total_calories = 0
    
    # Generate breakfasts
    for _ in range(7):
        breakfasts_count = random.randint(1, 2)  # Randomly select 1 or 2 breakfasts
        selected_recipes = create_meal_plan(breakfasts, 'breakfast', breakfasts_count)
        meal_plan.extend(selected_recipes)
        total_calories += sum(float(recipe['calories']) for recipe in selected_recipes)
    
    # Generate lunches
    for _ in range(4):
        lunches_count = random.randint(1, 2)  # Randomly select 1 or 2 lunches
        selected_recipes = create_meal_plan(lunches, 'lunch', lunches_count)
        meal_plan.extend(selected_recipes)
        total_calories += sum(float(recipe['calories']) for recipe in selected_recipes)
    
    # Generate dinners
    for _ in range(4):
        dinners_count = random.randint(1, 2)  # Randomly select 1 or 2 dinners
        selected_recipes = create_meal_plan(dinners, 'dinner', dinners_count)
        meal_plan.extend(selected_recipes)
        total_calories += sum(float(recipe['calories']) for recipe in selected_recipes)
    
    # Adjust calories to reach the target
    calories_difference = 14000 - total_calories
    if calories_difference > 0:
        # Add random recipes with low calories to increase the total
        all_recipes = breakfasts + lunches + dinners
        while calories_difference > 0:
            random_recipe = random.choice(all_recipes)
            meal_plan.append(random_recipe)
            total_calories += float(random_recipe['calories'])
            calories_difference = 14000 - total_calories
    
    return meal_plan

def export_meal_plan_to_csv(meal_plan, file_path):
    fieldnames = ['Day', 'Category', 'Recipe Name', 'Price']
    
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for day, recipe in enumerate(meal_plan, start=1):
            writer.writerow({'Day': day, 'Category': recipe['Category'], 'Recipe Name': recipe['Recipe Name'], 'Price': recipe['price']})

# Example usage
recipes_file = 'recipes.csv'
weekly_meal_plan = generate_weekly_meal_plan(load_recipes(recipes_file))
output_file = 'meal_plan.csv'

export_meal_plan_to_csv(weekly_meal_plan, output_file)
print(f"Meal plan exported to {output_file} successfully.")
