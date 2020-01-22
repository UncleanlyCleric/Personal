 #!/usr/bin/env python3
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

tsc = 2 * (c / a) * math.acosh(d // 2 * k + 1) ** (-1)
shipdays = tsc / 86400


vamx = Maximum velocty at the halfway point (flip and decelerate)
vmax = c / math.sqrt(1 + (k / a * ((T / 2) ** 2)))

One thing I'm not going to worry about is fuel.  The assumption is fuel/weight
problem has been solved by this point.  (Ex:  Epstien drive in The Expanse)

'''
import math
