import numpy as np
from simulation import helperfunctions
from simulation.swarm import Swarm
from experiments.aggregation.cockroach import Cockroach
from experiments.aggregation import parameters as p


class Aggregation(Swarm):
    def __init__(self, screen_size):
        super(Aggregation, self).__init__(screen_size)
        self.object_loc = p.SYMMETRIC_SITES

    def initialize(self, num_agents, swarm):
        self.n_agents = num_agents
        object_loc = p.OBJECT_LOC
        scale = [800, 800]
        filename = 'experiments/aggregation/images/convex.png'

        self.objects.add_object(file=filename,
                                pos=object_loc,
                                scale=scale,
                                type='obstacle')

        # add site(s) to the environment
        site_filename = 'experiments/aggregation/images/greyc2.png'
        if p.SYMMETRIC_SITES:
            # make two sites
            site_1_loc = [object_loc[0] - 200, object_loc[1]]
            site_2_loc = [object_loc[0] + 200, object_loc[1]]
            if p.SITES_DIFFER:
                scale1 = [100, 100]
                scale2 = [100, 100]
            else:
                scale1 = [90, 90]
                scale2 = [100, 100]

            self.objects.add_object(file=site_filename,
                                    pos=site_1_loc,
                                    scale=scale1,
                                    type='site')
            self.objects.add_object(file=site_filename,
                                    pos=site_2_loc,
                                    scale=scale2,
                                    type='site')
        else:
            self.objects.add_object(file=site_filename,
                                    pos=object_loc,
                                    scale=[100, 100],
                                    type='site')

        min_x, max_x = helperfunctions.area(object_loc[0], scale[0])
        min_y, max_y = helperfunctions.area(object_loc[1], scale[1])

        print(self.objects.obstacles)
        #add agents to the environment
        for agent in range(num_agents):
            coordinates = helperfunctions.generate_coordinates(self.screen)
            while coordinates[0] >= max_x or coordinates[
                    0] <= min_x or coordinates[1] >= max_y or coordinates[
                        1] <= min_y:
                coordinates = helperfunctions.generate_coordinates(self.screen)

            self.add_agent(
                Cockroach(pos=np.array(coordinates), velocity=None,
                          aggregation=swarm))

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

    def find_neighbor_separation(self, boid,
                                 neighbors):  #show what works better
        separate = np.zeros(2)
        for idx in neighbors:
            neighbor_pos = list(self.agents)[idx].pos
            difference = boid.pos - neighbor_pos  #compute the distance vector (v_x, v_y)
            difference /= helperfunctions.norm(
                difference
            )  #normalize to unit vector with respect to its maginiture
            separate += difference  #add the influences of all neighbors up
        return separate / len(neighbors)
