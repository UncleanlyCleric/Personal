#!/usr/bin/env python3.7
#pylint: disable = C0103, W0631, W0703, W0612

'''
Recoding both of my old IRC bots into one, and moving to Discord. This is not
the best code.  It's mostly for me to practice.

J. Miller
'''

import asyncio
import functools
import os
import sys
import signal
import logging
import random
import sqlite3
import datetime
import typing

from concurrent.futures import CancelledError
# import whois as who
import requests

from dotenv import load_dotenv

import pyowm
from googlesearch import search
import discord
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

'''
check if database is made and load it
'''
db = sqlite3.connect('quotes.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS quotes(hash TEXT primary key, user \
TEXT, message TEXT, date_added TEXT)')
print('Loaded quotes database')
db.commit()


'''
Setting up the base bot
'''

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    '''
    Letting me know she's on line
    '''
    print(
        f'{bot.user.name} is connected.'
    )

@bot.command(pass_context=True, name='ping', description='A basic ping command')
async def ping(ctx):
    '''
    A simple test for the bot
    '''
    start = datetime.datetime.timestamp(datetime.datetime.now())
    msg = await ctx.send(content='Pinging')
    await msg.edit(content=f'Pong!\nOne message round-trip took\
 {( datetime.datetime.timestamp( datetime.datetime.now() ) - start ) * 1000 }ms.')
    return
    # await ctx.send('pong')


@bot.event
async def on_member_join(member):
    '''
    New member welcome
    '''
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, welcome to Sincerely, Not Serious! I'm Minerva!\n"
        f'just-some-bullshit is our main chat\n'
        f'sportsball is for all your sports chatter\n'
        f'uspol is the politics quarantine zone\n'
        f'uspol-newsfeed is a birdsite feed of various news orgs\n'
        f'nmd is for no music discussion, which is iron(maiden)y\n'
        f'no-mans-high is the current name of the gaming channel\n'
        f'Please enjoy your stay!'
    )

'''
Here are the bots commands
'''

@bot.command(name='roll', help='Simulates rolling dice.')
async def roll(ctx, dice: str, modifier: typing.Optional[int] = 0):
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


'''
The dreaded quotes script
'''
@bot.command()
async def quotehelp(ctx):
    '''
    Help files
    '''
    embed = discord.Embed(name='help')
    embed.set_author(name='Quotebot commands:')
    embed.add_field(name='To quote:', value='!quote @[user] [message]',
                    inline=False)
    embed.add_field(name='To display', value='!getquote @[user]', inline=False)
    embed.add_field(name='Random quote from a random user',
                    value='!random_quotes', inline=False)
    await ctx.send(embed=embed)

#print random quote
@bot.command()
async def random_quotes(ctx):
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


@bot.command()
async def quote(ctx, *, message: str):
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


@bot.command()
async def getquote(ctx, message: str):
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

@bot.command()
async def weather(ctx, *, city: typing.Optional[str] = 'Seattle',
                  country: typing.Optional[str] = 'US'):
    '''
    Very basic weather API calls
    '''
    if city is None:
        await ctx.send('You must enter a city and two letter country code')

    owm = pyowm.OWM('f1244682f8d9b4dd7b9f5ec4ee83c8d4')
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
    await ctx.send(embed=embed) # Send the data back
'''
End quote scripting
'''

@bot.command()
async def commandlist(ctx):
    '''
    command list
    '''

    embed = discord.Embed(name='Command Help')
    embed.set_author(name='Minerva commands:')
    embed.add_field(name='!quote(!)', value='a work in progress quote DB',
                    inline=False)
    embed.add_field(name='!cat(!catadd) <category>', value='The old IRC category\
 files',
                    inline=False)
    embed.add_field(name='!weather <city>, <state/country>', value='Weather \
anywhere',
                    inline=False)
    embed.add_field(name='!roll <NdN +/- modifier (if wanted)>',
                    value='A diceroller', inline=False)
    embed.add_field(name='!info', value='Server statistics',
                    inline=False)
    embed.add_field(name='!zoom', value='Prints a link to the Blake White \
Memorial Zoom Channel',
                    inline=False)
    embed.add_field(name='!google', value='Posts first result from Google',
                    inline=False)
    embed.add_field(name='!youtube', value='Basic YouTube Search',
                    inline=False)
    await ctx.author.send(embed=embed)

@bot.command()
async def zoom(ctx):
    '''
    Link to our zoom
    '''
    await ctx.send(
        'https://us04web.zoom.us/j/3025651220?pwd=K0xRc0FwQStLNnlBT2VWNlhJZm16Zz09'
    )

@bot.command()
async def info(ctx):
    '''
    Grabs guild information from Discord and displays
    '''
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Waste v3.0",
                          timestamp=datetime.datetime.utcnow(),
                          color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")

    await ctx.send(embed=embed)

@bot.command(helpinfo='Searches for YouTube videos', aliases=['yt'])
async def youtube(ctx, *, query: str):
    '''
    Uses YouTube Data v3 API to search for videos
    '''
    req = requests.get(
        ('https://www.googleapis.com/youtube/v3/search?part=id&maxResults=1'
         '&order=relevance&q={}&relevanceLanguage=en&safeSearch=moderate&type=video'
         '&videoDimension=2d&fields=items%2Fid%2FvideoId&key=')
        .format(query) + os.environ['YOUTUBE_API_KEY'])
    await ctx.send('**Video URL: https://www.youtube.com/watch?v={}**'
                   .format(req.json()['items'][0]['id']['videoId']))


@bot.event
async def on_command_error(ctx, error):
    '''
    Unknown command handler
    '''
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send('That command was not found.')


@bot.command(helpinfo='Searches the web (or images if typed first)',
             aliases=['search', 'g'])
async def google(ctx, *, searchquery: str):
    '''
    Should be a group in the future
    Googles searchquery, or images if you specified that
    '''
    try:
        for j in search(searchquery, tld="com", num=1, stop=1, pause=2):
            await ctx.send(j)
    except Exception as e:
        await ctx.send('Invalid')

@bot.command(helpinfo='The old catagories live again')
async def cat(ctx, *, category: str):
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

@bot.command(helpinfo='Adding to the old category DB', aliases=['addcat'])
async def catadd(ctx, *, message: str):
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


# @bot.command(helpinfo='Network whois')
# async def whois(ctx, *, message: str):
    # '''
    # Network whois lookup
    # '''
    # w = who.whois(message)
    # ctx.send(w)


'''
Below defines the startup and shutdown functions
'''
def shutdown():
    '''
    Setting up a clean shutdown
    '''
    logging.info('received stop signal, cancelling tasks...')
    for task in asyncio.Task.all_tasks():
        task.cancel()
    logging.info('bye, exiting in a minute...')

@asyncio.coroutine
def get(i):
    '''
    Defining a sleep function
    '''
    logging.info('sleep for %d', i)
    yield from asyncio.sleep(i)

@asyncio.coroutine
def pull_stats():
    '''
    Pulling statistics for logging
    '''
    coroutines = [get(i) for i in range(10, 20)]
    status = yield from asyncio.gather(*coroutines)

def supervisor(loop):
    '''
    This supervisor closes the bot down gracefully on reload or restart
    '''
    try:
        while True:
            result = loop.run_until_complete(pull_stats())
    except CancelledError:
        logging.info('CancelledError')
    loop.close()
    sys.exit(1)


def main():
    '''
    Start up order.  Creates the loop that asyncio wants and sets the connection
    to the supervisor
    '''
    bot.run(TOKEN)
    logging.getLogger().setLevel(logging.INFO)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(supervisor(loop))
    loop.add_signal_handler(signal.SIGHUP, functools.partial(shutdown, loop))
    loop.add_signal_handler(signal.SIGTERM, functools.partial(shutdown, loop))
    supervisor(loop)


if __name__ == '__main__':
    main()
