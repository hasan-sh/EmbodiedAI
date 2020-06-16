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
SWARM = 'Covid'
# define the number of agents
N_AGENTS = 40

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
MAX_SPEED = 4.
MIN_SPEED = 1.

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
OBSTACLES = 0
OUTSIDE = False
N_OBSTACLES = 0

# the overall transmission is person's the average number of contacts of an agent; i = i*k
i = 0.3
r = 0.7


SUSCEPTIBLE = 'susceptible'
INFECTIOUS = 'infectious'
RECOVERED = 'recovered'

ORANGE = (255, 153, 18)
RED = (248, 59, 59)
GREEN = (0, 2, 187)
