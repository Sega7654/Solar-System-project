import sys
import os

# Feature that allows to import from children directory (for control code) AND to run this code without problems
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
from datetime import date, timedelta, datetime

from back_end_codes.Class_code_3D import Planet
from back_end_codes.Class_code_3D import Asteroid
from back_end_codes.solving_code_3D import csv_name_design, diffur_solving_3D, time_array

#tekainter - old lib for GUI graphics
#customtekainter - good lib for GUI graphics

def graph_module_3D(date_input, graph_speed):
    # Just a setup for graphing
    Planets_graph_data = {"Mercury":{"ms":4,  "color":"grey"},
                        "Venus":{"ms":5,  "color":"orange"},
                        "Earth":{"ms":5,  "color":"blue"},
                        "Mars":{"ms":4,  "color":"red"},
                        "Jupiter":{"ms":8,  "color":"orange"},
                        "Saturn":{"ms":7,  "color":"yellow"},
                        "Uranus":{"ms":6,  "color":"lightblue"},
                        "Neptune":{"ms":6,  "color":"blue"},
                        "Pluto":{"ms":3,  "color":"brown"},
                        "asteroid":{"ms":2,  "color":"white"}}

    ##---------------------------------------------------------------------------------------------
    # Get data from the saved csv file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(f"{script_dir}", "Diffur_solution_data")
    csv_path = os.path.join(folder_path, f"{csv_name_design(Planet.instances, date_input, Asteroid.instances)}")
    data = np.loadtxt(csv_path, delimiter=",")


    AU = 149597870700 / 1000 #km
    n = AU
    # Simulation scale setup - finding the max radius of planets (withou asteroids)
    for i in range(6 * Asteroid.count, len(data[0,:])):
        range_max = max(abs(data[:,i]))
        if range_max > n:
            n = range_max * 1.2
    
    # Figure setup
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    ax.grid(False)

    # Draw axis in 3D
    val = [2*n,0,0]
    labels = ['x', 'y', 'z']
    colors = ['r', 'g', 'blue']
    for v in range(3):
        x = [val[v-0], -val[v-0]]
        y = [val[v-1], -val[v-1]]
        z = [val[v-2] / 10, -val[v-2] / 10]
        ax.plot(x,y,z, linewidth = 1, color = "white")
        ax.text(val[v-0], val[v-1], val[v-2] / 10, labels[v], color=colors[v], fontsize = 10)

    # Hide axes ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    # Make the real axis transparent
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    # Hide box axes
    ax._axis3don = False

    # Setting the scale
    ax.set_xlim3d([-n, n])
    ax.set_ylim3d([-n, n])
    ax.set_zlim3d([-n, n])

    # Sun point
    ax.plot(0, 0, 0, marker = "o", color = "y", ms = 5)

    # Asteroids/comets graphics setup
    if Asteroid.count > 0:
        asteroid_points = {}
        asteroid_trajectories = {}
        asteroid_labels = {}
        for i in range(Asteroid.count):
            asteroid_points[f"{Asteroid.instances[i].name}"], = ax.plot(Asteroid.instances[i].x0, Asteroid.instances[i].y0, Asteroid.instances[i].z0, label = Asteroid.instances[i].name, marker = "o", ms = Planets_graph_data["asteroid"]["ms"], color = Planets_graph_data["asteroid"]["color"])
            asteroid_trajectories[f"{Asteroid.instances[i].name}"], = ax.plot([0,1], [0,1], [0,1], linestyle="--", linewidth=0.5, color = "grey")
            asteroid_labels[f"{Asteroid.instances[i].name}"] = ax.text(Asteroid.instances[i].x0, Asteroid.instances[i].y0, Asteroid.instances[i].z0, f"{Asteroid.instances[i].name}", color="white", fontsize = 7)


    # Planets graphics setup
    planet_points = {}
    planet_trajectories = {}
    planet_labels = {}
    for i in range(Planet.count):
        if Planet.instances[i].name in Planets_graph_data:
            planet_ms = Planets_graph_data[Planet.instances[i].name]["ms"]
            planet_color = Planets_graph_data[Planet.instances[i].name]["color"]
            planet_points[f"{Planet.instances[i].name}"], = ax.plot(Planet.instances[i].x0, Planet.instances[i].y0, Planet.instances[i].z0, label = Planet.instances[i].name, marker = "o", ms = planet_ms, color = planet_color)
            planet_trajectories[f"{Planet.instances[i].name}"], = ax.plot([0,1], [0,1], [0,1], linestyle = "-", linewidth = 0.3, color = "white")
            planet_labels[f"{Planet.instances[i].name}"] = ax.text(Planet.instances[i].x0, Planet.instances[i].y0, Planet.instances[i].z0, f"{Planet.instances[i].name}", color = planet_color, fontsize = 7)

    # Create a dummy line for the time display in legend (invisible)
    Initial_time_line, = ax.plot([], [], [], label="t = 0.00")
    Initial_time_line.set_visible(False)  # Hide the line marker from legend
    time_line, = ax.plot([], [], [], label="t = 0.00")
    time_line.set_visible(False)  # Hide the line marker from legend

    # Create legend once with both entries
    leg = ax.legend(loc = "upper left")

    # Simulation step for dynamic date update in legend
    simulation_step = time_array()[0]

    # Animation update function
    def update(time):
        # Label offset
        k_lb = 10000000
        k = 0
        k_tr = 1 # delay for trajectory start
        if Asteroid.count > 0: # check for asteroids in the simulation
            # Asteroid points update
            updated_asteroid_points = []
            updated_asteroid_trajectories = []
            updated_asteroid_labels = []
            for i in range(Asteroid.count):
                # Asteroid update
                x_ast = data[int(time), k + 0]
                y_ast = data[int(time), k + 2]
                z_ast = data[int(time), k + 4]
                asteroid_points[f"{Asteroid.instances[i].name}"].set_data([x_ast], [y_ast])
                asteroid_points[f"{Asteroid.instances[i].name}"].set_3d_properties([z_ast])
                updated_asteroid_points.append(asteroid_points[f"{Asteroid.instances[i].name}"])
                # Asteroid label update
                asteroid_labels[f"{Asteroid.instances[i].name}"].set_position((x_ast + k_lb, y_ast + k_lb))
                asteroid_labels[f"{Asteroid.instances[i].name}"].set_3d_properties(z_ast + k_lb)
                updated_asteroid_labels.append(asteroid_labels[f"{Asteroid.instances[i].name}"])
                # Asteroid update trajectory
                if time > k_tr:
                    traj_x = data[0:int(time), k + 0]
                    traj_y = data[0:int(time), k + 2]
                    traj_z = data[0:int(time), k + 4]
                    asteroid_trajectories[f"{Asteroid.instances[i].name}"].set_data(traj_x, traj_y)
                    asteroid_trajectories[f"{Asteroid.instances[i].name}"].set_3d_properties(traj_z)
                    updated_asteroid_trajectories.append(asteroid_trajectories[f"{Asteroid.instances[i].name}"])
                k = k + 6
        
        # Planets update
        updated_planet_points = []
        updated_planet_trajectories = []
        updated_planets_labels = []
        # Planets points update
        for i in range(Planet.count):
            x_p = data[int(time), k + i*6]
            y_p = data[int(time), k + 2 + i*6]
            z_p = data[int(time), k + 4 + i*6]
            planet_points[f"{Planet.instances[i].name}"].set_data([x_p], [y_p])
            planet_points[f"{Planet.instances[i].name}"].set_3d_properties([z_p])
            updated_planet_points.append(planet_points[f"{Planet.instances[i].name}"])
            # Planets label update
            planet_labels[f"{Planet.instances[i].name}"].set_position((x_p + k_lb, y_p + k_lb))
            planet_labels[f"{Planet.instances[i].name}"].set_3d_properties(z_p + k_lb)
            updated_planets_labels.append(planet_labels[f"{Planet.instances[i].name}"])
            # Planets update trajectory
            if time > k_tr:
                traj_x = data[0:int(time), k + i*6]
                traj_y = data[0:int(time), k + 2 + i*6]
                traj_z = data[0:int(time), k + 4 + i*6]
                planet_trajectories[f"{Planet.instances[i].name}"].set_data(traj_x, traj_y)
                planet_trajectories[f"{Planet.instances[i].name}"].set_3d_properties(traj_z)
                updated_planet_trajectories.append(planet_trajectories[f"{Planet.instances[i].name}"])
    
        # Update legend text dynamically 
        leg.get_texts()[Planet.count + Asteroid.count].set_text(f"Initial date: {dynamic_date(date_input, 0)}")
        leg.get_texts()[Planet.count + Asteroid.count + 1].set_text(f"Current date: {dynamic_date(date_input, int(time) * simulation_step)}")
        if Asteroid.count > 0:
            return *updated_asteroid_points, *updated_asteroid_trajectories, *updated_asteroid_labels, *updated_planet_points, *updated_planet_trajectories, *updated_planets_labels,
        else:
            return  *updated_planet_points, *updated_planet_trajectories, *updated_planets_labels,

    # array for animaiton
    graphics_simulation_speed = np.arange(0, len(data[:, 0]), graph_speed)

    # the animation itself
    animation = FuncAnimation(fig, update, interval=1, blit=False, repeat=True,
                        frames = graphics_simulation_speed)
    plt.show()


# function for dynamic date update in legend
def dynamic_date(date_input, time_step):
    if date_input.lower().strip() == "today":
        initial_date = date.today()
    else:
        initial_date = datetime.strptime(date_input, "%Y-%m-%d")
    result_date = initial_date + timedelta(seconds=time_step)
    return result_date


def main():
    print("Graph module - main")
    date = "2015-01-01"
    diffur_solving_3D(["Earth"], date, ["test_asteroid"])
    graph_module_3D(date, 50)
    # print(f"{dynamic_date('2015-01-01', 86400.3)}")
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # folder_path = os.path.join(f"{script_dir}", "Diffur_solution_data")
    # csv_path = os.path.join(folder_path, f"{csv_name_design(Planet.instances, date, Asteroid.instances)}")
    # data = np.loadtxt(csv_path, delimiter=",")
    # print(len(data[:,0]))


if __name__ == "__main__":
    main()