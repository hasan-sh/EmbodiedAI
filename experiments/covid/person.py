import random
import pygame
import time
import numpy as np
from simulation.agent import Agent
from simulation import helperfunctions
from experiments.covid import parameters as p


class Person(Agent):
    _state = np.random.choice((p.SUSCEPTIBLE, p.INFECTIOUS), p=[0.8, 0.2])  # initial state: weighted random choice
    _color = None

    def __init__(self,
                 pos,
                 velocity,
                 population
                 ):
        super(Person, self).__init__(pos,
                                     velocity,
                                     color=p.ORANGE if self._state == p.SUSCEPTIBLE else p.RED,
                                     max_speed=p.MAX_SPEED,
                                     min_speed=p.MIN_SPEED,
                                     mass=p.MASS,
                                     width=p.WIDTH,
                                     height=p.HEIGHT,
                                     dT=p.dT)
        self.color = self._color
        self.population = population

    def update_actions(self):
        print(self._state)
        # avoid any obstacles in the environment
        for obstacle in self.population.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()

        p_infection = self.calc_prob_infection()  # find prob of infection
        start_infection = 0.0

        if self._state == p.SUSCEPTIBLE and p_infection >= 0.4 and len(
                self.population.find_neighbors(self, radius=25)) >= 1:
            self._state = p.INFECTIOUS
            self.color = p.RED
            start_infection = pygame.time.get_ticks()
            # print("infected")

        elif self._state == p.INFECTIOUS and self.calc_infected_time(
                start_infection) >= 55:  # 55seconds before getting recovered
            self._state = p.RECOVERED
            self.color = p.GREEN
            # print("recovered")

    def calc_prob_infection(self):
        return round(random.uniform(0.3, 0.8), 1)

    def calc_infected_time(self, start_time):
        return (pygame.time.get_ticks() - start_time) / 1000
