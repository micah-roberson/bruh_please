import pandas as pd
import ast

# Read the CSV file
df = pd.read_csv('your_output_folder.csv')

# Group by 'title' and aggregate the values
aggregated_df = df.groupby('title').agg({
    'type': 'first',
    'info': lambda x: [ast.literal_eval(item) for item in x],
    'meal_plans': lambda x: sum([ast.literal_eval(item) for item in x], []),
    'dinner_1_list': lambda x: sum([ast.literal_eval(item) for item in x], [])  # Add aggregation for dinner_1_list
}).reset_index()

# Export the result to a new CSV file
aggregated_df.to_csv('output_file.csv', index=False)
