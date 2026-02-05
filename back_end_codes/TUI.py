import re
import time

time_sleep = 1

# Introduction
def intro_fun():
    print("""LOOK HERE (TERMINAL, u know this guy).

Hello! It is a mini game-project for simulation of our Solar system.

BEFORE RUNNING - pls check required pips in Requirements.txt file, they are required to run this program. (also I personally recomends using venv)

You suppose to say which planets you want to simulate and then setup the asteroid/comets to throw inside the system.
Then - just enjoy the graphical simulation result.

Enjoy :)""")
    input("\nType smth to enjoy :) ")
    print("\nThe control code uses TUI to navigate user.")
    time.sleep(time_sleep)


# TUI
def TUI_guide():
    time.sleep(time_sleep)
    print("""\nTUI guide:
1 - Planets setup
2 - Date setup
3 - Asteroid/comets setup
4 - simulation + graphics animation
5 - Exit
help - help (this message)

***points from 1-3 must be setup before starting the simulation***
                           
You can re setup planets, date and asteroids/comets as many times as you want, no need to exit the program.""")


# Planet input
def Planets_input_fun():
    print("""Gimme planets (not small bodies or Sun, just Planets). Separator - comma.
Planets names - strict, must follow their real names. Example - Earth, Venus, or Full - for all Planets.\n""")
    while True:
        try:
            planets_order = ["Mercury", "Venus", "Earth", "Mars", 
                        "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
            Planets_input = input("Planets input: ").split(",")
            for i in range(len(Planets_input)):
                Planets_input[i] = Planets_input[i].lower().strip().capitalize()
            if "Full" in Planets_input:
                if len(Planets_input) > 1:
                    raise ValueError(f"!!!Pls, for full system, use give only Full!!!")
                Planets_input = planets_order
                return Planets_input
            
            for i in range(len(Planets_input)):
                if Planets_input[i] not in planets_order:
                    raise ValueError(f"!!!Planet name '{Planets_input[i]}' is invalid. Please follow the real planet names!!!")
            Planets_list_intersect = set(Planets_input).issubset(set(planets_order))
            if Planets_list_intersect == True:
                Planets_input = Planets_sorting(Planets_input)
            return Planets_input
        except ValueError as e:
            time.sleep(time_sleep)
            print(f"{e}")
            continue


# Sorting funciton for planets
def Planets_sorting(plantes_list_input):
    planets_order = ["Mercury", "Venus", "Earth", "Mars", 
                 "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
    sorted_planets_list = plantes_list_input
    sorted_planets_list.sort(key=lambda x: planets_order.index(x))
    return sorted_planets_list


# Date input
def date_input_fun():
    print("""Now, gimme the date, from which simulation will begin.
For now, pls, follow the format: yyyy-mm-dd. Also, you can input Today, for today's date. \n""")
    while True:
        try:
            date_input = input("Date input: ").lower().strip()
            if date_input == "today":
                return date_input
            elif date_input_check(date_input) == True:
                return date_input
            else:
                raise ValueError("!!!Date format is invalid. Please, follow the format: yyyy-mm-dd or use Today!!!")
        except ValueError as e:
            time.sleep(time_sleep)
            print(f"{e}")
            continue


# Check for correct date input format
def date_input_check(date_input):
    pattern = r"^[1-9]{1}[0-9]{3}-(0[1-9]|10|11|12)-(0[1-9]|1[0-9]|2[0-9]|3[0-1])$"
    match = re.search(pattern, date_input)
    if match:
        return True
    else:
        return False


# Simulation speed
def graph_setup_fun():
    print("""\nWell, just to make graphics part more or less comfortable,
gimme the INTEGER digit for simulation speed.
Lets say common value for just Earth simulation - 10.
For full system simulation - 30 and more (the further planets are, the more simulation speed would be nice).
Also, I do not suggest using too high values for simulation speed, matplotlib is not almighty :) \n""")
    while True:
        try:
            graph_speed = int(input("Graph speed input (integer): "))
            if graph_speed <= 0:
                raise ValueError("!!!Graph speed must be positive integer!!!")
            return graph_speed
        except ValueError as e:
            time.sleep(time_sleep)
            print(f"{e}")
            continue


# Check for asteroids/comets setup
def asteroid_check():
    while True:
        try:
            asteroid_check_input = input("""Do you want to add asteroids/comets to throw inside the Solar system?
Y/N: """).lower().strip()
            if asteroid_check_input not in ["y", "n"]:
                raise ValueError("!!!Input must be 'Y' or 'N'!!!")
            return asteroid_check_input
        except ValueError:
            time.sleep(time_sleep)
            print("Invalid input, try again")
            continue


# Asteroid/comets setup
def asteroid_input_fun():
    if asteroid_check() == "y":
        time.sleep(time_sleep)
        print("""\nGreat! Now, gimme the names of asteroids/comets you want to throw inside the system.
Separator - comma. Asteroids/comets names should match their official names
(or numbers, actually better to use numbers, NASA API love them :)).
Example of inputs:
1) Main belt asteroids (between Mars and Jupiter): Ceres, Pallas, Vesta
2) Famous comets:
- Hartley 2 (data available from 2010-02-01 to 2012-02-01)
- c/2025 n1 (name - 3I/Atlas, data available from 2010 to today)
- 90000702 (name - 67P/Churyumov-Gerasimenko, data available from 2015 to today)
3) test_asteroid - special name for test asteroid with predefined initial conditions (not from NASA API).
4) my_asteroid - special name for your custom asteroid, you will be asked to input its initial conditions (position and velocity)""")
        asteroid_input = input("\nAsteroids/comets input: ").split(",")
        for i in range(len(asteroid_input)):
            asteroid_input[i] = asteroid_input[i].strip()
    else:
        time.sleep(time_sleep)
        print("Meh, no asteroids/comets will be added to the system :(")
        asteroid_input = []
    return asteroid_input


# Simulation starting message
def simulation_starting_message(Planets_input, date_input, Asteroid_input):
    print("Simulation setup summary:")
    time.sleep(time_sleep)
    print(f"Planets to simulate: {Planets_input}")
    time.sleep(time_sleep)
    print(f"Starting date: {date_input}")
    time.sleep(time_sleep)
    if Asteroid_input == []:
        time.sleep(time_sleep)
        print("No asteroids/comets will be added to the system")
    else:
        time.sleep(time_sleep)
        print(f"{len(Asteroid_input)} Asteroids/comets will be added to the system")
    time.sleep(time_sleep)
    print("Starting simulation...\n")
    time.sleep(time_sleep)


def main():
    # date_input_fun()
    print(f"{Planets_input_fun()}")


if __name__ == "__main__":
    main()