import csv
import json

def transform_csv(input_csv_path, output_csv_path):
    # Read the input CSV file
    with open(input_csv_path, 'r', encoding='utf-8-sig', errors='replace') as input_file:
        reader = csv.DictReader(input_file)
        data = list(reader)

    # Process data for each row
    transformed_data = []
    for row in data:
        row_filter = row['Filter'].strip()

        # Skip empty rows
        if not row['Names']:
            continue

        names_str = row['Names'].strip()

        try:
            names = json.loads(names_str)
        except json.decoder.JSONDecodeError:
            # If JSON decoding fails, treat it as plain text
            names = [names_str]

        # Extract specific information as integers
        total_calories = float(row['Total Calories'])
        total_protein = float(row['Total Protein'])
        total_fat = float(row['Total Fat'])
        total_carbs = float(row['Total Carbs'])
        total_cost = float(row['Total Cost'])
        total_time = int(row['Total Time'])
        total_servings = int(row['Total Servings'])

        # Create a dictionary for each row in the transformed format
        transformed_row = {
            'type': 'moms',
            'title': row_filter,
            'info': [
                total_calories,
                total_protein,
                total_fat,
                total_carbs,
                total_cost,
                total_time,
                total_servings
            ],
            'meal_plans': names
        }

        transformed_data.append(transformed_row)

    # Write the transformed data to the output CSV file
    fieldnames = ['type', 'title', 'info', 'meal_plans']
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transformed_data)

# Replace 'your_input_file.csv' and 'your_output_folder' with your actual file paths
transform_csv('meal_plans_final_v1_names copy.csv', 'your_output_folder.csv')
