import pygame
import numpy as np
from simulation.agent import Agent
from simulation import helperfunctions
from experiments.covid import parameters as p


class Person(Agent):
    _state = p.SUSCEPTIBLE  # initial state

    def __init__(self,
                 pos,
                 velocity,
                 population):
        super(Person, self).__init__(pos,
                                     velocity,
                                     color=(255, 153, 18),  # orange
                                     max_speed=p.MAX_SPEED,
                                     min_speed=p.MIN_SPEED,
                                     mass=p.MASS,
                                     width=p.WIDTH,
                                     height=p.HEIGHT,
                                     dT=p.dT)

        self.population = population

    def update_actions(self):
        pass
