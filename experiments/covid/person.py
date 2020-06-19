import random
import pygame
import time
import numpy as np
from simulation.agent import Agent
from simulation import helperfunctions
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
        self.p_infection = self.calc_prob_infection()  # find prob of infection
        self.infected_at = None
        self.clock = pygame.time.Clock()
        self.count = 0
        self.beta = p.i
        self.gama = p.r
        self.state = p.INFECTIOUS if infected else p.SUSCEPTIBLE
        self.color = p.ORANGE if self.state == p.SUSCEPTIBLE else p.RED

    def update_actions(self):
        # print(self.state)
        # avoid any obstacles in the environment
        for obstacle in self.population.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()

        if self.state == p.RECOVERED:
            # since agent recovered, no need for further calculation
            return

        if self.state == p.SUSCEPTIBLE:
            # TODO: change the radius to a parameter
            all_neighbors = self.population.find_neighbors(self, radius=25)
            all_susceptible = []
            for agent in all_neighbors:
                if agent.state is not p.RECOVERED:
                    all_susceptible.append(agent)
                    # the first part is be beta * Si;
                    # where Si is the infection prob. of the susceptible agents
                    # then that minus the prob. of recovery
                    agent.p_infection += self.beta * agent.p_infection - self.gama * agent.p_infection
                # another approach is to take the average of susceptible ones.

            neighbors_in_radius = len(all_susceptible) >= 1
            # TODO: .8 can be 1.0 or 0.9; for a higher prob. of being infected.
            if neighbors_in_radius and self.p_infection >= 0.8:
                self.state = p.INFECTIOUS
                self.color = p.RED
                if not self.infected_at:
                    self.infected_at = self.clock.tick()
        if self.state == p.INFECTIOUS:
            self.count += 1
            # TODO: (maybe) change the time for an agent to recover based on the recovery rate;
            # recovery and infection rates should sum up to 1; i.e. probability
            # the time can then be calculated as 1 / r
            if self.count >= 500:
                self.state = p.RECOVERED
                self.color = p.GREEN
                self.infected_at = None
        self.update_color()

        if p.SOCIAL_DISTANCING:  # adapts direction of the agents to
            align_force, cohesion_force, separate_force = self.neighbor_forces()
            # combine the vectors in one
            steering_force = align_force * p.ALIGNMENT_WEIGHT + cohesion_force * p.COHESION_WEIGHT + separate_force * p.SEPARATION_WEIGHT
            # adjust the direction
            self.steering += helperfunctions.truncate(steering_force / self.mass, p.MAX_FORCE)

    def update_color(self):
        self.image.fill(self.color)

    def calc_prob_infection(self):
        # TODO: the rate could/should be based on a parameter; easier for farther calculations!
        # return round(random.uniform(0.3, 0.8), 1)
        return p.i

    def calc_infected_time(self):
        t = self.clock.tick()
        # print(t)
        return t / 1000

    def neighbor_forces(self):

        align_force, cohesion_force, separate_force = np.zeros(2), np.zeros(2), np.zeros(2)

        # find all the neighbors based on its radius view
        neighbors = self.population.find_neighbors(self, p.RADIUS_VIEW)

        # if there are neighbors, estimate the influence of their forces
        if neighbors:
            align_force = self.align(self.population.find_neighbor_velocity(neighbors))
            cohesion_force = self.cohesion(self.population.find_neighbor_center(neighbors))
            separate_force = self.population.find_neighbor_separation(self, neighbors)

        return align_force, cohesion_force, separate_force

    def align(self, neighbor_force):
        """
        Function to align the agent in accordance to neighbor velocity
        :param neighbor_force: np.array(x,y)
        """
        return helperfunctions.normalize(neighbor_force - self.v)

    def cohesion(self, neighbor_center):
        """
        Function to move the agent towards the center of mass of its neighbors
        :param neighbor_rotation: np.array(x,y)
        """
        force = neighbor_center - self.pos
        return helperfunctions.normalize(force - self.v)
