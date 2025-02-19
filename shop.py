import csv

def read_recipes(file_path):
    recipes = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            dish = row[0]
            ingredients = [ingredient.strip().lower() for ingredient in row[2].split(',')]
            recipes[dish] = ingredients
    return recipes

def read_ingredients(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        ingredients = [ingredient.strip().lower() for ingredient in file.read().split(',')]
    return ingredients

def get_missing_ingredients(dish, recipes, current_ingredients):
    if dish not in recipes:
        raise ValueError(f"Dish '{dish}' not found in recipes.")
    required_ingredients = recipes[dish]
    missing_ingredients = [ingredient for ingredient in required_ingredients if ingredient not in current_ingredients]
    return missing_ingredients

def main():
    recipes_file = 'Dish.csv'  # Update with your CSV file path
    ingredients_file = 'ing.txt'  # Update with your TXT file path
    dish = input("Enter the name of the dish: ")

    recipes = read_recipes(recipes_file)
    current_ingredients = read_ingredients(ingredients_file)

    try:
        missing_ingredients = get_missing_ingredients(dish, recipes, current_ingredients)
        if missing_ingredients:
            print("You need to buy the following ingredients:")
            for ingredient in missing_ingredients:
                print(f"- {ingredient}")
        else:
            print("You have all the ingredients needed for this dish.")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()