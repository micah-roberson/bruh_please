import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('recipes_with_macros.csv')  # Replace 'your_file.csv' with the path to your CSV file

# Filter and create a DataFrame for recipes with null values only
recipes_with_null = df[df.isnull().any(axis=1)]

# Export recipes with null values to a CSV file
recipes_with_null.to_csv('recipes_with_null.csv', index=False)

# Filter and create a DataFrame for recipes without null values
recipes_without_null = df.dropna()

# Export recipes without null values to a CSV file
recipes_without_null.to_csv('recipes_without_null.csv', index=False)
