__author__ = 'Paul Conway'
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 19 10:33:15 2014

@author: Paul
"""
import os
# Clear the screen
os.system('cls')

# Requires numpy for matrix/vector ops and random functions
from numpy import zeros, array, string_, copy
from numpy.random import randint
import sys


def main(argv):
# Some defaults
    GAMES = 10
    COMPUTER_SWITCH_CHOICE = True
    SELF_PLAY = False

# Initialize the main variables
    behind_door = zeros((3,1))
    init_door = array((3,1), dtype=string_)
    init_door = ['##1##','##2##','##3##']
    #car  = 'car  '
    goat = 'goat '
    won = 0

# Process the command line args "-r <rounds>". Computer plays itself.
# And any string for last arg will tell computer to stick rather than switch
    if len(argv) > 0:
        if argv[0] == '-r':
            SELF_PLAY = True
            GAMES = int(argv[1]) if len(argv) >= 2 else 100
            COMPUTER_SWITCH_CHOICE = False if len(argv) == 3 else True
        else:
# If -r isn't the first arg then process this as the number of games to play
            SELF_PLAY = False
            try:
                GAMES = int(argv[0])
            except:
                print('''*** Bad command-line argument ***

SYNTAX:
For automated play -
    monty_hall -r <rounds> <always_switch_flag>              ... <always_switch_flag> can be any char/string
or, interactive play -
    monty_hall <rounds>''')
                exit(1)
# Intro
    print('''
    Welcome to the game show "Let's Make A Deal" with your host, Monty Hall.
    You're in the final round, facing three closed doors. Behind one of the
    doors is a car. Behind the other two are goats. Nobody walks away empty
    handed!

    Choose a door. Monty will then open one of the other doors showing you a
    goat behind it. After showing you the goat, Monty will give you a chance to
    stick to your original choice or switch to the door that he didn't open.

    Let's make a deal ...''')

# We default at 10 games, more can be selected on command line
    for games in range(GAMES):
        print('\nGame {0} of {1}'.format(games + 1, GAMES))
# Choose a door at random to have the car behind
        car_behind = randint(3)
        behind_door[car_behind] = 1

# Set all doors closed
        door = copy(init_door)

        while True:
# Show closed doors
            print('\n\n\n{0} {1} {2}\n'.format(door[0],door[1],door[2]))
# Initial door choice
            try:
                if SELF_PLAY:
# Computer chooses initial door at random
                    player_choice = randint(3)
                else:
# Subtracting one because array indices begin at 0
# If player chooses 0 then game exits
                    player_choice= int(input('Choose a door (1, 2, 3, or 0 to quit):')) - 1
                if player_choice < -1 or player_choice > 2:
                    raise ValueError
            except ValueError:
                print('\nERROR: Please choose a number between 1 and 3.\n\n')
            else:
                break
# Player chose to quit
        if player_choice == -1:
            games -= 1
            break

# Monty always chooses a goat door
        if player_choice == car_behind:
# If player chose car door then choose one of the other two at random
            monty_choice = (player_choice + 1 + randint(2)) % 3
        else:
# Otherwise choose the door with the goat behind it
            for i in range(3):
                if not (i == player_choice or i == car_behind):
                    monty_choice = i
                    break
        print('\nMonty opens door number {0}:\n'.format(monty_choice + 1))
        door[monty_choice] = 'Goat'
# Show Monty's goat
        print('{0} {1} {2}\n'.format(door[0],door[1],door[2]))
        if SELF_PLAY:
# Computer switches or sticks according to command line. Switch by default.
            switch_door = COMPUTER_SWITCH_CHOICE
            if switch_door:
                print("Computer switches to other door")
            else:
                print("Computer sticks with original door")
        else:
# Player gets to choose to switch or to stick
            while True:
                try:
                    player_yn = input('''
    You chose door number {0}. Monty's shown you a goat behind door number {1}.
    Would you like to change your mind and switch to the door Monty didn't open? (y/n):'''
                                      .format(player_choice + 1, monty_choice + 1))
                    if not (len(player_yn) == 1 and player_yn in 'YNyn'):
                        raise ValueError
                except ValueError:
                    print('\nERROR: Please choose Y or N.\n\n')
                else:
                    switch_door = (player_yn == 'Y' or player_yn == 'y')
                    break

# Switch to non-open, non-chosen door if switch is requested
        if switch_door:
            for i in range(3):
                if not (i == player_choice or i == monty_choice):
                    player_choice = i
                    break

        print('\n\nYou have won ... ', end = "")
        if player_choice == car_behind:
            print('A CAR!!!!\n')
            won += 1
        else:
            print(' a goat :-(\n')
        door[car_behind] = ' Car '
        print('{0} {1} {2}\n'.format(door[0],door[1],door[2]))

        print('\n    ################### NEW GAME ###################')

    print('You won {0} out of the {1} games you played'.format(won, games + 1))
    if SELF_PLAY == True:
        print('Computer chose {0} every time.'.format('to switch' if COMPUTER_SWITCH_CHOICE else 'to stick'))

# For command line execution
if __name__ == "__main__":
# Remove program path/name from command line options as we call main()
   main(sys.argv[1:])