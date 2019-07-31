#!/usr/bin/env python3
'''
Items list for the Belmonts Bannermen website game.

https://letstalkdata.com/2014/08/how-to-write-a-text-adventure-in-python-part-1-items-and-enemies/

'''
# pylint: disable = R0903, C0103
class Item():
    '''
    This is the base class for the items available in game.
    :items: sword(james), Skeleton key(gwen), golden dickbutt(aiden), sax(talbot),
    (dementor wasp)paul.
    '''
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value


    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\n".format(self.name,
                                                   self.description,
                                                   self.value)


class Goldendickbutt(Item):
    '''
    Creating the Golden Dickbutt, combine the Golden Dickbutt with the skeletonkey
    to exit the dungeon
    '''
    def __init__(self, amt):
        self.amt = amt
        super().__init__(name='Golden Dickbutt',
                         description='A small statue of a penis, that has a \
penis on it\'s butt, stamped with {}. There is an opening under the second \
penis'.format(str(self.amt)),
                         value=self.amt)


class Skeletonkey(Item):
    '''
    The key to exit
    '''
    def __init__(self, amt):
        self.amt = amt
        super().__init__(name='Skeleton Key',
                         description='A Skeleton Key with what appears to be \
a highly detailed sphincter under a set of testicles, stamped with a {}'.format\
                         (str(self.amt)),
                         value=self.amt)


class Weapon(Item):
    '''
    Weapons to attack
    '''
    def __init__(self, name, description, value, damage):
        self.damage = damage
        super().__init__(name, description, value)

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDamage: {}".format(self.name,
                                                             self.description,
                                                             self.value,
                                                             self.damage)


class Dagger(Weapon):
    '''
    Starting weapon, available in room one
    '''
    def __init__(self):
        super().__init__(name='Dagger',
                         description='A small dagger, suitable for stabbing.',
                         value=5,
                         damage=5)


class Sword(Weapon):
    '''
    A stronger weapon to defeat the final boss
    '''
    def __init__(self):
        super().__init__(name='Sword',
                         description='A broad sword inscribed with the latin for\
"Put this in your ass".',
                         value=20,
                         damage=20)


class Sax(Weapon):
    '''
    A stun weapon, used to stun the final boss
    '''
    def __init__(self):
        super().__init__(name='Sax',
                         description='A saxophone stamped with "Toot toot time to die".',
                         value=10,
                         damage=10)


class Dementorwasp(Weapon):
    '''
    The final weapon used to defeat the boss
    '''
    def __init__(self):
        super().__init__(name='Demntor Wasp',
                         description='A very angry wasp, in a jar.  It constantly\
 tries to coerce you into doing cocaine and murder in between singing gregorian \
 chants backwards.',
                         value=666,
                         damage=15)


class Whiskey(Weapon):
    '''
    The weapon of Jesse
    '''
    def __init__(self):
        super().__init__(name='Sax',
                         description='A half empty whiskey bottle labelled "Confidence"',
                         value=10,
                         damage=50)


class Enemy:
    '''
    Wandering Bannermen ahoy!
    '''
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage

    def is_alive(self):
        '''
        Are we alive?
        '''
        return self.hp > 0


class James(Enemy):
    '''
    Why
    '''
    def __init__(self):
        super().__init__(name='James the Red', hp=30, damage=20)


class Paul(Enemy):
    '''
    am
    '''
    def __init__(self):
        super().__init__(name='Paul the Uncanny', hp=30, damage=15)


class Aidan(Enemy):
    '''
    I
    '''
    def __init__(self):
        super().__init__(name='Aidan the British', hp=30, damage=10)


class Gwen(Enemy):
    '''
    docstringing
    '''
    def __init__(self):
        super().__init__(name='Gwenny the Technicolor Shark', hp=30, damage=10)


class Talbot(Enemy):
    '''
    these?
    '''
    def __init__(self):
        super().__init__(name='Talbot, the Talbort', hp=30, damage=15)


class Jesse(Enemy):
    '''
    Faaarrrrrrrrrrrrrrrrrrrrrrrrrrrrt
    '''
    def __init__(self):
        super().__init__(name='Jesse the Far Too Sure of Himself', hp=60, damage=10)
