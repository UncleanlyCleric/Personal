#!/usr/bin/env python3.7
'''
Bot ping delay tool.  Checks to see what the latency between Discord and the
bot actually is.
'''

from datetime import datetime as d
from discord.ext import commands


# New - The Cog class must extend the commands.Cog class
class Ping(commands.Cog):
    '''
    Running a ping command to check bot delay.
    '''
    def __init__(self, bot):
        self.bot = bot

    # Define a new command
    @commands.command(
        name='ping',
        description='The ping command, tests bot latency',
        aliases=['p'])

    async def ping_command(self, ctx):
        '''
        This is where we set up the latency ping
        '''
        start = d.timestamp(d.now())
        msg = await ctx.send(content='Pinging')

        await msg.edit(content=f'Pong!\nOne message round-trip took \
{( d.timestamp( d.now() ) - start ) * 1000 }ms.')
        return


def setup(bot):
    '''
    Sending the cog to the main bot
    '''
    bot.add_cog(Ping(bot))
