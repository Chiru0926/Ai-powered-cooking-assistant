import csv
from gtts import gTTS
import pygame
import threading
import os

class TTSController:
    def __init__(self):
        pygame.mixer.init()
        self.paused = threading.Event()
        self.paused.set()
        self.stop_signal = threading.Event()
        self.audio_file = "temp_audio.mp3"

    def speak(self, text):
        tts = gTTS(text=text, lang='en')
        tts.save(self.audio_file)
        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.play()

        def run():
            while pygame.mixer.music.get_busy():
                self.paused.wait()
                if self.stop_signal.is_set():
                    pygame.mixer.music.stop()
                    break

        self.thread = threading.Thread(target=run)
        self.thread.start()

    def pause(self):
        self.paused.clear()
        pygame.mixer.music.pause()

    def resume(self):
        self.paused.set()
        pygame.mixer.music.unpause()

    def stop(self):
        self.stop_signal.set()
        self.paused.set()
        pygame.mixer.music.stop()
        if self.thread.is_alive():
            self.thread.join()
        if os.path.exists(self.audio_file):
            os.remove(self.audio_file)

def read_recipe(file_path, index):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        recipes = list(reader)
        if index < 0 or index >= len(recipes):
            raise IndexError("Recipe index out of range")
        return recipes[index]

def main():
    file_path = 'Dish.csv'  # Update with your CSV file path
    ii = int(input("Enter Dish no: "))
    index = ii - 1  # Update with the desired recipe index

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

if __name__ == "__main__":
    main()