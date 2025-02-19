import csv
import pyttsx3

def read_recipe(file_path, index):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        recipes = list(reader)
        if index < 0 or index >= len(recipes):
            raise IndexError("Recipe index out of range")
        return recipes[index]

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    file_path = 'Dish.csv'  # Update with your CSV file path
    ii=int(input("Enter Dish no:"))
    index = ii-1  # Update with the desired recipe index

    try:
        recipe = read_recipe(file_path, index)
        recipe_text = f"Recipe for {recipe[0]}: " + ", ".join(recipe[1:4])
        print(recipe_text)
        text_to_speech(recipe_text)
    except IndexError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()