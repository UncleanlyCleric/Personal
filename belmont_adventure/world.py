#!/usr/bin/env python3
'''
Defining the world.  (I feel like a demigod)
'''

'''
https://letstalkdata.com/2014/08/how-to-write-a-text-adventure-in-python-part-2-the-world-space/
'''
# pylint: disable = C0103, C0200, W0603


_world = {}
starting_position = (0, 0)

def load_tiles():
    '''
    Parses a file that describes the world space into the _world object
    '''
    with open('resources/map.txt', 'r') as f:
        rows = f.readlines()
    x_max = len(rows[0].split('\t')) # Assumes all rows contain the same number of tabs
    for y in range(len(rows)):
        cols = rows[y].split('\t')
        for x in range(x_max):
            tile_name = cols[x].replace('\n', '') # Windows users may need to replace '\r\n'
            if tile_name == 'StartingRoom':
                global starting_position
                starting_position = (x, y)
            _world[(x, y)] = None if tile_name == '' else getattr(__import__\
            ('tiles'), tile_name)(x, y)


def tile_exists(x, y):
    '''
    Does the tile exist
    '''
    return _world.get((x, y))
