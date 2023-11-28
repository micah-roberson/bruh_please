import pandas as pd

# Step 1: Read the first CSV file with only 'recipe name'
file_path_1 = 'missing_images_spreadsheet.csv'  # Update with your actual file path
df1 = pd.read_csv(file_path_1)

# Step 2: Read the second CSV file with 'recipe name', 'category', and 'description'
file_path_2 = 'recipe_names_for_images copy 3.csv'  # Update with your actual file path
df2 = pd.read_csv(file_path_2)

# Step 3: Merge the dataframes based on 'recipe name'
merged_df = pd.merge(df1, df2, on='recipe name', how='left')

# Step 4: Remove duplicates based on 'recipe name'
merged_df = merged_df.drop_duplicates(subset='recipe name')

# Step 4: Save the merged dataframe to a new CSV file
output_file_path = 'merged_data.csv'  # Update with your desired output file path
merged_df.to_csv(output_file_path, index=False)

print(f"Merged data has been saved to {output_file_path}")
