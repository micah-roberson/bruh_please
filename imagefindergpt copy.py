import base64
import requests
import os
import csv
import re

# Your API key
API_KEY = "sk-OazLsYEiEPhCK4L9uAUeWxa9X6pzhe5yDhB2ZCg2Y4kHrclq"

# Define the API URL
url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

# Create an 'out4' directory if it doesn't exist
if not os.path.exists("./out4"):
    os.makedirs("./out4")

# Create a list to keep track of image file paths
image_file_paths = []

# Read the CSV file with recipe data
with open('recipe_names_for_images copy.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        recipe_name = row['recipe name']
        category = row['Category']
        description = row['Description']

        # Clean the recipe name for the filename
        clean_recipe_name = re.sub(r'[ /\\?!]', '_', recipe_name)

        # Define the text prompt
        text_prompt = f"image of {recipe_name}. Type: {category}. Description: {description}"
        
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

# Print the list of image file paths
print("Image file paths:")
for image_path in image_file_paths:
    print(image_path)
