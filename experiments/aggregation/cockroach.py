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
        pass
    #     for obstacle in self.aggregation.objects.obstacles:
    #         collide = pygame.sprite.collide_mask(self, obstacle)
    #         if bool(collide):
    #             self.avoid_obstacle(obstacle.pos, self.flock.object_loc)
    #     self.wander()

    #     #avoid any obstacles in the environment
    #     for obstacle in self.flock.objects.obstacles:
    #         collide = pygame.sprite.collide_mask(self, obstacle)
    #         if bool(collide):
    #             self.avoid_obstacle(obstacle.pos, self.flock.object_loc)

    #     align_force, cohesion_force, separate_force = self.neighbor_forces()

    #     #combine the vectors in one
    #     steering_force = align_force * p.ALIGNMENT_WEIGHT  + cohesion_force * p.COHESION_WEIGHT + separate_force * p.SEPARATION_WEIGHT

    #     #adjust the direction of the boid
    #     self.steering += helperfunctions.truncate(steering_force / self.mass, p.MAX_FORCE)
    #     self.steering *= random.randint(2, 4) if min(steering_force) < 0 else .8
