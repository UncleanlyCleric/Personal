import asyncio
import discord
import tweepy

from discord.ext import commands
from tweepy import Stream
from tweepy.streaming import StreamListener

class EpicListener(tweepy.StreamListener):
    def __init__(self, discord, loop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.discord = discord # this is just a function which sends a message to a channel
        self.loop = loop # this is the loop of discord client

    def on_status(self, status):
        self.send_message(status._json)

    def send_message(self, msg):
        # Submit the coroutine to a given loop
        future = asyncio.run_coroutine_threadsafe(self.discord(msg), self.loop)
        # Wait for the result with an optional timeout argument
        future.result()

DISCORD_TOKEN = 'dtoken'
TWITTER_CONSUMER_KEY = 'ckey'
TWITTER_CONSUMER_SECRET = 'csecret'
TWITTER_ACCESS_TOKEN = 'atoken'
TWITTER_ACCESS_SECRET = 'asecret'

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        myStream = tweepy.Stream(
                    auth=api.auth, listener=EpicListener(discord=self.sendtwitter, loop=asyncio.get_event_loop())
                )
        myStream.filter(follow=['mohitwr'], is_async=True)
        print(myStream)
