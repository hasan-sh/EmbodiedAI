import random

import pygame
import random
import numpy
from experiments.aggregation import parameters as p
from simulation import helperfunctions
from simulation.agent import Agent


class Cockroach(Agent):
    _state = [p.WANDERING]
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
        self._state = ['wandering']

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
                self.change_state(self._state[-1])
        self.site_behavior()

    def site_behavior(self):
        # join or leave with a certain prob.
        # print(self._state)
        pass

    def change_state(self, state):
        c_state = self._state.pop()
        p_state = None
        if bool(self._state):
            p_state = self._state.pop()
        if state == p.WANDERING:
            # if agent is joining, let it be
            if p_state == p.JOINING:
                self._state.append(p_state)
            elif p_state == p.LEAVING:
                self._state.append(p_state)
                self._state.append(state)
            else:
                self._state.append(state)
        elif state == p.STILL:
            # calculate the prob. of staying/leaving and change the state
            pl = self.leave()
            if pl <= 0.2:
                self._state.append(state)
                self._state.append(p.LEAVING)
            else:
                self._state.append(c_state)
        elif state == p.JOINING and p_state != p.LEAVING:
            in_center = pygame.sprite.spritecollide(
                self, self.aggregation.objects.sites, False,
                pygame.sprite.collide_mask)#collide_circle_ratio(0.7))
            if bool(in_center):# and prev_state != p.WANDERING:
                # the following is just to make them stop smoothly
                self.dT -= 0.007
                if self.dT <= 0.01:
                    self.dT = 0
                    self._state.append(state)
                    self._state.append(p.STILL)
                else:
                    self._state.append(c_state)
            else:
                self._state.append(c_state)
        else:
            # make agent move again
            self.dT = p.dT
            self._state.append(state)
            self._state.append(p.WANDERING)
    
    def leave(self):
        i_s = self.agent_in_sites()
        # the follwoing gets all sites, maybe, in some way, 
        # we should include the size of the current site into the probablity.
        # for s in self.aggregation.objects.sites:
        #     print('pos', s.rect)
        len_is = len(i_s)
        # the following isn't right; agent only knows within a radius!
        p = len_is / self.aggregation.n_agents
        # the next is a prob. within the site 
        # p = random.randint(1, len_is - 2 if len_is > 3 else 2) / len(i_s) 
        # awaiting a better model!
        return p
    
    def agent_in_sites(self):
        result = []
        for a in self.aggregation.agents:
            result += pygame.sprite.spritecollide(a, self.aggregation.objects.sites, False, pygame.sprite.collide_circle)
        return result
    
