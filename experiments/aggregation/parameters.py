def experiment0(screensize): # Single aggregation site
    area_loc1 = [screensize[0 ] /2., screensize[1] /2.]

    scale1 = [110, 110] # assuming a 1000 by 1000 screen

    big = False

    return area_loc1, scale1, big
"""
Parameter settings to be loaded in the model
"""

"""
General settings (DO NOT CHANGE)
"""
#screen settings
S_WIDTH, S_HEIGHT = 1000, 1000
SCREEN = (S_WIDTH, S_HEIGHT)

#choose how long to run the simulation
#-1 : infinite, N: finite
FRAMES=-1

#choose swarm type
SWARM = 'Aggregation'
#define the number of agents
N_AGENTS = 40
#object location
OBJECT_LOC = [S_WIDTH/2., S_HEIGHT/2.]

CONVEX = True


#Agent Settings:
#agent size
WIDTH=10
HEIGHT=8
#update
dT=0.2
#agents mass
MASS=20
#agent maximum/minimum speed
MAX_SPEED = 7.
MIN_SPEED = 4.


#Boid Settings:
#velocity force
MAX_FORCE = 8.

"""
Simulation settings to adjust:
"""

"""
Aggregation class parameters (defines the environment of where the aggregation to act)
"""
#Define the environment
SYMMETRIC_SITES = True
SITES_DIFFER = True


"""
Boid class parameters
"""
#view of site and other agents
RADIUS_VIEW=100



