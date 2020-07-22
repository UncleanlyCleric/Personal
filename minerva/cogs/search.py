#!/usr/bin/env python3.7
'''
Various web search utilities will go here.
'''
# pylint: disable = C0103, W0612, W0703
import os
import re
import aiohttp
from googlesearch import search
from discord.ext import commands

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

class Search(commands.Cog):
    '''
    This is the old category script. Will be placed in a DB eventually
    '''
    def __init__(self, bot):
        '''
        Initialize
        '''
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def _youtube_results(self, query: str):
        try:
            headers = {"user-agent": "Minerva/1.0"}
            async with self.session.get("https://www.youtube.com/results",
                                        params={"search_query": query},
                                        headers=headers) as r:
                result = await r.text()
            yt_find = re.findall(r"{\"videoId\":\"(.{11})", result)
            url_list = []
            for track in yt_find:
                url = f"https://www.youtube.com/watch?v={track}"
                if url not in url_list:
                    url_list.append(url)
        except Exception as e:
            url_list = [f"Something went terribly wrong! [{e}]"]

        return url_list

    @commands.command(
        name='youtube',
        description='A basic YouTube search that gives first hit as result',
        aliases=['yt'])
    async def youtube(self, ctx, *, query: str):
        '''
        Search on Youtube.
        '''
        result = await self._youtube_results(query)
        if result:
            await ctx.send(result[0])
        else:
            await ctx.send("Nothing found. Try again later.")


    @commands.command(
        name='google',
        description='A basic Google search that gives first hit as result',
        aliases=['g'])

    async def google(self, ctx, *, searchquery: str):
        '''
        Googles search or images
        '''
        try:
            for j in search(searchquery, tld="com", num=1, stop=1, pause=2):
                await ctx.send(j)
        except Exception as e:
            await ctx.send('Invalid')

def setup(bot):
    '''
    Sending the cog to the main bot
    '''
    bot.add_cog(Search(bot))
