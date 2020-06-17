import random
import pygame
import time
import numpy as np
from simulation.agent import Agent
from simulation import helperfunctions
from experiments.covid import parameters as p


class Person(Agent):
    _state = p.SUSCEPTIBLE
    _color = p.ORANGE if _state == p.SUSCEPTIBLE else p.RED  # I do not know why this is not working???? Halp???

    def __init__(self,
                 pos,
                 velocity,
                 population,
                 infected
                 ):
        super(Person, self).__init__(pos,
                                     velocity,
                                     color=self._color,
                                     max_speed=p.MAX_SPEED,
                                     min_speed=p.MIN_SPEED,
                                     mass=p.MASS,
                                     width=p.WIDTH,
                                     height=p.HEIGHT,
                                     dT=p.dT)
        self.population = population
        self.p_infection = self.calc_prob_infection()  # find prob of infection
        self.infected_at = None
        self.clock = pygame.time.Clock()
        self.count = 0
        self.beta = p.i
        self.gama = p.r
        self._state = p.INFECTIOUS if infected else p.SUSCEPTIBLE

    def update_actions(self):
        # print(self._state)
        # avoid any obstacles in the environment
        for obstacle in self.population.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()

        if self._state == p.RECOVERED:
            # since agent recovered, no need for further calculation
            # this if statement is just for fun!!
            if self.dT == p.dT:
                self.dT *= 0.2
            return

        self.p_infection = self.calc_prob_infection()  # find prob of infection
        # TODO: change 0.4 to a parameter; this should be based on a differential equation
        if self._state == p.SUSCEPTIBLE:# and self.p_infection >= 0.4:
            # TODO: change the radius to a parameter
            all_neighbors = self.population.find_neighbors(self, radius=25)
            not_recovered = []
            average_i = 0
            for agent in all_neighbors:
                if agent._state is not p.RECOVERED:
                    not_recovered.append(agent)
                    # maybe the first part should be beta * Si;
                    # where Si is the (averaged) n susceptible agents
                    agent.p_infection += self.beta * agent.p_infection - self.gama * agent.p_infection
            #         average_i += agent.p_infection

            # average_i = average_i / len(not_recovered) if average_i != 0 else 1.
            # # self.p_infection += n.e ** self.beta * average_i
            # self.p_infection += self.beta
            neighbors_in_radius = len(not_recovered) >= 1
            if neighbors_in_radius and self.p_infection >= 0.8:
                print('inf', self.p_infection)
                self._state = p.INFECTIOUS
                self._color = p.RED
                if not self.infected_at:
                    self.infected_at = self.clock.tick()
        if self._state == p.INFECTIOUS:
                #start_infection) >= 55:  # 55seconds before getting recovered
            # start_infection = self.calc_infected_time()
            self.count += 1
            # TODO: change the time for an agent to recover based on the recovery rate;
            # recovery and infection rates should sum up to 1; i.e. probability
            # the time can then be calculated as 1 / r
            # print('start', start_infection)
            # if start_infection >= 5:
            if self.count >= 500:
                self._state = p.RECOVERED
                self._color = p.GREEN
                self.infected_at = None
        self.update_color()

    def update_color(self):
        self.image.fill(self._color)


    def calc_prob_infection(self):
        # TODO: the rate could/should be based on a parameter; easier for farther calculations!
        return round(random.uniform(0.3, 0.8), 1)
        return p.i

    def calc_infected_time(self):
        t = self.clock.tick()
        # print(t)
        return t / 1000
