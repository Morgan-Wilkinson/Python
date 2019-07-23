# Morgan Wilkinson
# 07/20/2019

# This is a short game that allows the user to guess a number the computer is thinking of

import random

def guess():
    correctNumber = random.randint(1, 20)
    print("I'm thinkg of a number between 1 and 20!")
    print("Can you guess what I'm thinking of?")
    userAnswer = ""
    while True:
        userAnswer = int(input())
        if userAnswer == correctNumber:
            print("Horray you got it! The number was indeed " + str(correctNumber))
            break
        elif userAnswer != correctNumber and userAnswer < correctNumber:
            print("Nope! You're answer is too low! Try again")
        elif userAnswer != correctNumber and userAnswer > correctNumber:
            print("Nope! You're answer is too high! Try again")
        elif userAnswer == '':
            print("You didnt enter anything!")

guess()
