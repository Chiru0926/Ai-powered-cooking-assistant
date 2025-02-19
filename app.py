import sys
from Dish import suggest_dishes, read_ingredients, read_recipes
from recipe import read_recipe, TTSController
from shop import read_recipes as shop_read_recipes, read_ingredients as shop_read_ingredients, get_missing_ingredients
from nut import read_ingredients as nut_read_ingredients, get_nutrient_info, get_geographical_info

def main():
    while True:
        print("Choose an option:")
        print("1. Suggest Dishes")
        print("2. Read Recipe and TTS")
        print("3. Get Missing Ingredients")
        print("4. Get Nutrient Information")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            recipes = read_recipes('Dish.csv')
            user_ingredients = read_ingredients('ing.txt')
            suggestions = suggest_dishes(user_ingredients)
            if suggestions:
                print("Suggested Dishes:")
                for dish, match in suggestions:
                    print(f"- {dish} ({match:.1f}% match)")
            else:
                print("No matching dishes found. Try adding more ingredients.")

        elif choice == '2':
            file_path = 'Dish.csv'
            ii = int(input("Enter Dish no: "))
            index = ii - 1
            try:
                recipe = read_recipe(file_path, index)
                recipe_text = f"Recipe for {recipe[0]}: " + ", ".join(recipe[1:4])
                print(recipe_text)
                tts = TTSController()
                tts.speak(recipe_text)
                while True:
                    command = input("Enter 'pause' to pause, 'resume' to resume, 'stop' to stop: ").strip().lower()
                    if command == 'pause':
                        tts.pause()
                    elif command == 'resume':
                        tts.resume()
                    elif command == 'stop':
                        tts.stop()
                        break
                    else:
                        print("Invalid command. Please enter 'pause', 'resume', or 'stop'.")
            except IndexError as e:
                print(e)
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == '3':
            recipes = shop_read_recipes('Dish.csv')
            current_ingredients = shop_read_ingredients('ing.txt')
            dish = input("Enter the name of the dish: ")
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

        elif choice == '4':
            ingredients = nut_read_ingredients('ing.txt')
            for ingredient in ingredients:
                nutrient_info = get_nutrient_info(ingredient)
                geographical_info = get_geographical_info(ingredient)
                print(f"Ingredient: {ingredient.capitalize()}")
                print(f"Country: {geographical_info['country']}, State: {geographical_info['state']}")
                if nutrient_info:
                    print("Nutrient Information:")
                    for nutrient, value in nutrient_info.items():
                        print(f"  {nutrient}: {value}")
                else:
                    print("Nutrient information not found.")
                print()

        elif choice == '5':
            print("Exiting...")
            sys.exit()

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()