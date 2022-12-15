examples = [
['Write a character class in python with members for strength, intelligence, and perception and methods to get and set those members.',
"""
class Character:
    def __init__(self, strength, intelligence, perception):
        self.strength = strength
        self.intelligence = intelligence
        self.perception = perception

    def get_strength(self):
        return self.strength

    def set_strength(self, strength):
        self.strength = strength

    def get_intelligence(self):
        return self.intelligence

    def set_intelligence(self, intelligence):
        self.intelligence = intelligence

    def get_perception(self):
        return self.perception

    def set_perception(self, perception):
        self.perception = perception"""],
['Write a python script that print the date and time in 5 different formats',
"""
from datetime import datetime

# get the current date and time
now = datetime.now()

# format the date and time using different formats
format1 = now.strftime("%m/%d/%Y %H:%M:%S")
format2 = now.strftime("%Y-%m-%d %H:%M:%S")
format3 = now.strftime("%d %b %Y %H:%M:%S")
format4 = now.strftime("%B %d, %Y %I:%M:%S %p")
format5 = now.strftime("%A, %B %d %Y %I:%M:%S %p")

# print the date and time in the different formats
print("Format 1:", format1)
print("Format 2:", format2)
print("Format 3:", format3)
print("Format 4:", format4)
print("Format 5:", format5)"""],
['Write a python script that will play rock, paper, scissors with a user.',
"""
# list of possible moves
moves = ['rock', 'paper', 'scissors']

# get the user's move
user_move = input("Enter your move (rock, paper, or scissors): ")

# check if the user's move is valid
if user_move not in moves:
    print("Invalid move!")
else:
    # generate the computer's move
    computer_move = random.choice(moves)

    # determine the winner
    if user_move == computer_move:
        print("It's a tie!")
    elif user_move == 'rock' and computer_move == 'scissors':
        print("You win!")
    elif user_move == 'paper' and computer_move == 'rock':
        print("You win!")
    elif user_move == 'scissors' and computer_move == 'paper':
        print("You win!")
    else:
        print("You lose!")"""],
['Write a python script for the game of mastermind.',
"""
# function to generate a random code
def generate_code():
    # list of possible colors for the code
    colors = ['R', 'G', 'B', 'Y', 'O', 'P']

    # generate a random code by choosing 4 colors
    code = random.choices(colors, k=4)

    return code

# function to check the user's guess
def check_guess(guess, code):
    # initialize the number of correct colors and positions
    correct_colors = 0
    correct_positions = 0

    # check the number of correct colors
    for color in guess:
        if color in code:
            correct_colors += 1

    # check the number of correct positions
    for i in range(len(guess)):
        if guess[i] == code[i]:
            correct_positions += 1

    return correct_colors, correct_positions

# generate the code to be guessed
code = generate_code()

# initialize the number of guesses
num_guesses = 0

# keep playing until the code is guessed or the maximum number of guesses is reached
while num_guesses < 10:
    # get the user's guess
    guess = input("Enter your guess (4 colors): ")

    # check if the guess is valid
    if len(guess) != 4:
        print("Invalid guess!")
    else:
        # check the user's guess
        correct_colors, correct_positions = check_guess(guess, code)

        # print the results of the guess
        print("Correct colors:", correct_colors)
        print("Correct positions:", correct_positions)

        # check if the code has been guessed
        if correct_positions == 4:
            print("You win!")
            break

        # increment the number of guesses
        num_guesses += 1

# if the code has not been guessed, print the correct code
if num_guesses == 10:
    print("You lose! The correct code was:", code)"""]]