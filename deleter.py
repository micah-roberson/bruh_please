import pandas as pd

# Read the CSV file
df = pd.read_csv('meal_plans_300.csv')

# Columns to check for blanks
columns_to_check = ['Breakfast 1', 'Breakfast 2', 'Lunch 1', 'Lunch 2', 'Lunch 3', 'Lunch 4',
                     'Dinner 1', 'Dinner 2', 'Dinner 3', 'Dinner 4']

# Remove rows with blanks in specified columns
df_cleaned = df.dropna(subset=columns_to_check)

# Export the cleaned DataFrame to a new CSV file
df_cleaned.to_csv('meal_plans_300C.csv', index=False)

print("Cleaning complete. The cleaned data has been exported to 'your_output_file.csv'.")
