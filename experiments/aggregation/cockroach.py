import pygame
import random
import numpy
from experiments.aggregation import parameters as p
from simulation import helperfunctions
from simulation.agent import Agent


class Cockroach(Agent):
    def __init__(self,
                 pos,
                 velocity,
                 aggregation,
                 image='experiments/aggregation/images/ant.png'):
        super(Cockroach, self).__init__(pos,
                                        velocity,
                                        image,
                                        max_speed=p.MAX_SPEED,
                                        min_speed=p.MIN_SPEED,
                                        mass=p.MASS,
                                        width=p.WIDTH,
                                        height=p.HEIGHT,
                                        dT=p.dT)

        self.aggregation = aggregation

    def update_actions(self):
        for obstacle in self.aggregation.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle(obstacle.pos, False)

        for site in self.aggregation.objects.sites:
            collide = pygame.sprite.collide_mask(self, site)
            if bool(collide):
                # maybe measure time
                self.change_state(p.JOINING)
                # print(random.random())
                # self._state.append(p.JOINING)
            else:
                self.change_state(p.WANDERING)
        self.site_behavior();

    def site_behavior(self):
        # join or leave with a certain prob.
        # print(self._state)
        pass

    def change_state(self, state):
        p_state = self._state.pop()
        if state == p.WANDERING:
            # if agent is joining, let it be
            if p_state == p.JOINING:
                self._state.append(p_state)
                pass
            else:
                self._state.append(state)

        elif state == p.STILL:
            # calculate the prob. of staying/leaving and change the state
            self._state.append(state)
        elif state == p.JOINING:
            in_center = pygame.sprite.spritecollide(
                self, self.aggregation.objects.sites, False,
                pygame.sprite.collide_circle_ratio(0.7))
            # if collide, then set dt to 0; stop agent
            if len(collide):# and prev_state != p.WANDERING:
                print(random.random(), len(collide), prev_state)
                self.dT = 0
    #         if bool(collide):
    #             self.avoid_obstacle(obstacle.pos, self.flock.object_loc)

    #     align_force, cohesion_force, separate_force = self.neighbor_forces()

    #     #combine the vectors in one
    #     steering_force = align_force * p.ALIGNMENT_WEIGHT  + cohesion_force * p.COHESION_WEIGHT + separate_force * p.SEPARATION_WEIGHT

    #     #adjust the direction of the boid
    #     self.steering += helperfunctions.truncate(steering_force / self.mass, p.MAX_FORCE)
    #     self.steering *= random.randint(2, 4) if min(steering_force) < 0 else .8
