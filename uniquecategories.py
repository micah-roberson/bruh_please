import csv
from collections import defaultdict

# Read the CSV file
input_file = 'temp3.csv'
output_file = 'temp4.csv'

with open(input_file, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    
    # Use defaultdict to store unique values and their counts
    unique_values = defaultdict(int)
    
    for row in reader:
        filters = row['Filter'].split(',')
        
        # Update the count for each value
        for value in filters:
            unique_values[value] += 1

# Filter values that occur more than 20 times
filtered_values = [value for value, count in unique_values.items() if count > 20]

# Write the filtered values to a new CSV file
with open(output_file, 'w', newline='') as csv_out:
    writer = csv.writer(csv_out)
    
    # Write the header
    writer.writerow(['Filtered Values'])
    
    # Write each filtered value as a row
    for value in filtered_values:
        writer.writerow([value])
