import csv

def remove_empty_rows(input_file, output_file):
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader if any(field.strip() for field in row)]

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

# Replace 'input.csv' and 'output.csv' with your file names
remove_empty_rows('recipes_with_macros_filter.csv', 'recipes_with_macros_filter.csv')
