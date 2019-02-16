#   
#   montyHall.py
#
#   Author:     Joe Dill
#   Email:      thisisjoedill@gmail.com
#   
#   The program simulates the Monty Hall Gameshow problem over many many games
#   to evaluate how you will perform if you always switch, versus if you never switch.
#   To exagerate the difference, games with more and more doors are also simulated.
#  
#   For more information on this problem, watch this video by Numberphile:
#   https://youtu.be/4Lb-6rxZxx0
#   
#   The results of this simulation will be exported into a csv file named 'montyHall.csv'
#
#   Required modules: csv, random
#   

import random
import csv

class Door:
    def __init__(self,has_car=False):
        self._has_car = has_car
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return 'Door(%s)' % self.hasCar()
    def hideCar(self):
        self._has_car = True
    def hasCar(self,yes_no=True):
        return self._has_car
    def hasZonks(self,yes_no=True):
        return not self.hasCar()


def game(switch,num_doors=3):

    # Setup
    doors = [Door() for _ in range(num_doors)]  # Instantiate doors
    random.choice(doors).hideCar()              # Hide car behind one door
    choice = random.choice(doors)               # Randomly choose a door

    # Remove all doors except for 'choice' and the door with the car
    # If 'choice' has a car, leave one door closed
    i = 0
    while len(doors) > 2:
        #print("length: " + str(len(doors)))
        door = doors[i]
        if door == choice or door.hasCar():
            i += 1
        else:
            doors.remove(door)

    print(doors)
    
    # Switch doors if instructed to do so
    if switch:
        #print((doors.index(choice)+1)%2)
        choice = doors[(doors.index(choice)+1)%2]

    return choice.hasCar()

def playGames(switch,num_games=1000,num_doors=3):
    wins = 0
    for _ in range(num_games):
        if game(switch,num_doors):
            wins += 1
    return wins/num_games   # win percentage

def main():

    # Parameters for study
    max_doors           =   30      #   We will simulate games with 3 doors up through games with this number of doors
    three_door_games    =   10000   #   Number of trial games we will play for the 3-door case
    other_door_games    =   1000    #   Number of trials games we will play for all other cases
    num_games = lambda num_doors : {True:three_door_games,False:other_door_games}[num_doors==3]
        # Lambda expression determines how many games to play given number of doors

    # Theoretical result calculation
    theoretical_result = {
        True    :   lambda num_doors : (num_doors-1)/num_doors,
        False   :   lambda num_doors : 1/num_doors
    }
    # Theoretically, your chances of winning the Monty Hall gameshow are 
    #   1 in [# of doors]                   if you NEVER switch, 
    #   [# of doors - 1] in [# of doors]    if you ALWAYS switch.
    
    # Make File
    with open("montyHall.csv",'w',newline='') as file:
        
        # Write data to a csv file
        writer = csv.writer(file,)
        writer.writerow(["Doors","Switch?","Theoretical","Experimental"]) # Header
        
        ## Run simulation! ##

        # Do all cases where your strategy is to keep you original guess,
        # then all cases where the strategy is to switch.
        for strategy in [True,False]:
            for num_doors in range(3,max_doors+1):
                writer.writerow(
                    [
                        num_doors,
                        {True:"Yes",False:"No"}[strategy],
                        theoretical_result[strategy](num_doors),
                        playGames(
                            switch      =   strategy,
                            num_games   =   num_games(num_doors),
                            num_doors   =   num_doors
                        )
                    ]
                )


if __name__=="__main__":
    main()