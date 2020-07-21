#!/usr/bin/env python3.7
'''
A weather script.  Uses OWM to grab weather data.
'''
# pylint: disable = C0103, W0612, W0703

import os
import typing
import pyowm
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
OWM = os.getenv('OWM_TOKEN')

class Weather(commands.Cog):
    '''
    This is where the weather is pulled from the OWM API and formatted for
    Discord embed.
    '''
    @commands.command(
        name='!weather',
        description='Weather information. Eg. Seattle, WA or Moscow, RU',
        aliases=['w']
        )

    async def weather(self, ctx, *, city: typing.Optional[str] = 'Seattle',
                      country: typing.Optional[str] = 'US'):
        '''
        Very basic weather API calls
        '''
        if city is None:
            await ctx.send('You must enter a city and two letter country code')

        owm = pyowm.OWM(OWM)
        await ctx.trigger_typing()
        mgr = owm.weather_manager()
        obs = mgr.weather_at_place(city+','+country)
        w = obs.weather
        temp = w.temperature(unit='fahrenheit')['temp']
        status = w.status
        statusAD = w.detailed_status
        pfp = w.weather_icon_url()
        humid = w.humidity
        wind = w.wind()['speed']


        embed = discord.Embed(title=':white_sun_cloud: Weather Check ',
                              description=f'Details about the weather in {city} \
{country}',
                              color=0xff9f9f)
        embed.add_field(name='Status', value=f'{status}, {statusAD}', inline=True)
        embed.add_field(name='Temperature', value=f'{temp}F', inline=True)
        embed.add_field(name='Humidity', value=f'{humid}%', inline=True)
        embed.add_field(name='Wind speed', value=f'{wind}m/s', inline=True)

        embed.set_thumbnail(url=pfp)
        embed.set_footer(text=f'Requested by {ctx.message.author}',
                         icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    '''
    Sending the cog to the main bot
    '''
    bot.add_cog(Weather(bot))
