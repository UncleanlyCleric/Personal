#!/usr/bin/env python3.7
'''
Here we have quotes, and categories.  These will be combined later.
Categories is our old IRC flatfile DB
'''
# pylint: disable = C0103, W0612, W0703

import random
from discord.ext import commands

class Category(commands.Cog):
    '''
    This is the old category script. Will be placed in a DB eventually
    '''
    def __init__(self, bot):
        '''
        Initialize
        '''
        self.bot = bot

    @commands.command(
        name='cat',
        description='Pulls a quote from the catagories.  !cat <catagory>',
        )

    async def cat(self, ctx, *, category: str):
        '''
        The old categories script, modernized.  Currently, reading from files
        is supported.  Adding to files is a WIP.  Once all that works, time to begin
        the big SQLite work.
        '''
        try:
            with open('/home/junya/discord/categories/'+category+'.txt') as f:
                lines = f.readlines()
                await ctx.send(random.choice(lines))
        except FileNotFoundError as e:
            await ctx.send('No category found by that name.')

    @commands.command(
        name='addcat',
        description='Pulls a quote from the catagories.  !cat <catagory>',
        aliases=['catadd']
        )

    async def catadd(self, ctx, *, message: str):
        '''
        Some luck, and this won't destroy things as it adds to categories or creates
        new files.
        '''
        strings = str(message)
        temp = strings.split()

        category = temp[0]
        del temp[0]

        message = ' '.join(temp)

        with open('/home/junya/discord/categories/'+category+'.txt', 'a') as f:
            f.write(message+'\n')
            await ctx.send('Added to '+category)

def setup(bot):
    '''
    Sending the cog to the main bot
    '''
    bot.add_cog(Category(bot))

    # bot.add_cog(Random_Quotes(bot), GetQuote(bot))
    # bot.add_cog(CatAdd(bot))
