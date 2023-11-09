import pandas as pd

# Read the recipes_with_null.csv file to get the names with null values
recipes_with_null_df = pd.read_csv('recipes_with_null.csv')
names_with_null = recipes_with_null_df['recipe name'].tolist()

# Read the meal plans CSV file
meal_plans_df = pd.read_csv('meal_plans_20K.csv')  # Replace 'meal_plans.csv' with the actual file name

# Define the columns to check for matching names
columns_to_check = ['Breakfast 1', 'Breakfast 2', 'Lunch 1', 'Lunch 2', 'Lunch 3', 'Lunch 4', 'Dinner 1', 'Dinner 2', 'Dinner 3', 'Dinner 4']

# Filter the meal plans DataFrame to exclude rows with names matching names_with_null in any of the specified columns
meal_plans_df = meal_plans_df[~meal_plans_df[columns_to_check].isin(names_with_null).any(axis=1)]

# Export the filtered meal plans DataFrame to a new CSV file
meal_plans_df.to_csv('filtered_meal_plans.csv', index=False)
