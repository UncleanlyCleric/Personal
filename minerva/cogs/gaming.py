#!/usr/bin/env python3.7
# pylint: disable = W0703
'''
This will be the tabletop gaming cog.  Roll is the only command initiated at
this time.
'''
import random
import typing
from discord.ext import commands

class Roll(commands.Cog):
    '''
    This is a basic dice roller.  Eventually I think it would be fun to use
    discord as a tabletop platform. There's already bots that do this, but
    this is excellent practice for me.
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='roll',
        description='Dice roller, NdN +/- modifier (optional)',
        aliases=['r'])

    async def roll(self, ctx, dice: str, modifier: typing.Optional[int] = 0):
        '''
        Rolls a dice in NdN format.
        '''
        total = 0

        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN +N!')
            return

        result = ' + '.join(str(random.randint(1, limit)) for r in range(rolls))

        for i in result.split(' + '):
            i = int(i)
            total += i

        finaltotal = 'You rolled {} on dice, + {}, for a total of \
{}!'.format(result, modifier, (int(total) + modifier))

        await ctx.send(finaltotal)

def setup(bot):
    '''
    Sending the cog to the main bot
    '''
    bot.add_cog(Roll(bot))
