 #!/usr/bin/env python3
 # pylint: disable = C0103
'''
This is a first pass at writing a solar system transit time program.  The idea
will be to compensate for orbits, varying speeds of constant thrust and time
under float, to give a semi-accurate model of solar space travel.

Maybe I'll run this game, maybe I won't.


traveltime = travel time
k = c ** 2 / a
c = 2.99792458 * 10 ** 8 meters per sec (speed of light)
a = acceleration / deceleration
au = distance in AU
d = au * (1.495978707 * 10 ** 11)


traveltime = 2 * math.sqrt(k / a * (d // 2 * k + 1) - 1)
days = traveltime / 86400


tsc = travel time from the ship's point of reference
acosh = inverse hyperbolic cosine

tsc = ((2 * c) / a ) * ( math.acosh * math.round( ( d / (2 * k ) ) + 1 ) )
shipdays = tsc / 86400


vamx = Maximum velocty at the halfway point (flip and decelerate)
vmax = c / math.sqrt(1 + (k / a * ((T / 2) ** 2)))

One thing I'm not going to worry about is fuel.  The assumption is fuel/weight
problem has been solved by this point.  (Ex:  Epstien drive in The Expanse)

'''
import math
import numpy as np


def travel_time(a, d, k):
    '''
    Meat and potatoes of the back of the hand math to calculate travel time
    '''
    traveltime = 2 * math.sqrt(k / a * (d // 2 * k + 1) - 1)
    return traveltime


def ship_time(a, c, d, k):
    '''
    This is the same as above, only for ship time
    '''
    shiptime = np.arccosh(math.ceil((d / (2 * k))+ 1) * ((2 * c) / a))
    return shiptime


def output(a, d):
    # a = 1
    c = 2.99792458 * (10 ** 8)
    # d = .5 * (1.495978707 * 10 ** 11)
    k = c ** 2 / a

    shiptime = ship_time(a, c, d, k)
    traveltime = travel_time(a, d, k)
    vmax = c / math.sqrt(1 + (k / a * ((traveltime / 2) ** 2)))

    print(f'This trip will take {traveltime} days, {shiptime} days of ship time.\
          The maximum velocity reached will be {vmax}.  Clocks will resync once \
          docked')


def menu():
    prompt = '\n'.join(('Space travel time calculator 0.1.0',
                        '',
                        'Please choose from below options:',
                        'route - If you want standard point to point flights',
                        'custom - If you want to set a non-standard course',
                        'list - If you would like to see standard destinations',
                        'quit   - Exit',
                        '>>> '))
