import csv
import codecs

def remove_non_utf8(input_text):
    return input_text.encode('utf-8', 'ignore').decode('utf-8')

def clean_csv(input_file, output_file):
    with codecs.open(input_file, 'r', encoding='utf-8', errors='ignore') as infile:
        reader = csv.reader(infile)
        rows = [list(map(remove_non_utf8, row)) for row in reader]

    with codecs.open(output_file, 'w', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)

# Example usage
input_csv_file = 'meal_plans_final_v1_names.csv'
output_csv_file = 'meal_plans_final_v1_names0.csv'
clean_csv(input_csv_file, output_csv_file)
