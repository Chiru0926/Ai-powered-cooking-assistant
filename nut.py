# import requests

# # Replace with your actual Edamam API credentials
# EDAMAM_APP_ID = 'YOUR_EDAMAM_APP_ID'
# EDAMAM_APP_KEY = 'YOUR_EDAMAM_APP_KEY'

# def read_ingredients(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         ingredients = [ingredient.strip().lower() for ingredient in file.read().split(',')]
#     return ingredients

# def get_nutrient_info(ingredient):
#     url = f'https://api.edamam.com/api/food-database/v2/parser?ingr={ingredient}&app_id={EDAMAM_APP_ID}&app_key={EDAMAM_APP_KEY}'
#     response = requests.get(url)
#     data = response.json()
#     if 'parsed' in data and len(data['parsed']) > 0:
#         food = data['parsed'][0]['food']
#         nutrients = food.get('nutrients', {})
#         return nutrients
#     else:
#         return None

# def get_geographical_info(ingredient):
#     # This is a placeholder function. Replace with actual implementation.
#     # You can use a custom database or API to get the geographical information.
#     geographical_info = {
#         'garlic': {'country': 'USA', 'state': 'California'},
#         'butter': {'country': 'France', 'state': 'Normandy'},
#         # Add more ingredients and their geographical info here
#     }
#     return geographical_info.get(ingredient.lower(), {'country': 'Unknown', 'state': 'Unknown'})

# def main():
#     ingredients_file = 'ing.txt'  # Update with your TXT file path
#     ingredients = read_ingredients(ingredients_file)

#     for ingredient in ingredients:
#         nutrient_info = get_nutrient_info(ingredient)
#         geographical_info = get_geographical_info(ingredient)

#         print(f"Ingredient: {ingredient.capitalize()}")
#         print(f"Country: {geographical_info['country']}, State: {geographical_info['state']}")
#         if nutrient_info:
#             print("Nutrient Information:")
#             for nutrient, value in nutrient_info.items():
#                 print(f"  {nutrient}: {value}")
#         else:
#             print("Nutrient information not found.")
#         print()

# if __name__ == "__main__":
#     main()