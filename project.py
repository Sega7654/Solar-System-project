from back_end_codes import *


## RUN ME :)


def main():
    intro_fun()
    TUI_guide()
    
    while True:
        try:
            # User input check
            my_input = input("\nMy input: ")
            if my_input not in ["1","2","3","4","5","help"]:
                raise NameError("\n!!!Invalid input, pls follow the TUI guide!!!")
            # Planets setup
            if my_input == "1":
                Planets_input = Planets_input_fun()
            # Date setup
            if my_input == "2":
                date_input = date_input_fun()
            # Asteroid setup
            if my_input == "3":
                asteroid_input = asteroid_input_fun()
            # API call, Classes assert, Solving the Diffur + graphics
            if my_input == "4":
                if "Planets_input" not in locals():
                    raise ValueError("!!!No planets setup simulation. Use 1 to setup planets!!!")
                if "date_input" not in locals():
                    raise ValueError("!!!No date setup for simulation. Use 2 to setup date!!!")
                if "asteroid_input" not in locals():
                    raise ValueError("!!!No asteroids/comets setup for simulation. Use 3 to setup asteroids/comets!!!")
                simulation_starting_message(Planets_input, date_input, asteroid_input)
                diffur_solving_3D(Planets_input, date_input, asteroid_input)
                graph_speed = graph_setup_fun()
                graph_module_3D(date_input, graph_speed)
            # Just exit
            if my_input == "5":
                time.sleep(1)
                print("Exiting...")
                break
            # TUI guide
            if my_input == "help":
                TUI_guide()
        except NameError as e:
            print(f"{e}")
        except ValueError as e:
            print(f"{e}")


# Check for correct date input format
def date_input_check_1(date_input):
    pattern = r"^[1-9]{1}[0-9]{3}-(0[1-9]|10|11|12)-(0[1-9]|1[0-9]|2[0-9]|3[0-1])$"
    match = re.search(pattern, date_input)
    if match:
        return True
    else:
        return False


# Planet input
def Planets_input_fun_1(input):
    planets_order = ["Mercury", "Venus", "Earth", "Mars", 
                "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
    Planets_input = input.split(",")
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


# Check for asteroids/comets setup
def asteroid_check_1(input):
    asteroid_check_input = input.lower().strip()
    if asteroid_check_input not in ["y", "n"]:
        raise ValueError("!!!Input must be 'Y' or 'N'!!!")
    return asteroid_check_input


if __name__ == "__main__":
    main()




