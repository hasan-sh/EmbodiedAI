import pygame
import numpy as np
from simulation.agent import Agent
from simulation import helperfunctions
from experiments.covid import parameters as p


class Person(Agent):

    def __init__(self,
                 pos,
                 velocity,
                 population,
                 image=pygame.draw.circle(p.SCREEN, color=(255, 153, 18), center=(200, 200), radius=20)):
        super(Person, self).__init__(pos,
                                     velocity,
                                     image,
                                     max_speed=p.MAX_SPEED,
                                     min_speed=p.MIN_SPEED,
                                     mass=p.MASS,
                                     width=p.WIDTH,
                                     height=p.HEIGHT,
                                     dT=p.dT)

        self.population = population

    def update_actions(self):
        pass
