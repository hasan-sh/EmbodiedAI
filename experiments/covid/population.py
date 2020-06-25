import numpy as np
from simulation.swarm import Swarm
from simulation import helperfunctions
from experiments.covid.person import Person
from experiments.covid import parameters as p
import random

object_locs_full_lockdown = \
    [[p.S_WIDTH / 4., p.S_HEIGHT / 4],
    [p.S_WIDTH - (p.S_WIDTH / 4.), p.S_HEIGHT / 4],
    [p.S_WIDTH - (p.S_WIDTH / 4.), p.S_HEIGHT - (p.S_HEIGHT / 4)],
    [p.S_WIDTH / 4., p.S_HEIGHT - (p.S_HEIGHT / 4)],
    ]
object_scale_full_lockdown = [300, 300]
object_scale_full_lockdown_center = [200, 200]

class Population(Swarm):
    def __init__(self, screen_size):
        super(Population, self).__init__(screen_size)
        if p.FULL_LOCKDOWN:
            self.inside = [{'obstacle': (object_locs_full_lockdown[i], object_scale_full_lockdown), 'agents': 0} for i in range(0, len(object_locs_full_lockdown))]
            # center currently can only be one obstacle.
            self.in_center = {'obstacle': ([p.S_WIDTH / 2., p.S_HEIGHT / 2], [200, 200]), 'agents': 0}

    def initialize(self, num_agents, swarm):
        if p.PLACE_OBJECT:
            if p.FULL_LOCKDOWN:
                for object_loc in object_locs_full_lockdown:
                    self.objects.add_object(file='experiments/covid/images/community_border.png',
                                        pos=object_loc,
                                        scale=object_scale_full_lockdown,
                                        type='obstacle')
                self.objects.add_object(file='experiments/covid/images/community_border.png',
                                    pos=self.in_center.get('obstacle')[0],
                                    scale=self.in_center.get('obstacle')[1],
                                    type='obstacle')
            else:
                object_loc = [p.S_WIDTH / 2., p.S_HEIGHT / 2.5]
                scale = [900, 900]
                filename = 'experiments/covid/images/partial_lockdown.png'

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
                if p.FULL_LOCKDOWN:
                    coordinates = self.coor_inside_object()
                else:
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

    def coor_inside_object(self):
        n_in_each = int(p.N_AGENTS / len(object_locs_full_lockdown))
        def func(e):
            return e.get('agents') < n_in_each
        elements = list(filter(func, self.inside))
        # to randomize agents across all obstacles.
        random.shuffle(elements)
        el = elements[0]

        o_loc, o_scale = el.get('obstacle')
        x_pos = float(random.randrange(o_loc[0] - int(o_scale[0]/3),
                                    o_loc[0] + int(o_scale[0]/3)
                                    ))
        y_pos = float(random.randrange(o_loc[1] - int(o_scale[1]/3),
                                    o_loc[1] + int(o_scale[1]/3)
                                    ))
        # max n of agents inside an obstacle
        el['agents'] += 1
        return x_pos, y_pos

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
