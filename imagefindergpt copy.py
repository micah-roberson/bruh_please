import base64
import requests
import os
import csv
import re
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Your API key
API_KEY = ""

# Define the API URL
url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

# Create an 'out4' directory if it doesn't exist
if not os.path.exists("./out4"):
    os.makedirs("./out4")

# Create a list to keep track of image file paths
image_file_paths = []

# Get the total number of rows in the CSV file for the progress bar
total_rows = sum(1 for row in csv.DictReader(open('missing_images_spreadsheet2.csv')))

# Initialize the tqdm progress bar
progress_bar = tqdm(total=total_rows, desc="Processing")

# Define a function for making API requests
def process_row(row):
    recipe_name = row['recipe name']


    # Clean the recipe name for the filename
    clean_recipe_name = re.sub(r'[ /\\?!\'"]', '_', recipe_name)

    # Define the text prompt
    text_prompt = f"image of {recipe_name}. this is recipe"

    # Create the request body
    body = {
        "steps": 40,
        "width": 1024,
        "height": 1024,
        "seed": 0,
        "cfg_scale": 5,
        "samples": 1,
        "text_prompts": [
            {
                "text": text_prompt,
                "weight": 1
            },
            {
                "text": "blurry",
                "weight": -1
            }
        ],
    }

    # Set up headers with your API key
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    # Send a request to the Stable API
    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        raise Exception(f"Non-200 response for '{recipe_name}': {response.text}")

    data = response.json()

    # Save the generated image with the cleaned recipe name as the filename
    for i, image in enumerate(data["artifacts"]):
        image_file_path = f'./out4/txt2img_{clean_recipe_name}_{i}.png'
        with open(image_file_path, "wb") as f:
            f.write(base64.b64decode(image["base64"]))
        image_file_paths.append(image_file_path)

    # Update the progress bar
    progress_bar.update(1)

# Read the CSV file with recipe data
with open('missing_images_spreadsheet2.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(process_row, csv_reader)
        
# Close the progress bar
progress_bar.close()

# Print the list of image file paths
print("Image file paths:")
for image_path in image_file_paths:
    print(image_path)
