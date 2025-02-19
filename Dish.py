from fuzzywuzzy import process
import csv

def suggest_dishes(available_ingredients):
    suggested_dishes = []
    
    for dish, ingredients in recipes.items():
        match_count = sum(1 for ing in ingredients if process.extractOne(ing, available_ingredients)[1] > 80)
        match_percentage = (match_count / len(ingredients)) * 100

        if match_percentage > 50:  # If at least 50% of ingredients are available
            suggested_dishes.append((dish, match_percentage))
    
    suggested_dishes.sort(key=lambda x: x[1], reverse=True)  # Sort by best match
    return suggested_dishes

def read_ingredients(file_path):
    with open(file_path, 'r') as file:
        ingredients = [line.strip() for line in file.readlines()]
    return ingredients

# Read recipes from CSV file
def read_recipes(file_path):
    recipes = {}
    with open(file_path, 'r',encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            dish = row[0]
            Name=row[1]
            ingredients = row[1:]
            recipes[dish] = ingredients
    return recipes

# Update the recipes dictionary
recipes = read_recipes('dish.csv')

# Example: Ingredients detected in the fridge
user_ingredients = read_ingredients('ing.txt')

# Get dish suggestions
suggestions = suggest_dishes(user_ingredients)



if suggestions:
    print("Suggested Dishes:")
    for Name, match in suggestions:
        print(f"- {Name} ({match:.1f}% match)")
else:
    print("No matching dishes found. Try adding more ingredients!")