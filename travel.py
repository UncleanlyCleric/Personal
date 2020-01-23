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
d = au * 149597870700
         149597870691


traveltime = 2 * math.sqrt(k / a * math.floor((d / 2 * k + 1) ** 2) - 1)
days = traveltime // 86400


tsc = travel time from the ship's point of reference
acosh = inverse hyperbolic cosine

tsc = ((2 * c) / a ) * ( math.acosh * math.round( ( d / (2 * k ) ) + 1 ) )
shipdays = tsc // 86400


vamx = Maximum velocty at the halfway point (flip and decelerate)
vmax = c / math.sqrt(1 + (k / a * ((T / 2) ** 2)))

One thing I'm not going to worry about is fuel.  The assumption is fuel/weight
problem has been solved by this point.  (Ex:  Epstien drive in The Expanse)

'''
import sys
import math


def safe_input():
    '''
    This will be for handling keyboard exceptions
    '''
    return None


def travel_time(a, d, k):
    '''
    Meat and potatoes of the back of the hand math to calculate travel time
    '''
    traveltime = 2 * math.sqrt(k / a * math.floor((d / 2 * k + 1) ** 2) - 1)
    return traveltime


def ship_time(a, c, d, k):
    '''
    This is the same as above, only for ship time
    '''
    shipa = math.floor((d / 2 * k) + 1)
    shiptime = shipa * math.acosh(2 * c / a) ** -1
    return shiptime


def output(a, d):
    '''
    Collect and format our output
    '''
    c = 2.99792458 * (10 ** 8)
    k = float(c ** 2 / a)

    traveltime = travel_time(a, d, k) / 86400
    shiptime = ship_time(a, c, d, k) / 86400
    vmax = c / math.sqrt(1 + k / (a * ((traveltime / 2)) ** 2)) / 1000

    print(f'\nThis trip will take {str(traveltime)[:5]} days, {str(shiptime)[:5]}\
days of ship time. \
\nThe maximum velocity reached will be {vmax} kph.  \
\n\nClocks will be synced once docked.\n')


def custom():
    try:
        a = float(input('Enter the travel speed in Gs (ex: 1, or .33): '))
        au = float(input('Enter the travel distance in AUs (ex: .5 or 1): '))
        d = au * 149597870691
        output(a, d)
    except (KeyboardInterrupt, EOFError, ValueError):
        safe_input()

def route():
    pass


def goodbye():
    '''
    Gracefully exits
    '''
    print('Goodbye!')
    sys.exit()


def main():
    '''
    User input section
    '''
    prompt = '\n'.join(('Space travel time calculator 0.1.0',
                        '',
                        'Please choose from below options:',
                        'route - If you want standard point to point flights',
                        'custom - If you want to set a non-standard course',
                        'list - If you would like to see standard destinations',
                        'quit   - Exit',
                        '>>> '))

    valid_input = ('route', '1', 'custom', '2', 'list', '3', 'quit', '4')

    menu_choice = {'route': route,
                   '1': route,
                   'custom': custom,
                   '2': custom,
                   'list': list,
                   '3': list,
                   'quit': goodbye,
                   '4': goodbye
                   }

    while True:
        try:
            response = input(prompt)
        except (KeyboardInterrupt, EOFError):
            continue
        if response not in valid_input:
            print('\nERROR: Invalid option')
            continue
        menu_choice[response]()

if __name__ == '__main__':
    main()
