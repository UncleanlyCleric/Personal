#!/usr/bin/env python3.7
# pylint: disable = W0612, C0103, W0703
'''
Bot setup
'''
import os
import sys
import datetime
import asyncio
import logging
import signal
import sqlite3
import functools
import traceback

from concurrent.futures import CancelledError
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
OWNER = os.getenv('OWNER_ID')


timenow = datetime.datetime.now()
formatted_timenow = str(timenow.strftime('%d-%m-%Y %H:%M'))
db = sqlite3.connect('quotes.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS quotes(hash TEXT primary key, user \
TEXT, message TEXT, date_added TEXT)')
print('Loaded quotes database '+formatted_timenow)
db.commit()

def get_prefix(client, message):
    '''
    Setting the prefix for the commands
    '''
    prefixes = ['!']

    # Allow users to @mention the bot to trigger commands as well.
    return commands.when_mentioned_or(*prefixes)(client, message)

bot = commands.Bot(
    command_prefix=get_prefix,
    description='Bot rewrite in more modern form',
    owner_id=OWNER,
    case_insensitive=False
)

bot.remove_command('help')

cogs = [
    'cogs.embed',
    'cogs.gaming',
    'cogs.weather',
    'cogs.quotes',
    'cogs.info',
    'cogs.search',
    'cogs.help',
    'cogs.twitter'
    ]

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
    @bot.event
    async def on_ready():
        '''
        Successful Discord connect notification (in console)
        '''
        print(f'Logged in as {bot.user.name} - {bot.user.id}')
        for cog in cogs:
            try:
                bot.load_extension(cog)
            except Exception as e:
                print(f'Failed to load extension {cog}.', file=sys.stderr)
                traceback.print_exc()

    @bot.event
    async def on_command_error(ctx, error):
        '''
        Unknown command handler
        '''
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            await ctx.send('That command was not found.')

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

    bot.run(TOKEN, bot=True)
    logging.getLogger().setLevel(logging.INFO)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(supervisor(loop))
    loop.add_signal_handler(signal.SIGHUP, functools.partial(shutdown, loop))
    loop.add_signal_handler(signal.SIGTERM, functools.partial(shutdown, loop))
    supervisor(loop)

if __name__ == '__main__':
    main()
