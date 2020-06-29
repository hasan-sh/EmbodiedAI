import random
import pygame
import numpy as np
from simulation.agent import Agent
from simulation import helperfunctions, swarm
from experiments.covid import parameters as p


class Person(Agent):
    def __init__(self,
                 pos,
                 velocity,
                 population,
                 infected
                 ):
        super(Person, self).__init__(pos,
                                     velocity,
                                     color=p.ORANGE,
                                     max_speed=p.MAX_SPEED,
                                     min_speed=p.MIN_SPEED,
                                     mass=p.MASS,
                                     width=p.WIDTH,
                                     height=p.HEIGHT,
                                     dT=p.dT)
        self.population = population
        # TODO: remove this if not needed
        self.p_infection = self.calc_prob_infection()  # find prob of infection
        self.count = 0
        self.state = p.INFECTIOUS if infected else p.SUSCEPTIBLE
        self.in_center = False
        self.in_center_count = 0
        self.in_center_prob = random.random()
        self.color = p.ORANGE if self.state == p.SUSCEPTIBLE else p.RED
        self._original_pos = np.copy(pos)



    def update_actions(self):
        # print(self.state)
        # avoid any obstacles in the environment
        for obstacle in self.population.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()
        
        if self.state == p.SUSCEPTIBLE:
            self.population.datapoints.append('S')
        elif self.state == p.INFECTIOUS:
            self.population.datapoints.append('I')
            self.count += 1
            all_neighbors = self.population.find_actual_neighbors(self, radius=p.INFECTIOUS_RADIUS)
            all_susceptible = []
            for agent in all_neighbors:
                if agent.state is p.SUSCEPTIBLE:
                    all_susceptible.append(agent)
            if len(all_susceptible) > 0:
                for susceptible in all_susceptible:
                    infected_chance = random.random()
                    if infected_chance >= .5:
                        susceptible.state = p.INFECTIOUS
                        susceptible.color = p.RED
            if self.count >= 500:
                self.state = p.RECOVERED
                self.color = p.GREEN
        elif self.state == p.RECOVERED:
            self.population.datapoints.append('R')
        self.update_color()


        if p.SOCIAL_DISTANCING:  # adapts direction of the agents to
            separate_force = self.neighbor_forces()
            # combine the vectors in one
            steering_force = separate_force * p.SEPARATION_WEIGHT
            # adjust the direction
            self.steering += helperfunctions.truncate(steering_force / self.mass, p.MAX_FORCE)


        if p.FULL_LOCKDOWN:
            if self.in_center:
                self.in_center_count += 1
                if self.in_center_count >= random.randint(100, 200):
                    # go out
                    self.population.leave_center(self)
                    self.in_center = False
                    self.in_center_count = 0
            elif self.population.can_enter_center() and self.in_center_prob >= .6:
                self.population.enter_center(self)
                self.in_center = True
            else:
                self.in_center_prob = random.random()


    def update_color(self):
        self.image.fill(self.color)

    def calc_prob_infection(self):
        # TODO: the rate could/should be based on a parameter; easier for farther calculations!
        # return round(random.uniform(0.3, 0.8), 1)
        return p.i

    def neighbor_forces(self):

        separate_force = np.zeros(2)
        # find all the neighbors based on its radius view
        neighbors = self.population.find_neighbors(self, p.RADIUS_VIEW)

        # if there are neighbors, estimate the influence of their forces
        if neighbors:
            separate_force = self.population.find_neighbor_separation(self, neighbors)

        return separate_force
