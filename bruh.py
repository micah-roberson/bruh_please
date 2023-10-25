import pandas as pd
import re

def remove_non_utf8(text):
    if isinstance(text, str):
        return re.sub(r'[^\x00-\x7F]+', '', text)
    else:
        return text


# Read the CSV file into a DataFrame
input_csv_file = "meal_plans_20k.csv"
output_csv_file = "meal_plans_20k1.csv"

df = pd.read_csv(input_csv_file, encoding='ISO-8859-1')

# Apply the remove_non_utf8 function to all columns
df = df.applymap(remove_non_utf8)

# Write the cleaned data to a new CSV file
df.to_csv(output_csv_file, index=False)

print("Cleaning and export complete.")
