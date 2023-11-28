import pandas as pd

# Load the CSV file
df = pd.read_csv('temp2.csv')

# Replace commas with a page break in the 'Filter' column
df['Filter'] = df['Filter'].str.replace('\n', ',')

# Save the updated DataFrame to a new CSV file
df.to_csv('temp3.csv', index=False)
