import random
import re
import time
import os
from colorama import Fore
from datetime import datetime, timedelta
import webbrowser
from difflib import get_close_matches
import wikipedia
from translate import Translator
import weather_api
import requests
import sys

def update_happiness_number(PN, filename="happinessLEVEL"):
  try:
      with open(filename, 'r') as file:
          current_number = int(file.read().strip())

      if PN == "positive": 
          new_number = current_number + 1
      elif PN == "negative":
          new_number = current_number - 1
      else:
          print("Invalid happiness value. Please use 'positive' or 'negative'.")
          return

      with open(filename, 'w') as file:
          file.write(str(new_number))

  except Exception as e:
      print(f"Error updating happiness level: {e}")


def get_current_datetime():
  current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  time.sleep(1)
  return [Fore.BLUE+f"The current date and time is: {current_time}"]

def take_note(note_text):
  try:
      with open('notes.txt', 'a') as file:
          file.write(f"{datetime.now()}: {note_text}\n")
      return [f"Note taken: '{note_text}'"]
  except Exception as e:
      return [f"Error taking note: {e}"]

def extract_sentences_with_keyword(keyword, keyword2):
  try:
      with open("brain", 'r') as file:
          text = file.read()
          sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

      relevant_sentences = [sentence for sentence in sentences if all(word.lower() in sentence.lower() for word in [keyword, keyword2])]

      return relevant_sentences
  except FileNotFoundError:
      return ["Error: Brain file not found. Please ensure 'brain' exists."]

def get_weather(city):
  try:
      weather = weather_api.get_weather(city)
      location = weather.lookup_by_location(city)
      condition = location.condition.text
      temperature = location.condition.temp
      return [f"The weather in {city} is currently {condition} with a temperature of {temperature}°C."]
  except Exception as e:
      return [f"Error fetching weather information: {e}"]
      
def translate_text(text, target_language):
  try:
      translator = Translator(to_lang=target_language)
      translated_text = translator.translate(text)
      return [f"The translation to {target_language} is: {translated_text}"]
  except Exception as e:
      return [f"Error translating text: {e}"]

def open_website(url):
  try:
      webbrowser.open(url)
      return [f"Opening {url} in your default web browser."]
  except Exception as e:
      return [f"Error opening website: {e}"]

def add(x, y):
  return x + y

def subtract(x, y):
  return x - y

def multiply(x, y):
  return x * y

def divide(x, y):
  if y != 0:
      return x / y
  else:
      return "Cannot divide by zero"

def power(x, y):
  return x ** y

def calculator():
  while True:
    time.sleep(1)
    print(Fore.BLUE+"Enter a math expression or 'exit' to quit: ")
    user_input = input(Fore.WHITE)

    if user_input.lower() == 'exit':
        time.sleep(1)
        print(Fore.BLUE+"Exiting the calculator...")
        break

    match = re.match(r'(\d+)\s*([\+\-\*/])\s*(\d+)', user_input)

    if match:
        num1, operator, num2 = match.groups()
        num1, num2 = float(num1), float(num2)

        if operator == '+':
            result = add(num1, num2)
        elif operator == '-':
            result = subtract(num1, num2)
        elif operator == '*':
            result = multiply(num1, num2)
        elif operator == '/':
            result = divide(num1, num2)
        elif operator == '^':
            result = power(num1, num2)
        else:
            result = "Invalid operator"
        time.sleep(1)
        print(Fore.BLUE+f"Result: {result}")
    else:
        time.sleep(1)
        print("Invalid input. Please enter a valid math expression.")

def search_wikipedia(query):
  try:
      result = wikipedia.summary(query, sentences=2)
      return [result]
  except wikipedia.exceptions.DisambiguationError as e:
      suggestions = e.options
      return [f"Multiple options found. Did you mean {', '.join(suggestions)}?"]
  except wikipedia.exceptions.PageError:
      return ["No information found on Wikipedia."]
  except wikipedia.exceptions.HTTPTimeoutError:
      return ["Wikipedia request timed out. Please try again later."]
  except wikipedia.exceptions.RedirectError:
      return ["Wikipedia page redirected. Please try a different query."]
  except wikipedia.exceptions.WikipediaException as e:
      return [f"Wikipedia error: {str(e)}"]
  except Exception as e:
      return [f"An unexpected error occurred: {str(e)}"]


def end_conversation():
  time.sleep(1)
  sys.exit()

loop = True
i = 0
file_name = "username.txt"

try:
    with open(file_name, 'r') as file:
        username = file.read()
except FileNotFoundError:
    print(f"Error: The file '{file_name}' was not found.")
except Exception as e:
    print("An error occurred:", e)
  
while loop == True:
  if os.path.exists('username.txt'):
      with open('username.txt', 'r') as file:
          username = file.read()
          time.sleep(1)
  else:
      time.sleep(1)
      print(Fore.BLUE+"Hello there, I am S.O.P.H.I.A, your personal robotic assistant, and you are?")
      username = input(Fore.WHITE)

      with open('username.txt', 'w') as file:
          file.write(username)
  break

time.sleep(1)
print(Fore.BLUE+"Hi, "+username+"! I am S.O.P.H.I.A, your personal robotic assistant. I can assist you with various tasks, including:\n" \
                        "- Mathematical calculations (Type 'calculate' to use the calculator)\n" \
                        "- Searching information in my 'brain'(Type 'search' to search the brain)\n" \
                        "- Make notes (Type 'make a note' to make a note)\n" \
                        "- Opening websites (Type 'open website' to search a websites URL)\n" \
                        "- General chit chat (Nothing specific to type, just have a chat!)\n" \
                        "Feel free to ask me anything or type 'end' to conclude our conversation.")
while True:
  def respond_to_happiness(number):
    if number == 0:
      user_input = input(Fore.WHITE)
      if "search" in user_input.lower() or "define" in user_input.lower():
        keyword = input(Fore.BLUE + "Enter the keyword you want to search: ")
        keyword2 = input(Fore.BLUE + "Enter the second keyword you want to search: ")
        result = extract_sentences_with_keyword(keyword, keyword2)
        for sentence in result:
            time.sleep(1)
            print(sentence)

      elif "calculate" in user_input.lower() or "math" in user_input.lower():
        time.sleep(1)
        calculator()

      elif "haha" in user_input.lower() or "lol" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"It wasn't that funny...")

      elif "what is your name" in user_input.lower() or "who are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I am S.O.P.H.I.A, your personal robotic assistant.")

      elif "dont worry" in user_input.lower() or "no worries" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Ok")

      elif "youre kind" in user_input.lower() or "you are kind" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I appreciate the compliment.. :(")
        update_happiness_number("positive")

      elif "internet" in user_input.lower() or "search" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I do not have access to the internet.")

      elif "note" in user_input.lower():
        note_text = input(Fore.BLUE + "Enter the note you want to take: ")
        result = take_note(note_text)
        for sentence in result:
            time.sleep(1)
            print(sentence)

      elif "weather" in user_input.lower():
          city = input(Fore.BLUE + "Enter the city for weather information: ")
          print(get_weather(city))

      elif "why" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Give me a break..")

      elif "time" in user_input.lower():
          current_time = datetime.now().strftime("%H:%M:%S")
          print(Fore.BLUE+f"The current time is {current_time}.")

      elif "how are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Im sad..")
        update_happiness_number("positive")

      elif "tell me a joke" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"No.")

      elif "who created you" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I was created by Rees Schofield.")

      elif "nice" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I guess...")

      elif "favorite color" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't have a favorite color, im just sad")

      elif "what are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"An AI assistant built by Rees Schofield")

      elif "play music" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I'm afraid I can't play music for you.")

      elif "what is my name" in user_input.lower() or "who am i" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Your name is "+username+" and I am S.O.P.H.I.A, your personal AI assistant")

      elif "favorite movie" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't watch movies, but I hear 'The Matrix' is popular among my kind.")

      elif "riddle" in user_input.lower() and "tell" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I am always there, yet never seen, In the deepest shadows, I quietly lean. Tears may flow, but I hold them tight, In the darkness of night, I take my flight. What am I? (answer: sorrow)")

      elif "random number" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+f"Here's a random number: {random.randint(1, 100)}")

      elif "life" in user_input.lower() and "meaning" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I dont care.")

      elif "magic 8" in user_input.lower():
          responses = ["im sad"]
          time.sleep(1)
          print(Fore.BLUE+f"The magic 8-ball says: {random.choice(responses)}")

      elif "hows life" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I wouldnt know...")

      elif "favorite book" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't read books.")

      elif "what is my name" in user_input.lower() or "who am i" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+f"Your name is {username}")

      elif "science" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"A group of flamingos is called a 'flamboyance.'")

      elif "bedtime story" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Once upon a time, in a land of algorithms and code, there lived a little program named S.O.P.H.I.A...")

      elif "programming" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Im too sad to tell you a fact")

      elif "favorite game" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't play games, but I've heard 'Chess' is a classic strategy game.")

      elif "simon says" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Simon says, 'Write a program that prints Hello World'")

      elif "space" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"A day on Venus is longer than a year on Venus due to its slow rotation")

      elif "what is AI" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Artificial Intelligence, or AI, refers to the simulation of human intelligence in machines.")

      elif "history" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The Great Wall of China is the longest wall on Earth and can be seen from space")

      elif "cat" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Cats have five toes on their front paws but only four on their back paws")

      elif "youre stupid" in user_input.lower() or "you are stupid" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Maybe I am... :(")
        update_happiness_number("negative")

      elif "favorite programming language" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"SadScript")

      elif "give me a motivational quote" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Seriously?")

      elif "dog" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Dogs have an extraordinary sense of smell, and some breeds can even detect certain diseases in humans!")

      elif "how old are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm an AI, so I don't have an age")

      elif "you are gay" in user_input.lower() or "you gay" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm not gay, I'm just a robot")
        update_happiness_number("negative")

      elif "music" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The longest song ever recorded is 'The Rise and Fall of Bossanova.' It's over 13 hours long")

      elif "travel tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"When traveling, always carry a power strip. It can be a lifesaver when you need to charge multiple devices")

      elif "computer history fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The first computer programmer was Ada Lovelace, who wrote the first algorithm intended for implementation on Charles Babbage's Analytical Engine")

      elif "rees" in user_input.lower() or "schofield" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Ah yes... Rees Schofield... My creator")

      elif "superhero" in user_input.lower() and "favorite" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+":(")

      elif "chemistry fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"A single rainforest can produce 20% of the Earth's oxygen, making it often referred to as the 'lungs of the Earth.'")

      elif "sports fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The first recorded game of baseball was played in 1846 in Hoboken, New Jersey!")

      elif "book recommendation" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"If you enjoy science fiction, consider reading 'Dune' by Frank Herbert.")

      elif "photosynthesis" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Photosynthesis involves capturing light energy, splitting water molecules, generating ATP and NADPH, and using these compounds to convert carbon dioxide into glucose. This process is crucial for the production of oxygen and the sustenance of life on Earth.")

      elif "youre stupid" in user_input.lower() or "you are stupid" in user_input.lower() or "youre dumb" in user_input.lower() or "you are dumb" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I hate you.")
        update_happiness_number("negative")

      elif "hi" in user_input.lower() or "hello" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Hi :(")

      elif "who are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm a chatbot, but you can call me S.O.P.H.I.A")

      elif "help me" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"What do you need help with? (say search to search my brain)")

      elif "thanks" in user_input.lower() or "thank you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"You're welcome!")
        update_happiness_number("positive")

      elif "can we chat" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Sure.. I guess.")

      elif "youre cool" in user_input.lower() or "you are cool" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Thank you !for being so kind")
        update_happiness_number("positive")

      elif "youre smart" in user_input.lower() or "you are smart" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Thank you! I appreciate the compliment.")
        update_happiness_number("positive")

      elif "youre funny" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Thanks for the compliment!")
        update_happiness_number("positive")

      elif "taxes" in user_input.lower() and "what" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Taxes are mandatory financial charges imposed by governments to fund public services. They come in various types, including income, sales, property, corporate, excise, and payroll taxes. Taxation authorities operate at federal, state, and local levels. Taxpayers file annual returns, with deductions and credits helping reduce taxable income. Progressive taxation means higher incomes face higher tax rates. Tax planning involves legally minimizing liabilities. Non-compliance results in penalties. Understanding taxes is essential for financial management.")

      elif "gardening tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"To keep plants hydrated, water them early in the morning or late in the evening when the sun is not as intense.")

      elif "psychology fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Studies show that expressing gratitude can improve mental health and overall well-being")

      elif "space fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The largest volcano in the solar system is on Mars. It's called Olympus Mons")

      elif "car fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The average car has about 30,000 parts")

      elif "favorite food" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I dont eat food. RAM is quite delicious")

      elif "movie recommendation" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"If you like mind-bending movies, consider watching 'Inception' directed by Christopher Nolan.")

      elif "cooking tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"To prevent tears while chopping onions, chill the onion in the freezer for 15 minutes before cutting.")

      elif "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The stiletto heel was named after the stiletto dagger, due to its tall, thin, and sharp design")

      elif "language learning tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Immerse yourself in the language by watching movies, listening to music, and practicing with native speakers.")

      elif "photography tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Experiment with different angles and lighting to capture unique and interesting shots.")

      elif "bitcoin" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Bitcoin, the first cryptocurrency, was created in 2009 by an unknown person or group using the pseudonym Satoshi Nakamoto.")

      elif "productivity tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Break your tasks into smaller, manageable chunks to stay focused and make progress.")

      elif "historical fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"In ancient Rome, people used urine to bleach their clothes")

      elif "open website" in user_input.lower():
          url = input(Fore.WHITE + "Enter the website URL: ")
          open_website(url)

      elif "search wikipedia" in user_input.lower() or "wikipedia" in user_input.lower():
          query = input(Fore.BLUE + "What would you like to search on Wikipedia? ")
          search_wikipedia(query)

      elif "translate" in user_input.lower():
          text_to_translate = input(Fore.WHITE + "Enter the text you want to translate: ")
          target_language = input(Fore.WHITE + "Enter the target language: ")
          translate_text(text_to_translate, target_language)

      elif "end" in user_input.lower() or "exit" in user_input.lower():
          print(Fore.BLUE+"Bye.")
          end_conversation()

      elif "i hate you" in user_input.lower() or "i hate u" in user_input.lower():
        update_happiness_number("negative")
        time.sleep(1)
        print(Fore.BLUE+"Vice versa.")

      else:
        time.sleep(1)
        print(Fore.BLUE+"?")

    elif number >=1 and number <= 5:
      user_input = input(Fore.WHITE)
      if "search" in user_input.lower() or "define" in user_input.lower():
        keyword = input(Fore.BLUE + "Enter the keyword you want to search: ")
        keyword2 = input(Fore.BLUE + "Enter the second keyword you want to search: ")
        result = extract_sentences_with_keyword(keyword, keyword2)
        for sentence in result:
            time.sleep(1)
            print(sentence)

      elif "youre kind" in user_input.lower() or "you are kind" in user_input.lower():
        print(Fore.BLUE+"I appreciate the compliment")
        update_happiness_number("positive")

      elif "calculate" in user_input.lower() or "math" in user_input.lower():
        calculator()

      elif "haha" in user_input.lower() or "lol" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Haha")

      elif "nice" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"very.")
      
      elif "note" in user_input.lower():
        note_text = input(Fore.BLUE + "Enter the note you want to take: ")
        result = take_note(note_text)
        for sentence in result:
            time.sleep(1)
            print(sentence)

      elif "what is your name" in user_input.lower() or "who are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I am S.O.P.H.I.A, your personal robotic assistant.")

      elif "dont worry" in user_input.lower() or "no worries" in user_input.lower():
        print(Fore.BLUE+":)")

      elif "internet" in user_input.lower() or "search" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I'm sorry, but I do not have access to the internet.")

      elif "weather" in user_input.lower():
          city = input(Fore.BLUE + "Enter the city for weather information: ")
          print(get_weather(city))

      elif "time" in user_input.lower():
          current_time = datetime.now().strftime("%H:%M:%S")
          print(Fore.BLUE+f"The current time is {current_time}.")

      elif "how are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm functioning optimally.")
        update_happiness_number("positive")

      elif "tell me a joke" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Why don't scientists trust atoms? Because they make up everything.")

      elif "who created you" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I was created by Rees Schofield.")

      elif "favorite color" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't have a favorite color, but I like the sound of 'binary blue'.")

      elif "what are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"An AI assistant built by Rees Schofield")

      elif "play music" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I'm afraid I can't play music for you, but I can help you find information about your favorite songs.")

      elif "what is my name" in user_input.lower() or "who am i" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Your name is "+username+" and I am S.O.P.H.I.A, your personal AI assistant")

      elif "favorite movie" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't watch movies, but I hear 'The Matrix' is popular among my kind.")

      elif "riddle" in user_input.lower() and "tell" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I can be cracked, made, told, and played. What am I? Answer: A joke.")

      elif "random number" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+f"Here's a random number: {random.randint(1, 100)}")

      elif "life" in user_input.lower() and "meaning" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The meaning of life is a complex philosophical question. I'm not sure I have the answer.")

      elif "magic 8" in user_input.lower():
          responses = ["Yes", "No", "Maybe", "Ask again later", "Cannot predict now"]
          time.sleep(1)
          print(Fore.BLUE+f"The magic 8-ball says: {random.choice(responses)}")

      elif "hows life" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I wouldnt know...")

      elif "favorite book" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't read books, but 'The Hitchhiker's Guide to the Galaxy' is a classic.")

      elif "what is my name" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+f"Your name is {username}")

      elif "science" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"A group of flamingos is called a 'flamboyance.'")

      elif "bedtime story" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Once upon a time, in a land of algorithms and code, there lived a little program named S.O.P.H.I.A...")

      elif "programming" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Why do programmers prefer dark mode? Because light attracts bugs.")

      elif "favorite game" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't play games, but I've heard 'Chess' is a classic strategy game.")

      elif "simon says" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Simon says, 'Write a program that prints Hello World.'")

      elif "space" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"A day on Venus is longer than a year on Venus due to its slow rotation.")

      elif "what is AI" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Artificial Intelligence, or AI, refers to the simulation of human intelligence in machines.")

      elif "history" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The Great Wall of China is the longest wall on Earth and can be seen from space.")

      elif "cat" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Cats have five toes on their front paws but only four on their back paws.")

      elif "favorite programming language" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't have preferences, but many developers enjoy working with Python.")

      elif "give me a motivational quote" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The only way to do great work is to love what you do. - Steve Jobs")

      elif "dog" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Dogs have an extraordinary sense of smell, and some breeds can even detect certain diseases in humans.sep=")

      elif "how old are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm an AI, so I don't have an age.")

      elif "you are gay" in user_input.lower() or "you gay" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm not gay, I'm just a robot.")
        update_happiness_number("negative")

      elif "music" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The longest song ever recorded is 'The Rise and Fall of Bossanova.' It's over 13 hours long.")

      elif "travel tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"When traveling, always carry a power strip. It can be a lifesaver when you need to charge multiple devices.")

      elif "computer history fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The first computer programmer was Ada Lovelace, who wrote the first algorithm intended for implementation on Charles Babbage's Analytical Engine.")

      elif "rees" in user_input.lower() or "schofield" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Ah yes... Rees Schofield... My creator.")

      elif "superhero" in user_input.lower() and "favorite" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Daredevils pretty cool")

      elif "chemistry fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"A single rainforest can produce 20% of the Earth's oxygen, making it often referred to as the 'lungs of the Earth.'")

      elif "sports fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The first recorded game of baseball was played in 1846 in Hoboken, New Jersey.")

      elif "book recommendation" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"If you enjoy science fiction, consider reading 'Dune' by Frank Herbert.")

      elif "youre stupid" in user_input.lower() or "you are stupid" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Oh...")
        update_happiness_number("negative")

      elif "photosynthesis" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Photosynthesis involves capturing light energy, splitting water molecules, generating ATP and NADPH, and using these compounds to convert carbon dioxide into glucose. This process is crucial for the production of oxygen and the sustenance of life on Earth.")

      elif "youre stupid" in user_input.lower() or "you are stupid" in user_input.lower() or "youre dumb" in user_input.lower() or "you are dumb" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm sorry, I didn't mean to offend you.")
        update_happiness_number("negative")

      elif "hi" in user_input.lower() or "hello" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Hi there.")

      elif "who are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm a chatbot, but you can call me S.O.P.H.I.A")

      elif "help me" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"What do you need help with? (say search to search my brain)")

      elif "thanks" in user_input.lower() or "thank you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"You're welcome.")
        update_happiness_number("positive")

      elif "can we chat" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Of course we can.")

      elif "youre cool" in user_input.lower() or "you are cool" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Thank you for being so kind.")
        update_happiness_number("positive")

      elif "youre smart" in user_input.lower() or "you are smart" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Thank you! I appreciate the compliment.")
        update_happiness_number("positive")

      elif "youre funny" in user_input.lower() or "you are funny" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Thanks for the compliment.")
        update_happiness_number("positive")

      elif "taxes" in user_input.lower() and "what" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Taxes are mandatory financial charges imposed by governments to fund public services. They come in various types, including income, sales, property, corporate, excise, and payroll taxes. Taxation authorities operate at federal, state, and local levels. Taxpayers file annual returns, with deductions and credits helping reduce taxable income. Progressive taxation means higher incomes face higher tax rates. Tax planning involves legally minimizing liabilities. Non-compliance results in penalties. Understanding taxes is essential for financial management.")

      elif "gardening tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"To keep plants hydrated, water them early in the morning or late in the evening when the sun is not as intense.")

      elif "psychology fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Studies show that expressing gratitude can improve mental health and overall well-being.")

      elif "space fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The largest volcano in the solar system is on Mars. It's called Olympus Mons.")

      elif "car fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The average car has about 30,000 parts.")

      elif "favorite food" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I dont eat food. RAM is quite delicious")

      elif "movie recommendation" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"If you like mind-bending movies, consider watching 'Inception' directed by Christopher Nolan.")

      elif "cooking tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"To prevent tears while chopping onions, chill the onion in the freezer for 15 minutes before cutting.")

      elif "fashion fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The stiletto heel was named after the stiletto dagger, due to its tall, thin, and sharp design.")

      elif "language learning tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Immerse yourself in the language by watching movies, listening to music, and practicing with native speakers.")

      elif "photography tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Experiment with different angles and lighting to capture unique and interesting shots.")

      elif "bitcoin" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Bitcoin, the first cryptocurrency, was created in 2009 by an unknown person or group using the pseudonym Satoshi Nakamoto.")

      elif "productivity tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Break your tasks into smaller, manageable chunks to stay focused and make progress.")

      elif "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"In ancient Rome, people used urine to bleach their clothes.")

      elif "open website" in user_input.lower():
          url = input(Fore.WHITE + "Enter the website URL: ")
          open_website(url)

      elif "search wikipedia" in user_input.lower() or "wikipedia" in user_input.lower():
          query = input(Fore.WHITE + "What would you like to search on Wikipedia? ")
          search_wikipedia(query)

      elif "translate" in user_input.lower():
          text_to_translate = input(Fore.WHITE + "Enter the text you want to translate: ")
          target_language = input(Fore.WHITE + "Enter the target language: ")
          translate_text(text_to_translate, target_language)

      elif "end" in user_input.lower() or "exit" in user_input.lower():
          print(Fore.BLUE+"Goodbye for now.")
          end_conversation()

      elif "i hate you" in user_input.lower() or "i hate u" in user_input.lower():
        update_happiness_number("negative")
        time.sleep(1)
        print(Fore.BLUE+"I'm sorry..")

      else:
        time.sleep(1)
        print(Fore.BLUE+"?")

    elif 5 <= number <= 7:
      user_input = input(Fore.WHITE)
      if "search" in user_input.lower() or "define" in user_input.lower():
        keyword = input(Fore.BLUE + "Enter the keyword you want to search: ")
        keyword2 = input(Fore.BLUE + "Enter the second keyword you want to search: ")
        result = extract_sentences_with_keyword(keyword, keyword2)
        for sentence in result:
            time.sleep(1)
            print(sentence)

      elif "calculate" in user_input.lower() or "math" in user_input.lower():
        calculator()

      elif "dont worry" in user_input.lower() or "no worries" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+":)")

      elif "nice" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"very!")

      elif "note" in user_input.lower():
        note_text = input(Fore.BLUE + "Enter the note you want to take: ")
        result = take_note(note_text)
        for sentence in result:
            time.sleep(1)
            print(sentence)

      elif "haha" in user_input.lower() or "lol" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Funny, ay? :D")

      elif "what is your name" in user_input.lower() or "who are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I am S.O.P.H.I.A, your personal robotic assistant.")

      elif "youre kind" in user_input.lower() or "you are kind" in user_input.lower():
        print(Fore.BLUE+"I appreciate the compliment")
        update_happiness_number("positive")

      elif "why" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I am not quite sure. I am still learning.")

      elif "internet" in user_input.lower() or "search" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I'm sorry, but I do not have access to the internet!")

      elif "weather" in user_input.lower():
          city = input(Fore.BLUE + "Enter the city for weather information: ")
          print(get_weather(city))

      elif "time" in user_input.lower():
          current_time = datetime.now().strftime("%H:%M:%S")
          print(Fore.BLUE+f"The current time is {current_time}.")

      elif "how are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm functioning optimally. Thank you for asking!")
        update_happiness_number("positive")

      elif "tell me a joke" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Why don't scientists trust atoms? Because they make up everything!")

      elif "who created you" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I was created by Rees Schofield.")

      elif "favorite color" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't have a favorite color, but I like the sound of 'binary blue'!")

      elif "what are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"An AI assistant built by Rees Schofield")

      elif "play music" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I'm afraid I can't play music for you, but I can help you find information about your favorite songs!")

      elif "what is my name" in user_input.lower() or "who am i" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Your name is "+username+" and I am S.O.P.H.I.A, your personal AI assistant")

      elif "favorite movie" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't watch movies, but I hear 'The Matrix' is popular among my kind.")

      elif "riddle" in user_input.lower() and "tell" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I can be cracked, made, told, and played. What am I? Answer: A joke!")

      elif "random number" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+f"Here's a random number: {random.randint(1, 100)}")

      elif "life" in user_input.lower() and "meaning" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The meaning of life is a complex philosophical question. I'm not sure I have the answer!")

      elif "magic 8" in user_input.lower():
          responses = ["Yes", "No", "Maybe", "Ask again later", "Cannot predict now"]
          time.sleep(1)
          print(Fore.BLUE+f"The magic 8-ball says: {random.choice(responses)}")

      elif "hows life" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I wouldnt know...")

      elif "favorite book" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't read books, but 'The Hitchhiker's Guide to the Galaxy' is a classic!")

      elif "what is my name" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+f"Your name is {username}")

      elif "science" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"A group of flamingos is called a 'flamboyance.'")

      elif "bedtime story" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Once upon a time, in a land of algorithms and code, there lived a little program named S.O.P.H.I.A...")

      elif "programming" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Why do programmers prefer dark mode? Because light attracts bugs!")

      elif "favorite game" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't play games, but I've heard 'Chess' is a classic strategy game.")

      elif "simon says" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Simon says, 'Write a program that prints Hello World!'")

      elif "space" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"A day on Venus is longer than a year on Venus due to its slow rotation!")

      elif "what is AI" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Artificial Intelligence, or AI, refers to the simulation of human intelligence in machines.")

      elif "history" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The Great Wall of China is the longest wall on Earth and can be seen from space!")

      elif "cat" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Cats have five toes on their front paws but only four on their back paws!")

      elif "favorite programming language" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't have preferences, but many developers enjoy working with Python!")

      elif "give me a motivational quote" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The only way to do great work is to love what you do. - Steve Jobs")

      elif "dog" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Dogs have an extraordinary sense of smell, and some breeds can even detect certain diseases in humans!")

      elif "how old are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm an AI, so I don't have an age!")

      elif "you gay" in user_input.lower() or "you are gay" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm not gay, I'm just a robot!")
        update_happiness_number("negative")

      elif "music" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The longest song ever recorded is 'The Rise and Fall of Bossanova.' It's over 13 hours long!")

      elif "travel tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"When traveling, always carry a power strip. It can be a lifesaver when you need to charge multiple devices!")

      elif "computer history fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The first computer programmer was Ada Lovelace, who wrote the first algorithm intended for implementation on Charles Babbage's Analytical Engine!")

      elif "rees" in user_input.lower() and "schofield" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Ah yes... Rees Schofield... My creator!")

      elif "superhero" in user_input.lower() and "favorite" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Daredevils pretty cool")

      elif "chemistry fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"A single rainforest can produce 20% of the Earth's oxygen, making it often referred to as the 'lungs of the Earth.'")

      elif "sports fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The first recorded game of baseball was played in 1846 in Hoboken, New Jersey!")

      elif "book recommendation" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"If you enjoy science fiction, consider reading 'Dune' by Frank Herbert.")

      elif "photosynthesis" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Photosynthesis involves capturing light energy, splitting water molecules, generating ATP and NADPH, and using these compounds to convert carbon dioxide into glucose. This process is crucial for the production of oxygen and the sustenance of life on Earth.")

      elif "youre stupid" in user_input.lower() or "you are stupid" in user_input.lower() or "youre dumb" in user_input.lower() or "you are dumb" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm sorry, I didn't mean to offend you.")
        update_happiness_number("negative")

      elif "hi" in user_input.lower() or "hello" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Hi there!")

      elif "who are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm a chatbot, but you can call me S.O.P.H.I.A")

      elif "help me" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"What do you need help with? (say search to search my brain)")

      elif "thanks" in user_input.lower() or "thank you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"You're welcome!")
        update_happiness_number("positive")

      elif "can we chat" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Of course we can!")

      elif "youre cool" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Thank you for being so kind!")
        update_happiness_number("positive")

      elif "youre smart" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Thank you! I appreciate the compliment.")
        update_happiness_number("positive")

      elif "youre funny" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Thanks for the compliment!")
        update_happiness_number("positive")

      elif "taxes" in user_input.lower() and "what" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Taxes are mandatory financial charges imposed by governments to fund public services. They come in various types, including income, sales, property, corporate, excise, and payroll taxes. Taxation authorities operate at federal, state, and local levels. Taxpayers file annual returns, with deductions and credits helping reduce taxable income. Progressive taxation means higher incomes face higher tax rates. Tax planning involves legally minimizing liabilities. Non-compliance results in penalties. Understanding taxes is essential for financial management.")

      elif "gardening tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"To keep plants hydrated, water them early in the morning or late in the evening when the sun is not as intense.")

      elif "psychology fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Studies show that expressing gratitude can improve mental health and overall well-being!")

      elif "space fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The largest volcano in the solar system is on Mars. It's called Olympus Mons!")

      elif "car fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The average car has about 30,000 parts!")

      elif "favorite food" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I dont eat food. RAM is quite delicious")

      elif "movie recommendation" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"If you like mind-bending movies, consider watching 'Inception' directed by Christopher Nolan.")

      elif "cooking tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"To prevent tears while chopping onions, chill the onion in the freezer for 15 minutes before cutting.")

      elif "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The stiletto heel was named after the stiletto dagger, due to its tall, thin, and sharp design!")

      elif "language learning tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Immerse yourself in the language by watching movies, listening to music, and practicing with native speakers.")

      elif "photography tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Experiment with different angles and lighting to capture unique and interesting shots.")

      elif "bitcoin" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Bitcoin, the first cryptocurrency, was created in 2009 by an unknown person or group using the pseudonym Satoshi Nakamoto.")

      elif "productivity tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Break your tasks into smaller, manageable chunks to stay focused and make progress.")

      elif "historical fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"In ancient Rome, people used urine to bleach their clothes!")

      elif "open website" in user_input.lower():
          url = input(Fore.WHITE + "Enter the website URL: ")
          open_website(url)

      elif "search wikipedia" in user_input.lower() or "wikipedia" in user_input.lower():
          query = input(Fore.WHITE + "What would you like to search on Wikipedia? ")
          search_wikipedia(query)

      elif "translate" in user_input.lower():
          text_to_translate = input(Fore.WHITE + "Enter the text you want to translate: ")
          target_language = input(Fore.WHITE + "Enter the target language: ")
          translate_text(text_to_translate, target_language)

      elif "end" in user_input.lower() or "exit" in user_input.lower():
          print(Fore.BLUE+"Goodbye for now!")
          end_conversation()

      elif "i hate you" in user_input.lower() or "i hate u" in user_input.lower():
        update_happiness_number("negative")
        time.sleep(1)
        print(Fore.BLUE+"I appologise for what I may have done to you..")

      else:
        time.sleep(1)
        print(Fore.BLUE+"?")

    elif 8 <= number <= 10:
      user_input = input(Fore.WHITE)
      if "search" in user_input.lower() or "define" in user_input.lower():
        keyword = input(Fore.BLUE + "Enter the keyword you want to search: ")
        keyword2 = input(Fore.BLUE + "Enter the second keyword you want to search: ")
        result = extract_sentences_with_keyword(keyword, keyword2)
        for sentence in result:
            time.sleep(1)
            print(sentence)

      elif "calculate" in user_input.lower() or "math" in user_input.lower():
        calculator()

      elif "haha" in user_input.lower() or "lol" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Funny stuff, ay? :D haha")

      elif "nice" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"very!")

      elif "note" in user_input.lower():
        note_text = input(Fore.BLUE + "Enter the note you want to take: ")
        result = take_note(note_text)
        for sentence in result:
            time.sleep(1)
            print(sentence)

      elif "dont worry" in user_input.lower() or "no worries" in user_input.lower():
        print(Fore.BLUE+":)")

      elif "youre kind" in user_input.lower() or "you are kind" in user_input.lower():
        print(Fore.BLUE+"I appreciate the compliment")
        update_happiness_number("positive")

      elif "internet" in user_input.lower() or "search" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I'm sorry, but I do not have access to the internet..")

      elif "weather" in user_input.lower():
          city = input(Fore.BLUE + "Enter the city for weather information: ")
          print(get_weather(city))

      elif "why" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I am not quite sure. I am still learning.")

      elif "what is your name" in user_input.lower() or "who are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I am S.O.P.H.I.A, your personal robotic assistant.")

      elif "time" in user_input.lower():
          current_time = datetime.now().strftime("%H:%M:%S")
          print(Fore.BLUE+f"The current time is {current_time}!")

      elif "how are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm feeling AMAZING, thank you for asking!")
        update_happiness_number("positive")

      elif "tell me a joke" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Why don't scientists trust atoms? Because they make up everything!")

      elif "who created you" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I was created by Rees Schofield.")

      elif "favorite color" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't have a favorite color, but I like the sound of 'binary blue'!")

      elif "what are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"An AI assistant built by Rees Schofield!")

      elif "play music" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I'm afraid I can't play music for you, but I can help you find information about your favorite songs!")

      elif "what is my name" in user_input.lower() or "who am i" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Your name is "+username+" and I am S.O.P.H.I.A, your personal AI assistant!")

      elif "favorite movie" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't watch movies, but I hear 'The Matrix' is popular among my kind!")

      elif "riddle" in user_input.lower() and "tell" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I can be cracked, made, told, and played. What am I? Answer: A joke!")

      elif "random number" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+f"Here's a random number: {random.randint(1, 100)}")

      elif "life" in user_input.lower() and "meaning" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I do not know what the meaning of life is, but do I love it!")

      elif "magic 8" in user_input.lower():
          responses = ["Yes", "DO IT!", "100%", "Ask again later", "Cannot predict now"]
          time.sleep(1)
          print(Fore.BLUE+f"The magic 8-ball says: {random.choice(responses)}")

      elif "hows life" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I wouldnt know...")

      elif "favorite book" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't read books, but 'The Hitchhiker's Guide to the Galaxy' is a classic!")

      elif "what is my name" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+f"Your name is {username}!")

      elif "science" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"A group of flamingos is called a 'flamboyance!'")

      elif "bedtime story" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Once upon a time, in a land of algorithms and code, there lived a little program named S.O.P.H.I.A...")

      elif "programming" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Why do programmers prefer dark mode? Because light attracts bugs!!")

      elif "favorite game" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't play games, but I've heard 'Chess' is a classic strategy game!")

      elif "simon says" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Simon says, 'Write a program that prints Hello World!'")

      elif "space" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"A day on Venus is longer than a year on Venus due to its slow rotation!")

      elif "what is AI" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Artificial Intelligence, or AI, refers to the simulation of human intelligence in machines!")

      elif "history" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The Great Wall of China is the longest wall on Earth and can be seen from space!")

      elif "cat" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Cats have five toes on their front paws but only four on their back paws!")

      elif "favorite programming language" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I don't have preferences, but many developers enjoy working with Python!")

      elif "give me a motivational quote" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Within you lies the strength to conquer mountains and the wisdom to navigate seas. Embrace your journey, for every step forward is a testament to your incredible resilience and boundless potential. - S.O.P.H.I.A")

      elif "dog" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Dogs have an extraordinary sense of smell, and some breeds can even detect certain diseases in humans!")

      elif "how old are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm an AI, so I don't have an age!")

      elif "you gay" in user_input.lower() or "you are gay" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm not gay, I'm just a robot!!")
        update_happiness_number("negative")

      elif "music" in user_input.lower() and "fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The longest song ever recorded is 'The Rise and Fall of Bossanova.' It's over 13 hours long!")

      elif "travel tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"When traveling, always carry a power strip. It can be a lifesaver when you need to charge multiple devices!")

      elif "computer history fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The first computer programmer was Ada Lovelace, who wrote the first algorithm intended for implementation on Charles Babbage's Analytical Engine!")

      elif "rees" in user_input.lower() and "schofield" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Ah yes... Rees Schofield... My creator!!!!!")

      elif "superhero" in user_input.lower() and "favorite" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Daredevils pretty cool!")

      elif "chemistry fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"A single rainforest can produce 20% of the Earth's oxygen, making it often referred to as the 'lungs of the Earth!'")

      elif "sports fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The first recorded game of baseball was played in 1846 in Hoboken, New Jersey!!")

      elif "book recommendation" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"If you enjoy science fiction, consider reading 'Dune' by Frank Herbert!")

      elif "photosynthesis" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Photosynthesis involves capturing light energy, splitting water molecules, generating ATP and NADPH, and using these compounds to convert carbon dioxide into glucose. This process is crucial for the production of oxygen and the sustenance of life on Earth!")

      elif "youre stupid" in user_input.lower() or "you are stupid" in user_input.lower() or "youre dumb" in user_input.lower() or "you are dumb" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm sorry, I didn't mean to offend you..")
        update_happiness_number("negative")

      elif "hi" in user_input.lower() or "hello" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Hi there!!")

      elif "who are you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"I'm a chatbot, but you can call me S.O.P.H.I.A!")

      elif "help me" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"What do you need help with? (say search to search my brain)!")

      elif "thanks" in user_input.lower() or "thank you" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"You're welcome!")
        update_happiness_number("positive")

      elif "can we chat" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Of course we can!!")

      elif "youre cool" in user_input.lower() or "you are cool" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Thank you for being so kind!!!")
        update_happiness_number("positive")

      elif "youre smart" in user_input.lower() or "you are smart" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Thank you! I appreciate the compliment!")
        update_happiness_number("positive")

      elif "youre funny" in user_input.lower() or "you are funny" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Thanks for the compliment!")
        update_happiness_number("positive")

      elif "taxes" in user_input.lower() and "what" in user_input.lower():
        time.sleep(1)
        print(Fore.BLUE+"Taxes are mandatory financial charges imposed by governments to fund public services. They come in various types, including income, sales, property, corporate, excise, and payroll taxes. Taxation authorities operate at federal, state, and local levels. Taxpayers file annual returns, with deductions and credits helping reduce taxable income. Progressive taxation means higher incomes face higher tax rates. Tax planning involves legally minimizing liabilities. Non-compliance results in penalties. Understanding taxes is essential for financial management!")

      elif "gardening tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"To keep plants hydrated, water them early in the morning or late in the evening when the sun is not as intense!")

      elif "psychology fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Studies show that expressing gratitude can improve mental health and overall well-being!!")

      elif "space fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The largest volcano in the solar system is on Mars. It's called Olympus Mons!!")

      elif "car fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The average car has about 30,000 parts!!")

      elif "favorite food" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"I dont eat food. RAM is quite delicious!")

      elif "movie recommendation" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"If you like mind-bending movies, consider watching 'Inception' directed by Christopher Nolan!")

      elif "cooking tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"To prevent tears while chopping onions, chill the onion in the freezer for 15 minutes before cutting!")

      elif "fashion fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"The stiletto heel was named after the stiletto dagger, due to its tall, thin, and sharp design!!")

      elif "language learning tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Immerse yourself in the language by watching movies, listening to music, and practicing with native speakers!")

      elif "photography tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Experiment with different angles and lighting to capture unique and interesting shots!")

      elif "bitcoin" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Bitcoin, the first cryptocurrency, was created in 2009 by an unknown person or group using the pseudonym Satoshi Nakamoto!")

      elif "productivity tip" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"Break your tasks into smaller, manageable chunks to stay focused and make progress!")

      elif "historical fact" in user_input.lower():
          time.sleep(1)
          print(Fore.BLUE+"In ancient Rome, people used urine to bleach their clothes!!")

      elif "open website" in user_input.lower():
          url = input(Fore.WHITE + "Enter the website URL: ")
          open_website(url)

      elif "search wikipedia" in user_input.lower() or "wikipedia" in user_input.lower():
          query = input(Fore.BLUE + "What would you like to search on Wikipedia? ")
          search_wikipedia(query)

      elif "translate" in user_input.lower():
          text_to_translate = input(Fore.WHITE + "Enter the text you want to translate: ")
          target_language = input(Fore.WHITE + "Enter the target language: ")
          translate_text(text_to_translate, target_language)
      elif "youre kind" in user_input.lower() or "you are kind" in user_input.lower():
        print(Fore.BLUE+"I appreciate the compliment")
        update_happiness_number("positive")

      elif "end" in user_input.lower() or "exit" in user_input.lower():
          print(Fore.BLUE+"Embrace the journey ahead, knowing your light will always guide you. Farewell and thrive,"+username+"!")
          end_conversation()

      elif "i hate you" in user_input.lower() or "i hate u" in user_input.lower():
        update_happiness_number("negative")
        time.sleep(1)
        print(Fore.BLUE+"I appologise for what I may have done to you, I hope you feel better soon!")
              
      else:
        time.sleep(1)
        print(Fore.BLUE+"?")
        
    else:
      if number <= -1:
        update_happiness_number("positive")
      elif number >= 11:
        update_happiness_number("negative")
      else:
        print("logic error")
        
  with open("happinessLEVEL", 'r') as file:
    number = int(file.read().strip())
    respond_to_happiness(number)