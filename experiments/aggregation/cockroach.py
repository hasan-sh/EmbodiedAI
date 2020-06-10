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

    def update_actions(self):
        for obstacle in self.aggregation.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle(obstacle.pos, False)
        # _state will act as a stack; LIFO
        # this helps for controlling what the current and previous states are.
        curr_state = self._state[0]
        prev_state = None
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
