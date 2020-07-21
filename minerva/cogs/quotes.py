#!/usr/bin/env python3.7
'''
Here we have quotes, and categories.  These will be combined later.
Categories is our old IRC flatfile DB
'''
# pylint: disable = C0103, W0612, W0703

import random
import sqlite3
import datetime
import discord
from discord.ext import commands


db = sqlite3.connect('quotes.db')
cursor = db.cursor()

class Random_Quotes(commands.Cog):
    '''
    The !quote command.  This WILL change once I get the !cat command in a db
    '''
    def __init__(self, bot):
        '''
        Initialize
        '''
        self.bot = bot

    @commands.command(
        name='random_quotes',
        description='Pulls a random quote from the quote DB',
        )

    async def random_quotes(self, ctx):
        '''
        Pulling random things from the db
        '''
        cursor.execute('SELECT user,message,date_added FROM quotes ORDER BY RANDOM() \
    LIMIT 1')
        query = cursor.fetchone()

        #log
        print(query[0]+': \''+query[1]+'\' printed to the screen '+str(query[2]))

        #embeds the output
        style = discord.Embed(name='responding quote', description='- '+str(query[0])+
                              ' '+str(query[2]))
        style.set_author(name=str(query[1]))
        await ctx.send(embed=style)

class Quotes(commands.Cog):
    '''
    Quote additions.
    '''
    def __init__(self, bot):
        '''
        Initialize
        '''
        self.bot = bot

    @commands.command(
        name='quote',
        description='Adds a quote to the db.  Format !quote @user <text>',
        )

    async def quote(self, ctx, *, message: str):
        '''
        Adding quotes to the sqlite3 db
        '''
        #split the message into words
        strings = str(message)
        temp = strings.split()

        #take the username out
        user = temp[0]
        del temp[0]

        #join the message back together
        text = ' '.join(temp)

        if user[1] != '@':
            await ctx.send('Use ```@[user] [message]``` to quote a person')
            return

        uniqueID = hash(user+message)

        #date and time of the message
        time = datetime.datetime.now()
        formatted_time = str(time.strftime('%d-%m-%Y %H:%M'))

        #find if message is in the db already
        cursor.execute('SELECT count(*) FROM quotes WHERE hash = ?', (uniqueID,))
        find = cursor.fetchone()[0]

        if find > 0:
            return

        #insert into database
        cursor.execute('INSERT INTO quotes VALUES(?,?,?,?)', (uniqueID, user, text,
                                                              formatted_time,))
        await ctx.send('Quote successfully added')

        db.commit()

        #number of words in the database
        rows = cursor.execute('SELECT * from quotes')

        #log to terminal
        print(str(len(rows.fetchall()))+'. added - '+str(user)+': \''+str(text)+'\' \
    to database at '+formatted_time)

class GetQuote(commands.Cog):
    '''
    Get quote
    '''
    def __init__(self, bot):
        '''
        Initialize
        '''
        self.bot = bot

    @commands.command(
        name='getquote',
        description='Pulls a random quote for specific user.  !getquote @user',
        )

    async def getquote(self, ctx, message: str):
        '''
        Querying the db for a random quote from the db attached to a user
        '''
        #sanitise name
        user = (message,)

        try:
            #query random quote from user
            cursor.execute('SELECT message,date_added FROM quotes WHERE user=(?) \
ORDER BY RANDOM() LIMIT 1', user)
            query = cursor.fetchone()

            #adds quotes to message
            output = '\''+str(query[0])+'\''

            #log
            print(message+': \''+output+'\' printed to the screen '+str(query[1]))

            #embeds the output to make it pretty
            style = discord.Embed(name='responding quote', description='- '
                                  +message+' '+str(query[1]))
            style.set_author(name=output)
            await ctx.send(embed=style)

        except Exception as e:

            await ctx.send('No quotes of that user found')
            print(e)
        db.commit()

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
        name='!cat',
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

class CatAdd(commands.Cog):
    '''
    This is the old category addition script. Will be placed in a DB eventually
    '''
    def __init__(self, bot):
        '''
        Initialize
        '''
        self.bot = bot

    @commands.command(
        name='!addcat',
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
    bot.add_cog(Quotes(bot))
    bot.add_cog(Category(bot))
    # bot.add_cog(Random_Quotes(bot), GetQuote(bot))
    # bot.add_cog(CatAdd(bot))
