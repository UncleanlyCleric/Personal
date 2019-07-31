#!/usr/bin/env python3
'''
The actions a player can take
'''
# pylint: disable = R0903

from belmont_adventure.player import Player
from belmont_adventure.items import Enemy, Item
import belmont_adventure.world as world

class Action():
    '''
    Using the actions defined in player.py
    '''
    def __init__(self, method, name, hotkey, **kwargs):
        self.method = method
        self.hotkey = hotkey
        self.name = name
        self.kwargs = kwargs

    def __str__(self):
        return '{}: {}'.format(self.hotkey, self.name)


    class MoveNorth(Action):
        '''
        self explanatory
        '''
        def __init__(self):
            super().__init__(method=Player.move_north,
                             name='Move north',
                             hotkey='n')

    class MoveSouth(Action):
        '''
        self explanatory
        '''
        def __init__(self):
            super().__init__(method=Player.move_south,
                             name='Move south',
                             hotkey='s')

    class MoveEast(Action):
        '''
        self explanatory
        '''
        def __init__(self):
            super().__init__(method=Player.move_east,
                             name='Move east',
                             hotkey='e')

    class MoveWest(Action):
        '''
        self explanatory
        '''
        def __init__(self):
            super().__init__(method=Player.move_west,
                             name='Move west',
                             hotkey='w')


    class ViewInventory(Action):
        '''
        Prints the player's inventory
        '''
        def __init__(self):
            super().__init__(method=Player.print_inventory,
                             name='View inventory',
                             hotkey='i')


    class Attack(Action):
        '''
        Hit things with stick
        '''
        def __init__(self, enemy):
            super().__init__(method=Player.attack,
                             name='Attack',
                             hotkey='a',
                             enemy=enemy)


    class MapTile():
        def adjacent_moves(self):
            '''
            Returns all move actions for adjacent tiles.
            '''
            moves = []
            if world.tile_exists(self.x + 1, self.y):
                moves.append(self.MoveEast())
            if world.tile_exists(self.x - 1, self.y):
                moves.append(actions.MoveWest())
            if world.tile_exists(self.x, self.y - 1):
                moves.append(actions.MoveNorth())
            if world.tile_exists(self.x, self.y + 1):
                moves.append(actions.MoveSouth())
            return moves


        def available_actions(self):
            '''
            Returns all of the available actions in this room.
            '''
            moves = self.adjacent_moves()
            moves.append(Player.actions.ViewInventory())

            return moves
