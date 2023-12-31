import csv
import openai
from tqdm import tqdm

# Set up OpenAI API credentials
openai.api_key = ''

# Function to predict category based on meal names
def predict_category(meal_data, engine):
    categories = []
    for data in tqdm(meal_data, desc="Predicting Categories"):
        retries = 0
        while retries < 5:
            try:
                response = openai.Completion.create(
                    engine=engine,
                    prompt=f"Based on the recipe name: {data['recipe name']} and ingredients: {data['Grocery Items']} choose what the categories(max of six categories) the recipe belongs to. these are your categories ' One-Pot Meals, Grilling,Italian, Mexican, Asian, Mediterranean, American, Indian, Middle Eastern, French, Thai, Japanese,Beginner-Friendly, Intermediate Cooking, Advanced Culinary Creations, Quick and Simple, Gourmet Delights, Family-Friendly, Cooking for Singles, Cooking with Kids, Date Night Dinners, Chicken Creations, Seafood Spectacular, Pasta Perfection, Veggie Varieties, Rice and Grain Galore, Bean Bonanza, Eggcellent Recipes, Cheese Lover's Paradise, Quinoa Queen (or King), Avocado Adoration,Southern Comfort, Northeastern Delights, Midwest Classics, Pacific Northwest, Southwest Flavors, Coastal Cuisine, Rustic Country Fare, International Street Food, City-Inspired Dishes, Global Fusion,Low-Calorie, High-Fiber, Heart-Healthy, Weight-Loss Friendly, Nutrient-Packed, Low-Sugar, Detoxifying, Immune-Boosting, Clean Eating, Plant-Based Protein'",
                    temperature=0.3,
                    max_tokens=50,
                    n=1,
                    stop=None,
                )
                predicted_category = response.choices[0]['text'].strip().lower()
                categories.append(predicted_category)
                break  # Break the retry loop if the request is successful
            except (openai.error.ServiceUnavailableError, openai.error.APIError) as e:
                # Print error and continue to the next set of meal names
                print(f"Error predicting category for '{data['Names']}': {e}")
                categories.append(None)
                break
            except Exception as e:
                # Print error and continue to the next set of meal names
                print(f"An error occurred predicting category for '{data['Names']}': {e}")
                categories.append(None)
                break
        else:
            # If maximum retries reached, append None as the predicted category
            categories.append(None)

    return categories

# Read meal data from CSV
meal_data = []
with open('recipes_with_macros.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        meal_data.append(row)

# Predict categories based on meal names
predicted_categories = predict_category(meal_data, "text-davinci-003")

# Update the 'Filter' column in the input CSV
with open('recipes_with_macros.csv', 'r') as input_file, open('recipes_with_macros_filter.csv', 'w', newline='') as output_file:
    reader = csv.DictReader(input_file)
    fieldnames = reader.fieldnames + ['Filter']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()

    for row, category in zip(reader, predicted_categories):
        row['Filter'] = category
        writer.writerow(row)
