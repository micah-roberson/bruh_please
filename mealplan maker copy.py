import pandas as pd
import numpy as np
from tqdm import tqdm
from random import randint

# Load the recipe data
df_recipes = pd.read_csv('recipes_with_macros_filter.csv')

# Separate the recipes into breakfast, lunch, and dinner categories
df_breakfasts = df_recipes[df_recipes['Category'] == 'breakfast']
df_lunches = df_recipes[df_recipes['Category'] == 'lunch']
df_dinners = df_recipes[df_recipes['Category'] == 'dinner']

def select_random_recipes_with_common_filter(category_df, filter_value, num_recipes):
    # Use str.contains to filter based on the presence of the specified filter and category
    filtered_recipes = category_df[
        (category_df['Filter'].str.split(',').apply(lambda x: filter_value.lower() in map(str.lower, x))) &
        (category_df['Category'] == category_df['Category'].mode()[0])
    ]
    
    # Check if the number of available recipes is less than num_recipes
    if len(filtered_recipes) < num_recipes:
        return filtered_recipes, filter_value
    else:
        # Randomly select the specified number of recipes from the filtered recipes
        return filtered_recipes.sample(num_recipes), filter_value

# Function to generate a single meal plan for one day
def generate_meal_plan(counter):
    b_num = randint(1, 2)
    l_num = randint(1, 4)
    d_num = randint(1, 4)
    # completed 'middle eastern','beginner-friendly','high-fiber','grilling','mexican','family-friendly','quick meals','mediterranean','bean bonanza','international street food','eggcellent recipes','indian','asian','date night dinners','gourmet delights','rice and grain galore',
    # Update the filter every 20 meal plans     'southern comfort','italian','pasta perfection','pork creations','chicken creations','beef dishes','cajun','seafood spectacular','french','global fusion','japanese','beginner-friendly ','italian ','grilling ','european','northeastern delights','southwest flavors','coastal cuisine','detoxifying','immune-boosting','comfort food','southern comfort ','date night dinners ','american','german','thai','american'
    if counter % 20 == 0:
        selected_filter = np.random.choice(['southern comfort','italian','pasta perfection','pork creations','chicken creations','beef dishes','cajun','seafood spectacular','french','global fusion','japanese','beginner-friendly ','italian ','grilling ','european','northeastern delights','southwest flavors','coastal cuisine','detoxifying','immune-boosting','comfort food','southern comfort ','date night dinners ','american','german','thai','american'])
    else:
        selected_filter = 'mediterranean'
    
    while True:
        # Generate meal plan
        breakfasts, _ = select_random_recipes_with_common_filter(df_breakfasts, selected_filter, b_num)
        lunches, _ = select_random_recipes_with_common_filter(df_lunches, selected_filter, l_num)
        dinners, _ = select_random_recipes_with_common_filter(df_dinners, selected_filter, d_num)
        
        # Combine recipes to create a meal plan
        meal_plan = pd.concat([breakfasts, lunches, dinners])
        
       # Check the number of unique items count
        unique_items_count = calculate_totals(meal_plan)[-1]
        
        # If the condition is met, break out of the loop
        if unique_items_count < 65:
            meal_plan_filter = ','.join(set(selected_filter.split(',')))
            return meal_plan, meal_plan_filter
        
# Function to calculate the total values for a meal plan
def calculate_totals(meal_plan):
    total_calories = meal_plan['Total Calories'].sum()
    total_protein = meal_plan['Total Protein'].sum()
    total_fat = meal_plan['Total Fat'].sum()
    total_carbs = meal_plan['Total Carbs'].sum()
    total_cost = meal_plan['Total Cost'].sum()
    total_time = meal_plan['Total Time Mins'].sum()
    total_servings = meal_plan['Serving Size'].sum()
    
    # Concatenate all the unique grocery items from the recipes
    unique_grocery_items = '\n'.join(set('\n'.join(meal_plan['Grocery Items']).split('\n')))
    
    # Calculate the ratio of each recipe's calories to the total calories
    meal_plan['Calories Ratio'] = meal_plan['Total Calories'] / total_calories
    
    # Count the number of unique items in the "Unique Grocery Items" column
    unique_items_count = len(set(unique_grocery_items.split('\n')))
    
    return total_calories, total_protein, total_fat, total_carbs, total_cost, total_time, total_servings, unique_grocery_items, list(meal_plan['Calories Ratio']), unique_items_count

# Generate 30 meal plans
total_meal_plans =  520# Change the total number of meal plans as needed
meal_plans = []
counter = 1  # Initialize the counter

columns = [
    'Breakfast 1', 'Breakfast 2', 'Lunch 1', 'Lunch 2', 'Lunch 3', 'Lunch 4',
    'Dinner 1', 'Dinner 2', 'Dinner 3', 'Dinner 4', 'Total Calories', 'Total Protein',
    'Total Fat', 'Total Carbs', 'Total Cost', 'Total Time', 'Total Servings', 'Unique Grocery Items', 'Filter', 'Calories Ratio', 'Unique Items Count'
]

for _ in tqdm(range(total_meal_plans), desc="Generating Meal Plans"):
    meal_plan, meal_plan_filter = generate_meal_plan(counter)
    total_calories = calculate_totals(meal_plan)[0]
    
    # Check if total calories are within the desired range
    while total_calories < 13000 or total_calories > 15000:
        meal_plan, meal_plan_filter = generate_meal_plan(counter)
        total_calories = calculate_totals(meal_plan)[0]
    
    totals = calculate_totals(meal_plan)
    
    # Create a dictionary to represent the meal plan
    meal_plan_dict = {}

    # Iterate over the columns and populate the meal plan dictionary
    for col in columns[:10]:
        # Extract the category and number from the column name
        category, number = col.split()
        
        # Filter recipes based on the category
        if category.lower() == 'breakfast':
            filtered_recipes = meal_plan[meal_plan['Category'] == 'breakfast']
        elif category.lower() == 'lunch':
            filtered_recipes = meal_plan[meal_plan['Category'] == 'lunch']
        elif category.lower() == 'dinner':
            filtered_recipes = meal_plan[meal_plan['Category'] == 'dinner']
        else:
            filtered_recipes = pd.DataFrame()  # Handle other categories if needed
        
        # Check if filtered_recipes is not empty
        if not filtered_recipes.empty:
            # Get the recipe name for the specified number (e.g., Breakfast 1)
            index_to_access = int(number) - 1
            # Check if index_to_access is within the bounds of the DataFrame
            if 0 <= index_to_access < len(filtered_recipes):
                recipe_name = filtered_recipes.iloc[index_to_access]['recipe name']
            else:
                recipe_name = ''  # Index out of bounds, set an empty string or handle accordingly
        else:
            recipe_name = ''  # No recipes for the specified category

        # Update the meal plan dictionary
        meal_plan_dict[col] = recipe_name

    meal_plan_dict.update(dict(zip(columns[10:], totals)))
    meal_plans.append(meal_plan_dict)
    
    # Increment the counter
    counter += 1

# Create a DataFrame with the meal plans
df_meal_plans = pd.DataFrame(meal_plans, columns=columns)

# Export the DataFrame to a CSV file
df_meal_plans.to_csv('meal_plans_520.csv', index=False)
