import random

import pygame
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
        self._state = ['wandering', 'still', 'still','still']

    def update_actions(self):
        for obstacle in self.aggregation.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle(obstacle.pos, False)
        # _state will act as a stack; LIFO
        # this helps for controlling what the current and previous states are.
        curr_state = self._state[-1]
        # if len(self._state) > 0:
        #     prev_state = self._state.pop()

        if curr_state == p.WANDERING:
            # check for collision once the agent within the .x*site radius; x=0.7 now!
            # this way we won't need timers and all that hassle
            collide = pygame.sprite.spritecollide(
                self, self.aggregation.objects.sites, False,
                pygame.sprite.collide_circle_ratio(0.7))
            # if collide, then set dt to 0; stop agent
            if len(collide):# and prev_state != p.WANDERING:
                print(random.random(), len(collide))
                self.dT = 0
                self._state.append("still")


        if curr_state == p.STILL:
            still_for_long_enough = True;
            for x in range(2):
                if not(self._state[x] == p.STILL):
                    still_for_long_enough = False

            if still_for_long_enough:
                self._state.append("leaving")

        if curr_state == p.LEAVING:
            leaving_for_long_enough = True;
            for x in range(2):
                if not (self._state[x] == p.STILL):
                    leaving_for_long_enough = False

            if leaving_for_long_enough:
                self._state.append("leaving")