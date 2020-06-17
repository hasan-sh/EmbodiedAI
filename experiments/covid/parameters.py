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
# i = prob. of infecting others
# r = prob. recovering oneself
i = 0.8
r = 0.2


SUSCEPTIBLE = 'susceptible'
INFECTIOUS = 'infectious'
RECOVERED = 'recovered'

ORANGE = (255, 153, 18)
RED = (248, 59, 59)
GREEN = (0, 2, 187)
RED = (238, 59, 59)
GREEN = (0, 201, 87)

INFECTIOUS_RADIUS = 1

#object
FULL_LOCKDOWN = False
PLACE_OBJECT = True
OBJECT_LOC = [S_WIDTH/2., S_HEIGHT/3.]

