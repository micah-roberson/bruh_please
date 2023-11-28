import os
import re
import pandas as pd

# Step 1: Read the existing CSV file
input_file_path = 'recipe_names_for_images copy.csv'  # Update with your actual file path
df = pd.read_csv(input_file_path)

# Step 2: Generate image file paths and check for existence
output_directory = './out4/'
missing_images = []

for index, row in df.iterrows():
    recipe_name = row['recipe name']
    clean_recipe_name = re.sub(r'[ /\\?!]', '_', recipe_name)
    image_file_path = f'{output_directory}txt2img_{clean_recipe_name}_0.png'

    if not os.path.isfile(image_file_path):
        missing_images.append(recipe_name)

# Step 3: Create a new CSV file with missing recipe names
output_file_path = 'missing_images_spreadsheet3.csv'  # Update with your desired output file path
missing_df = pd.DataFrame({'Missing Recipe Names': missing_images})
missing_df.to_csv(output_file_path, index=False)

print(f"Missing images have been saved to {output_file_path}")

