#!/usr/bin/env python3
# pylint: disable = C0103,R0912, R1702, W0105
'''This custom help command is a perfect replacement for the default one on any
Discord Bot written in Discord.py! However, you must put 'bot.remove_command('help')'
in your bot, and the command must be in a cog for it to work. Written by
Jared Newsom (AKA Jared M.F.)! - edited by ceron21

paste this into your (mail) bot code after defining your bot:
# LOADING Extentions
bot.remove_command('help')
initial_extensions = [
        'cogs.help' #path is here cogs/help.py
            ]
'''
import discord
from discord.ext import commands


class Help(commands.Cog):
    '''
    Set up the command class
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(add_reactions=True, embed_links=True)
    async def help(self, ctx, *cog):
        '''Gets all cogs and commands of mine.'''
        try:
            if not cog:
                '''Cog listing.  What more?'''
                halp = discord.Embed(title='Cog Listing and Uncatergorized Commands',
                                     description='Use `!help *cog*` to find out more \
about them!\n(BTW, the Cog Name Must Be in Title Case, Just Like this Sentence.)')
                cogs_desc = ''
                for x in self.bot.cogs:
                    cogs_desc += ('{} - {}'.format(x, self.bot.cogs[x].__doc__)+'\n')
                halp.add_field(name='Cogs', value=cogs_desc[0:len(cogs_desc)-1],
                               inline=False)
                cmds_desc = ''
                for y in self.bot.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ('{} - {}'.format(y.name, y.help)+'\n')
                if cmds_desc != '':
                    halp.add_field(name='Uncatergorized Commands',
                                   value=cmds_desc[0:len(cmds_desc) - 1],
                                   inline=False)
                await ctx.message.add_reaction(emoji='✉')
                await ctx.message.author.send('', embed=halp)
            else:
                '''Helps me remind you if you pass too many args.'''
                if len(cog) > 1:
                    halp = discord.Embed(title='Error!', description='That is \
way too many cogs!', color=discord.Color.red())
                    await ctx.message.author.send('', embed=halp)
                else:
                    '''Command listing within a cog.'''
                    found = False
                    for x in self.bot.cogs:
                        for y in cog:
                            if x == y:
                                halp = discord.Embed(title=cog[0]+' Command Listing',
                                                     description=self.bot.cogs[cog[0]].__doc__)
                                for c in self.bot.get_cog(y).get_commands():
                                    if not c.hidden:
                                        halp.add_field(name=c.name, value=c.help, inline=False)
                                found = True
                    if not found:
                        '''Reminds you if that cog doesn't exist.'''
                        halp = discord.Embed(title='Error!', description='How do \
you even use ''+cog[0]+''?', color=discord.Color.red())
                    else:
                        await ctx.message.add_reaction(emoji='✉')
                    await ctx.message.author.send('', embed=halp)
        except:
            await ctx.send('Please send me a direct message for !help.')

def setup(bot):
    '''
    Set up the config for the bot to consume
    '''
    bot.add_cog(Help(bot))
