import sys
import random

answers = [
    "Hello Stranger",
    "Its been a while",
    "Awesome",
    "YAY!"
]

print("Welcome to Jchat")
print("Say 'Bye' to end chat")
userInput = raw_input("Let's Chat!\n")
while userInput != "Bye":
    print random.choice(answers)
    userInput = raw_input("")
