import sys
import random

answers = [
    "Hello Stranger",
    "Its been a while",
    "Awesome",
    "YAY!"
]

print("Welcome to Jchat")
userInput = raw_input("Let's Chat!\n")
print random.choice(answers)