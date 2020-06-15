"""
Parameter settings for covid experiment
"""

# screen settings
S_WIDTH, S_HEIGHT = 1000, 1000
SCREEN = (S_WIDTH, S_HEIGHT)

# choose how long to run the simulation
# -1 : infinite, N: finite
FRAMES = -1

# choose swarm type
SWARM = 'population'
# define the number of agents
N_AGENTS = 80
# object location
OBJECT_LOC = [S_WIDTH / 2., S_HEIGHT / 2.]
CONVEX = True

# Agent Settings:
# agent size
WIDTH = 10
HEIGHT = 8
# update
dT = 0.2
# agents mass
MASS = 20
# agent maximum/minimum speed
MAX_SPEED = 7.
MIN_SPEED = 4.

# Person Settings:
# velocity force
MAX_FORCE = 8.

"""
Simulation settings to adjust:
"""

"""
Population class parameters (defines the environment of where the flock to act)
"""
# Define the environment
OBSTACLES = False
N_OBSTACLES = 0

SUSCEPTIBLE = 'susceptible'
INFECTIOUS = 'infectious'
RECOVERED = 'recovered'
