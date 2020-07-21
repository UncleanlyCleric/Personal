#!/usr/bin/env python3.7
# pylint: disable = W0612
'''
Bot setup
'''
import os
import sys
import asyncio
import logging
import signal
import functools

from concurrent.futures import CancelledError
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
OWNER = os.getenv('OWNER_ID')

def get_prefix(client, message):
    '''
    Setting the prefix for the commands
    '''
    prefixes = ['!', '!!']

    if not message.guild:
        prefixes = ['!!']   # Only allow as a prefix when in DMs

    # Allow users to @mention the bot to trigger commands as well.
    return commands.when_mentioned_or(*prefixes)(client, message)

bot = commands.Bot(
    command_prefix=get_prefix,
    description='Bot rewrite in more modern form',
    owner_id=OWNER,
    case_insensitive=False
)

cogs = [
    'cogs.ping',
    'cogs.embed',
    'cogs.gaming',
    'cogs.weather',
    'cogs.quotes',
    'cogs.catagories'
    ]

@bot.event
async def on_ready():
    '''
    Successful Discord connect notification (in console)
    '''
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    bot.remove_command('help')
    for cog in cogs:
        bot.load_extension(cog)
    return

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
    bot.run(TOKEN, bot=True)
    logging.getLogger().setLevel(logging.INFO)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(supervisor(loop))
    loop.add_signal_handler(signal.SIGHUP, functools.partial(shutdown, loop))
    loop.add_signal_handler(signal.SIGTERM, functools.partial(shutdown, loop))
    supervisor(loop)


if __name__ == '__main__':
    main()
