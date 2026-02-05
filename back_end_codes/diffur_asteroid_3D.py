import math


def system_asteroid_3D(Y, t, n_planet, mu_planets, n_asteroid):
    # X, VX, Y, VY, Z, VZ - structure of Y vector (same for each planet/asteroid)
    mu_Sun = 1.327 * (10**11) #km^3/s^2
    m = 0 # index shift for asteroid
    k_in = 0 # index shift for planets
    ast = []
    if n_asteroid > 0:
        # Finding the start index for planets
        for i in range(n_asteroid):
            k_in = k_in + 6
        
        for j in range(n_asteroid):
            # Asteoid - Sun gravitational interaction, left vector part
            ast = ast + [Y[m + 1], - (mu_Sun * Y[m + 0] / (math.sqrt((Y[m + 0]**2) + (Y[m + 2]**2) + (Y[m + 4]**2))**3)),
                        Y[m + 3], - (mu_Sun * Y[m + 2] / (math.sqrt((Y[m + 0]**2) + (Y[m + 2]**2) + (Y[m + 4]**2))**3)),
                        Y[m + 5], - (mu_Sun * Y[m + 4] / (math.sqrt((Y[m + 0]**2) + (Y[m + 2]**2) + (Y[m + 4]**2))**3))]
            k = k_in
            for i in range(n_planet):
                # Asteroid - planets gravitational interaction, left vector part
                ast[m + 1] = ast[m + 1] - ( mu_planets[i] * (Y[m + 0] - Y[0 + k]) / (math.sqrt(((Y[m + 0] - Y[0 + k])**2) + ((Y[m + 2] - Y[2 + k])**2) + ((Y[m + 4] - Y[4 + k])**2))**3))
                ast[m + 3] = ast[m + 3] - ( mu_planets[i] * (Y[m + 2] - Y[2 + k]) / (math.sqrt(((Y[m + 0] - Y[0 + k])**2) + ((Y[m + 2] - Y[2 + k])**2) + ((Y[m + 4] - Y[4 + k])**2))**3))
                ast[m + 5] = ast[m + 5] - ( mu_planets[i] * (Y[m + 4] - Y[4 + k]) / (math.sqrt(((Y[m + 0] - Y[0 + k])**2) + ((Y[m + 2] - Y[2 + k])**2) + ((Y[m + 4] - Y[4 + k])**2))**3))
                k = k + 6
            m = m + 6
    # planets - Sun gravitational interaction
    planets = []
    k = k_in
    for i in range(n_planet):
        # Planets left vector part
        planets = planets + [Y[1 + k], - (mu_Sun * Y[0 + k] / (math.sqrt((Y[0 + k]**2) + (Y[2 + k]**2) + (Y[4 + k]**2))**3)),
                             Y[3 + k], - (mu_Sun * Y[2 + k] / (math.sqrt((Y[0 + k]**2) + (Y[2 + k]**2) + (Y[4 + k]**2))**3)),
                             Y[5 + k], - (mu_Sun * Y[4 + k] / (math.sqrt((Y[0 + k]**2) + (Y[2 + k]**2) + (Y[4 + k]**2))**3))]
        k = k + 6
    
    # Simulation left vector
    vect_left = ast + planets
    return vect_left