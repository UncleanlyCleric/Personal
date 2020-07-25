#!/usr/bin/env python3
'''
Anything giving info on something goes here.
'''
# pylint: disable = C0103, W0612, W0703
import datetime

import discord
from discord.ext import commands


class Info(commands.Cog):
    '''
    Currently just server info and the Zoom link.
    '''
    def __init__(self, bot):
        '''
        Initialize
        '''
        self.bot = bot

    @commands.command(
        name='zoom',
        description='Link to the Blake White Memorial Videoconference room.',
        )
    async def zoom(self, ctx):
        '''
        Blake White Memorial Videoconference room
        '''
        await ctx.send(
            'https://us04web.zoom.us/j/3025651220?pwd=K0xRc0FwQStLNnlBT2VWNlhJZm16Zz09'
            )


    @commands.command(
        name='info',
        description='Server info.',
        )
    async def info(self, ctx):
        '''
        Displays server information
        '''
        embed = discord.Embed(title=f"{ctx.guild.name}", description="Waste v3.0",
                              timestamp=datetime.datetime.utcnow(),
                              color=discord.Color.blue())
        embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
        embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
        embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
        embed.add_field(name="Server ID", value=f"{ctx.guild.id}")

        await ctx.send(embed=embed)

    @commands.command(
        name='ping',
        description='The ping command, tests bot latency',
        aliases=['p'])

    async def ping_command(self, ctx):
        '''
        Latency test for bot to server.
        '''
        start = datetime.datetime.timestamp(datetime.datetime.now())
        msg = await ctx.send(content='Pinging')

        await msg.edit(content=f'Pong!\nOne message round-trip took \
{( datetime.datetime.timestamp( datetime.datetime.now() ) - start ) * 1000 }ms.')
        return

def setup(bot):
    '''
    Sending the cog to the main bot
    '''
    bot.add_cog(Info(bot))
