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
            scale = [600, 600]
            filename = 'experiments/covid/images/border.png' if p.FULL_LOCKDOWN else 'experiments/covid/images/border_open.png'

            self.objects.add_object(file=filename,
                                    pos=object_loc,
                                    scale=scale,
                                    type='obstacle')


        # add agents to the environment
        for agent in range(num_agents):
            coordinates = helperfunctions.generate_coordinates(self.screen)

            # code snipet (not complete) to avoid initializing agents on obstacles
            # given some coordinates and obstacles in the environment, this repositions the agent
            if p.PLACE_OBJECT:
                for object in self.objects.obstacles:
                    coordinates = helperfunctions.generate_coordinates(self.screen)
                    rel_coordinate = helperfunctions.relative(coordinates, (object.rect[0], object.rect[1]))
                    try:
                        while object.mask.get_at(rel_coordinate):
                            coordinates = helperfunctions.generate_coordinates(self.screen)
                            rel_coordinate = helperfunctions.relative(coordinates, (object.rect[0], object.rect[1]))


                    except IndexError:
                        pass  # not sure what to do here

            self.add_agent(Person(pos=np.array(coordinates), velocity=None, population=swarm,
                                  infected=True if agent <= 3 else False))

    def find_neighbor_separation(self, person, neighbors):  # show what works better
        separate = np.zeros(2)
        for idx in neighbors:
            neighbor_pos = list(self.agents)[idx].pos
            difference = person.pos - neighbor_pos  # compute the distance vector (v_x, v_y)
            difference /= helperfunctions.norm(difference)  # normalize to unit vector with respect to its maginiture
            separate += difference  # add the influences of all neighbors up

        return separate / len(neighbors)

    def find_neighbor_velocity(self, neighbors):
        neighbor_sum_v = np.zeros(2)
        for idx in neighbors:
            neighbor_sum_v += list(self.agents)[idx].v
        return neighbor_sum_v / len(neighbors)

    def find_neighbor_center(self, neighbors):
        neighbor_sum_pos = np.zeros(2)
        for idx in neighbors:
            neighbor_sum_pos += list(self.agents)[idx].pos
        return neighbor_sum_pos / len(neighbors)
