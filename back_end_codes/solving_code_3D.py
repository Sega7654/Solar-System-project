import sys
import os

# Feature that allows to import from children directory (for control code) AND to run this code without problems
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import numpy as np
from scipy.integrate import odeint
from datetime import date
import os

from back_end_codes.diffur_asteroid_3D import system_asteroid_3D
from back_end_codes.Class_code_3D import Planet
from back_end_codes.Class_code_3D import assert_Planets_class, assert_Asteroid_class
from back_end_codes.Class_code_3D import Asteroid


# Just creating planets and asteroid classes
def assert_Planets_and_Asteroid_classes_fun(Planet_input, date_input, Asteroid_input):
    Planets_data = assert_Planets_class(Planet_input, date_input)
    Asteroid_data = assert_Asteroid_class(Asteroid_input, date_input)
    return Planets_data, Asteroid_data


# Solving code itself
def diffur_solving_3D(Planet_input, date_input, Asteroid_input):
    Solar_system_data = assert_Planets_and_Asteroid_classes_fun(Planet_input, date_input, Asteroid_input)
    Planets_data = Solar_system_data[0]
    Asteroid_data = Solar_system_data[1]
    folder_path = create_solution_folder()
    csv_path = os.path.join(folder_path, f"{csv_name_design(Planets_data, date_input, Asteroid_data)}")

    # time array for simulation
    t = time_array()[1]
    if os.path.isfile(csv_path):
        print("Diffur solution data file exists")
        pass
    else:
        # Initial conditions array
        y_0_system = []
        if Asteroid.count > 0:
            for i in range(Asteroid.count):
                y_0_system = y_0_system + [Asteroid_data[i].x0, Asteroid_data[i].velocity_x0,
                                        Asteroid_data[i].y0, Asteroid_data[i].velocity_y0,
                                        Asteroid_data[i].z0, Asteroid_data[i].velocity_z0]

        for i in range(Planet.count):
            y_0_system = y_0_system + [Planets_data[i].x0, Planets_data[i].velocity_x0,
                                    Planets_data[i].y0, Planets_data[i].velocity_y0,
                                    Planets_data[i].z0, Planets_data[i].velocity_z0]

        mu_planets = []
        for i in range(Planet.count):
            mu_planets = mu_planets + [Planets_data[i].mu]

        # Solving the system
        sol_asteroid = odeint(system_asteroid_3D, y_0_system, t, args = (Planet.count, mu_planets, Asteroid.count))
        print("Diffur solved")

        # Save the solution to csv
        np.savetxt(csv_path, sol_asteroid, delimiter = ",")
        print("Solution saved to csv file")


def create_solution_folder():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(f"{script_dir}", "Diffur_solution_data")

    if os.path.isdir(f"{folder_path}"):
        print("Solution folder exists")
        # Diffur solution data folder exists
        return folder_path
    else:
        # Create Diffur solution data folder
        print("Solution folder created")
        os.mkdir(folder_path)
    return folder_path


def csv_name_design(Planets_data, date_input, asteroid_data):
    csv_name = ""
    if date_input == "today":
        csv_date = f"{date.today()}_"
    else:
        csv_date = f"{date_input}_"
    csv_plantes = "Pl_"
    for i in range(Planet.count):
        csv_plantes += f"{Planets_data[i].name.replace('/', '_').replace(' ', '_')}_"
    csv_asteroids = "Ast_"
    if Asteroid.count == 0:
        csv_asteroids += "no_asteroids_"
    else:
        for i in range(Asteroid.count):
            csv_asteroids += f"{asteroid_data[i].name.replace('/', '_').replace(' ', '_')}_"

    csv_name = csv_date + csv_plantes + csv_asteroids + ".csv"
    return csv_name


# For testing
def planet_R_V():
    AU = 149597870700 / 1000 #km
    for i in range(Planet.count):
        print(f"{Planet.instances[i].name}: R = {Planet.instances[i].R/AU} AU, V = {Planet.instances[i].V}")


# Fun to define simulation length and step
def time_array():
    simulation_lenght = 1000000000
    simulation_frames = 100000
    simulation_step = simulation_lenght / ( simulation_frames - 1)
    t = np.linspace(0, simulation_lenght, simulation_frames)
    return simulation_step, t


def main():
    print("Diffur solving 3D - main")
    diffur_solving_3D(["Earth", "Mars"], "today", [])
    # print(csv_name_design(Planet.instances, "today", Asteroid.instances))


if __name__ == "__main__":
    main()