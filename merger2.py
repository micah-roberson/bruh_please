import pandas as pd
import ast

# Read the CSV file
df = pd.read_csv('your_output_folder.csv')

# Define a function to remove commas and single quotes from a list of strings
def clean_list(lst):
    return [item.replace(',', '').replace("'", "") for item in lst]

# Group by 'title' and aggregate the values
aggregated_df = df.groupby('title').agg({
    'type': 'first',
    'info': lambda x: [ast.literal_eval(item) for item in x],
    'meal_plans': lambda x: clean_list(sum([ast.literal_eval(item) for item in x], [])),
    'dinner_1_list': lambda x: clean_list(sum([ast.literal_eval(item) for item in x], []))
}).reset_index()

# Export the result to a new CSV file
aggregated_df.to_csv('output_file.csv', index=False)
