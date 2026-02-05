import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from back_end_codes.NASA_API_3D import get_API_data
import math


class Planet:
    count = 0
    instances = []

    def __init__(self, name = "name", r_0 = [0,0,0], velocity_0 = [0,0,0], mu = 0):
        self.name = name
        self.x0 = r_0[0]
        self.y0 = r_0[1]
        self.z0 = r_0[2]
        self.velocity_x0 = velocity_0[0]
        self.velocity_y0 = velocity_0[1]
        self.velocity_z0 = velocity_0[2]
        self.mu = mu
        self.R = math.sqrt(self.x0**2 + self.y0**2 + self.z0**2)
        self.V = math.sqrt(self.velocity_x0**2 + self.velocity_y0**2 + self.velocity_z0**2)
        Planet.count += 1
        Planet.instances.append(self)
    
    @classmethod
    def refresh(cls):
        cls.instances = []
        cls.count = 0


class Asteroid:
    count = 0
    instances = []

    def __init__(self, name = "my_asteroid", r_0 = [0,0,0], velocity_0 = [0,0,0]):
        self.name = name
        self.x0 = r_0[0]
        self.y0 = r_0[1]
        self.z0 = r_0[2]
        self.velocity_x0 = velocity_0[0]
        self.velocity_y0 = velocity_0[1]
        self.velocity_z0 = velocity_0[2]
        Asteroid.count += 1
        Asteroid.instances.append(self)
    
    @classmethod
    def refresh(cls):
        cls.instances = []
        cls.count = 0


def assert_Planets_class(Planet_input, date_input):
    Planet.refresh()
    AU = 149597870700 / 1000 #km

    for i in range(len(Planet_input)):
        planet_API_data = get_API_data(Planet_input[i], date_input, asteroid = False)
        new_planet = Planet(name = Planet_input[i],
                            r_0 = [planet_API_data["Ephem_data"]["X"] * AU, planet_API_data["Ephem_data"]["Y"] * AU, planet_API_data["Ephem_data"]["Z"] * AU],
                            velocity_0 = [planet_API_data["Ephem_data"]["VX"], planet_API_data["Ephem_data"]["VY"], planet_API_data["Ephem_data"]["VZ"]],
                            mu = planet_API_data["GM_data"])
    print("Planet class asserted")
    return Planet.instances


def assert_Asteroid_class(Asteroid_input = ["test_asteroid"], date_input = "today"):
    Asteroid.refresh()
    AU = 149597870700 / 1000 #km
    if Asteroid_input == []:
        return Asteroid.instances
    j = 1
    for i in range(len(Asteroid_input)):
        if Asteroid_input[i] == "test_asteroid":
            My_asteroid = Asteroid(name = "test_asteroid", r_0 = [max_radius(), 2*AU, 1*AU], velocity_0 = [-20, 1, -1])
        elif Asteroid_input[i] == "my_asteroid":
            print(f"\nThis is setup for ur custom asteroid_{j}")
            print("Position data in AU (1 AU ~ equal to Earth orbit radius)")
            print("Velocity data - in km/s")
            x_0 = float(input(f"Gimme x0 for my_asteroid_{j} (in AU): "))
            y_0 = float(input(f"Gimme y0 for my_asteroid_{j} (in AU): "))
            z_0 = float(input(f"Gimme z0 for my_asteroid_{j} (in AU): "))
            vx_0 = float(input(f"Gimme vx0 for my_asteroid_{j} (in km/s): "))
            vy_0 = float(input(f"Gimme vy0 for my_asteroid_{j} (in km/s): "))
            vz_0 = float(input(f"Gimme vz0 for my_asteroid_{j} (in km/s): "))
            print("")
            My_asteroid = Asteroid(name = f"my_asteroid_{j}", r_0 = [x_0 * AU, y_0 * AU, z_0 * AU], velocity_0 = [vx_0, vy_0, vz_0])
            j += 1

        else:
            asteroid_API_data = get_API_data(Asteroid_input[i], date_input, asteroid = True)
            new_asteroid = Asteroid(name = Asteroid_input[i],
                            r_0 = [asteroid_API_data["Ephem_data"]["X"] * AU, asteroid_API_data["Ephem_data"]["Y"] * AU, asteroid_API_data["Ephem_data"]["Z"] * AU],
                            velocity_0 = [asteroid_API_data["Ephem_data"]["VX"], asteroid_API_data["Ephem_data"]["VY"], asteroid_API_data["Ephem_data"]["VZ"]])
    
    print("Asteroid class asserted")
    return Asteroid.instances


def max_radius():
    max_r = 0
    for i in range(Planet.count):
        r_i = math.sqrt((Planet.instances[i].x0**2 + Planet.instances[i].y0**2))
        if r_i > max_r:
            max_r = r_i * 1.5
    return max_r


def main():
    print("Class code main")
    AU = 149597870700 / 1000 #km
    assert_Asteroid_class(Asteroid_input = [], date_input = "today")
    print(Asteroid.instances)
    # print(Asteroid.instances[0].name)
    # print(Asteroid.instances[0].velocity_x0)


if __name__ == "__main__":
    main()