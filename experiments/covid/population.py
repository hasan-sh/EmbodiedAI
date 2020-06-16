import numpy as np
from simulation.swarm import Swarm
from simulation import helperfunctions
from experiments.covid.person import Person
from experiments.covid import parameters as p


class Population(Swarm):
    def __init__(self, screen_size):
        super(Population, self).__init__(screen_size)

    def initialize(self, num_agents, swarm):

        if p.PLACE_OBJECT:
            object_loc = p.OBJECT_LOC
            scale = [500, 500]
            filename = 'experiments/covid/images/border.png' if p.FULL_LOCKDOWN else 'experiments/covid/images/border_open.png'

            self.objects.add_object(file=filename,
                                    pos=object_loc,
                                    scale=scale,
                                    type='obstacle')

        # code snipet (not complete) to avoid initializing agents on obstacles
        # given some coordinates and obstacles in the environment, this repositions the agent

        if p.OBSTACLES:  # you need to define this variable
            for object in self.objects.obstacles:
                rel_coordinate = helperfunctions.relative(coordinates, (object.rect[0], object.rect[1]))
                try:
                    while object.mask.get_at(rel_coordinate):
                        coordinates = helperfunctions.generate_coordinates(self.screen)
                        rel_coordinate = helperfunctions.relative(coordinates, (object.rect[0], object.rect[1]))

                        min_x, max_x = helperfunctions.area(coordinates[0], 800)
                        min_y, max_y = helperfunctions.area(coordinates[1], 800)

                except IndexError:
                    pass  # not sure what to do here

        # add agents to the environment
        for agent in range(num_agents):
            coordinates = helperfunctions.generate_coordinates(self.screen)

            # if obstacles present re-estimate the coordinates
            if p.OBSTACLES:
                while coordinates[0] >= max_x or coordinates[0] <= min_x or coordinates[1] >= max_y or \
                        coordinates[1] <= min_y:
                    coordinates = helperfunctions.generate_coordinates(self.screen)

            self.add_agent(Person(pos=np.array(coordinates), velocity=None, population=swarm, infected=True if agent == 0 else False))
