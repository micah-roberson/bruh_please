import pandas as pd
import random

# Read the original CSV file
df = pd.read_csv('recipes_with_macros_filter copy.csv')

# Drop rows with missing values in the 'Filter' column
df = df.dropna(subset=['Filter'])

# Define the filters
filters = ['middle eastern', 'beginner-friendly', 'high-fiber', 'grilling', 'mexican',
           'family-friendly', 'quick meals', 'mediterranean', 'bean bonanza',
           'international street food', 'eggcellent recipes', 'indian', 'asian',
           'date night dinners', 'gourmet delights', 'rice and grain galore',
           'southern comfort', 'italian', 'pasta perfection', 'chicken creations',
           'beef dishes', 'cajun', 'seafood spectacular', 'french', 'global fusion',
           'japanese', 'beginner-friendly ', 'italian ', 'grilling ', 'european',
           'northeastern delights', 'southwest flavors', 'coastal cuisine', 'detoxifying',
           'immune-boosting', 'comfort food', 'southern comfort ', 'date night dinners ',
           'american', 'german', 'thai', 'american']

# Create a dictionary to store 20 recipes for each filter
filtered_recipes = {filter_name: [] for filter_name in filters}

# Iterate through each filter and randomly select 20 recipes
for filter_name in filters:
    recipes_for_filter = df[df['Filter'].str.contains(filter_name, case=False)]['recipe name'].tolist()
    selected_recipes = random.sample(recipes_for_filter, min(20, len(recipes_for_filter)))
    filtered_recipes[filter_name] = selected_recipes + [''] * (20 - len(selected_recipes))

# Create a list to store DataFrames
dfs = []

# Populate the list with DataFrames for each filter
for filter_name, recipes in filtered_recipes.items():
    info_array = []
    for recipe_name in recipes:
        if recipe_name:
            recipe_info = df[df['recipe name'] == recipe_name][['Total Calories', 'Total Protein', 'Total Fat', 'Total Carbs', 'Total Cost']].values.tolist()
            info_array.append(recipe_info[0])  # Assuming each recipe name is unique
        else:
            info_array.append(['', '', '', '', ''])
    
    # Create a DataFrame for each filter
    temp_df = pd.DataFrame({'type': filter_name, 'title': 'Recipes with ' + filter_name.capitalize(),
                            'info': [info_array], 'recipes': [recipes]})
    dfs.append(temp_df)

# Concatenate the list of DataFrames into the final result
result_df = pd.concat(dfs, ignore_index=True)

# Save the result to a new CSV file
result_df.to_csv('filtered_recipes.csv', index=False)