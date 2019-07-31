#!/usr/bin/env python3
'''
Creating the tiles for the coordinate plane.
'''
#pylint: disable = C0103, R0903, R0201, W0107
from belmont_adventure.items import Item
from belmont_adventure.items import Enemy
from belmont_adventure.actions import Action
import belmont_adventure.world as world
'''
https://letstalkdata.com/2014/08/how-to-write-a-text-adventure-in-python-part-2-the-world-space/
'''

class MapTile:
    '''
    Defining tileset
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def adjacent_moves(self):
        '''
        Returns all move actions for adjacent tiles.
        '''
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(Action.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(Action.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(Action.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(Action.MoveSouth())
        return moves

    def available_actions(self):
        '''
        Returns all of the available actions in this room.
        '''
        moves = self.adjacent_moves()
        moves.append(Action.ViewInventory())

        return moves


class StartingRoom(MapTile):
    '''
    Defining the very start of the game.
    '''
    def intro_text(self):
        '''
        Here there be intro text
        '''
        return
        '''
        You find yourself if a cave with a flickering torch on the wall.
        You can make out four paths, each equally as dark and foreboding.
        '''


    def modify_player(self, player):
        '''
        Nothing to be done.
        '''
        #Room has no action on player
        pass


class LootRoom(MapTile):
    '''
    This defines a room where an item can be picked up
    '''
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)


    def add_loot(self, player):
        '''
        Get rock.
        '''
        player.inventory.append(self.item)


    def modify_player(self, player):
        '''
        Show inv, see gotten rock.  Yay...
        '''
        self.add_loot(player)


class EnemyRoom(MapTile):
    '''
    This defines a room with an enemy.  Once the enemy is defeated it will
    become a loot room.
    '''
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        '''
        TAKE DAMAGE!!!!
        '''
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print('Enemy does {} damage. You have {} HP remaining.'.format\
            (self.enemy.damage, the_player.hp))


class EmptyCavePath(MapTile):
    '''
    Gasp!  An empty room!
    '''
    def intro_text(self):
        '''
        Self explanatory
        '''
        return
        '''
        Another unremarkable part of the cave. You must forge onwards.
        '''

    def modify_player(self, player):
        '''
        Nothing to be done.
        '''
        #Room has no action on player
        pass


class Aidanroom(EnemyRoom):
    '''
    A room with a Brit!
    '''
    def __init__(self, x, y):
        super().__init__(x, y, Enemy.Aidan())

    def intro_text(self):
        '''
        Self explanatory
        '''
        if self.enemy.is_alive():
            return
            '''
            Aiden britishly leaps at you from his liquor bottle filled corner.
            In his hand flashes a golden statue of a penis.
            '''

        return
        '''
        The corpse of a dead englishman rots on the ground.
        '''


class FindDaggerRoom(LootRoom):
    '''
    A room with a dagger!
    '''
    def __init__(self, x, y):
        super().__init__(x, y, Item.Dagger())

    def intro_text(self):
        '''
        Self explanatory
        '''
        return
        '''
        Your notice something shiny in the corner.
        It's a dagger! You pick it up.
        '''
