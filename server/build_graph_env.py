"""
Environment for Spot indoor
"""
from collections import defaultdict
import numpy as np
#import matplotlib.pyplot as plt


def build_graph_env(dict):
    cube_env = {}  # define settings as a dictionary
    cube_env['num_floor'] = 1
    all_ids =[]
    name_to_id={}
    env={}
    # Define a map 
    room_to_poses = {}
    for i in range(len(dict)):
        room_to_poses[i]=[i]
    cube_env['num_room'] = len(dict)
    # map location name to id
    i=0
    for key in dict:
        name_to_id[key]=i
        all_ids.append(i)
        i+=1
    # creating connections between node ID and all IDs
    for i in range(len(dict)):
        env[i]=all_ids   # creating connections between node ID and locaiton name
    cube_env['transition_table']= env
    
    # Compute id to poses, id to room, room to id
    num_id = 0
    id_to_pose = defaultdict()
    loc_to_room = defaultdict()
    room_to_locs = defaultdict()
    for room in range(0, len(dict)):
        num_id_in_room = len(room_to_poses[room])
        for pose_idx, pose in enumerate(room_to_poses[room]):
            id_to_pose[num_id+pose_idx] = pose
            loc_to_room[num_id+pose_idx] = room

        room_to_locs[room] = list(range(num_id, num_id + num_id_in_room))
        num_id += num_id_in_room

    cube_env['id_to_gps'] = id_to_pose
    cube_env['loc_to_room'] = loc_to_room
    cube_env['room_to_locs'] = room_to_locs
    cube_env['num_id'] = num_id

    # Extract room numbers and locations in each floor
    cube_env['floor_to_rooms'] = {0: list(range(0, cube_env['num_room']))}  # {floor: the list of rooms on the floor}
    cube_env['floor_to_locs'] = {0: list(range(0, cube_env['num_id']))}  # {floor: the list of locs}
    cube_env['room_to_floor'] = dict.fromkeys(range(0, cube_env['num_room']), 0)  # {room: the corresponding floor}
    cube_env['loc_to_floor']= dict.fromkeys(range(0, cube_env['num_id']), 0)  # {loc: the corresponding floor}

    # Compute the transition table
    cube_env['transition_table_l0'] = cube_env['transition_table']
    cube_env['num_action'] = max([len(next_states) for next_states in cube_env['transition_table_l0'].values()])

    # # Define attributes
    # cube_env['attribute_color'] = {1: 'red', 6: 'blue', 12: 'blue', 18: 'blue',
    #                                8: 'yellow', 10: 'purple', 15: 'green'}

    # Define Actions
    cube_env['L1ACTIONS'] = ["toRoom%d" % ii for ii in range(0, cube_env['num_room'])]

    # Save
    # np.save('cube_env_1.npy', cube_env)
    return cube_env


if __name__ == '__main__':
    env = build_graph_env()
    print("done")


