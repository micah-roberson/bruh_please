import csv
import requests
import time
import re
import os
import base64
from tqdm import tqdm
from retrying import retry

# Define the API endpoint and your API key
api_url = "https://api.stability.ai/v1/generation/stable-diffusion-512-v2-1/text-to-image"
api_key = "sk-OazLsYEiEPhCK4L9uAUeWxa9X6pzhe5yDhB2ZCg2Y4kHrclq"  # Replace with your API key

# Function to generate images using the new API with retries on network errors
@retry(wait_fixed=2000, stop_max_attempt_number=3)
def generate_images_with_retry(prompt, n=1, size="512x512"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "steps": 40,
        "width": 512,
        "height": 512,
        "seed": 0,
        "cfg_scale": 5,
        "samples": 1,
        "text_prompts": [
            {
                "text": prompt,
                "weight": 1
            },
            {
                "text": "blurry, bad, not a recipe, food, dessert, drink, appetizer, eddible,",
                "weight": -1
            }
        ],
    }
    response = requests.post(api_url, json=data, headers=headers, timeout=30)
    response.raise_for_status()  # Raise an exception for non-200 status codes
    return response.json()

# Define the output directory
output_directory = "./out3/"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Read ingredients from CSV
recipe_info = []
with open('recipe_names_for_images copy.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        if len(row) >= 3:  # Check if there are at least three columns
            recipe_name, category, description = row[:3]  # Only unpack the first three values
            recipe_info.append({
                'recipe name': recipe_name,
                'Category': category,
                'Description': description
            })
# Generate images and save them to the output directory with checkpointing
generated_images = []

checkpoint_file = "processing_checkpoint.txt"

if os.path.exists(checkpoint_file):
    with open(checkpoint_file, "r") as checkpoint:
        processed_ingredients = checkpoint.read().splitlines()
else:
    processed_ingredients = []

for recipe in recipe_info:
    recipe_name = recipe['recipe name']
    category = recipe['Category']
    description = recipe['Description']
    # Modify recipe name to remove spaces and special characters
    recipe_name_mod = re.sub(r'[\s\\/?!]+', '', recipe_name)

    # Create the prompt
    prompt = f"{'recipe name'} Its category {category}. Its description {description}"

    if recipe_name_mod not in processed_ingredients:
        try:
            image_data = generate_images_with_retry(prompt)
            if "artifacts" in image_data:
                image_base64 = image_data["artifacts"][0]["base64"]
                # Save the image to a file in the output directory
                with open(os.path.join(output_directory, f"txt2img_{recipe_name_mod}.png"), "wb") as img_file:
                    img_file.write(base64.b64decode(image_base64))
                generated_images.append((recipe_name_mod, os.path.join(output_directory, f"txt2img_{recipe_name_mod}.png")))
            else:
                generated_images.append((recipe_name_mod, "Failed to generate image"))
        except Exception as e:
            print(f"Error processing {recipe_name_mod}: {str(e)}")
        processed_ingredients.append(recipe_name_mod)
        with open(checkpoint_file, "a") as checkpoint:
            checkpoint.write(recipe_name_mod + "\n")
# Write generated image file paths to CSV


# Write generated image file paths to CSV with modified recipe names
with open('generated_images_final6.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Recipe Name', 'Image Path'])
    for recipe_name_mod, image_path in generated_images:
        writer.writerow([recipe_name_mod, image_path])

print("Image generation complete!")
