import sys
from importlib import resources

import discord
from discord.ext import commands
import urpy
from urpy import utils, lcl, MyBot
import cog_presentation.info
from cog_presentation import strings
from cog_presentation import settings
from urpy.utils import error_log

_ = lcl

#UR_Bot © 2020 by "Association Union des Rôlistes & co" is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA)
#To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
#Ask a derogation at Contact.unionrolistes@gmail.com

class Presentation(urpy.MyCog):
    """
    This cog serves the purpose of automating the making of presentations on the guild.
    """

    def __init__(self, bot: MyBot):
        super().__init__(bot, 'cog_presentation')

        global _
        _ = lambda s: bot.localization.gettext(s, self.domain)
        bot.localization.add_translation(self.domain, ['fr'])

    @commands.Cog.listener()
    async def on_ready(self):  # TODO move to MyCog
        utils.log("\t| Presentation started.")

    @commands.command(brief=strings.jdr_brief, help=strings.jdr_help)
    async def prez(self, ctx):
        """
        Envoie un lien pour se présenter
        """
        base_ctx = ctx
        ctx = urpy.MyContext(ctx)
        # TODO fix contexts shenanigans
        # checks that $cal is called in the right place
        if isinstance(ctx.channel, discord.DMChannel):
            await base_ctx.send(_(strings.on_prez_dm_channel))
        elif isinstance(ctx.channel, discord.TextChannel):
            anncmnt_channel = discord.utils.get(ctx.guild.channels, name=settings.announcement_channel)
            if not anncmnt_channel:
                await ctx.send(_(strings.on_prez_channel_not_found.format(channel=settings.announcement_channel)))
            else:
                try:
                    webhooks = await anncmnt_channel.webhooks()
                    webhook: discord.Webhook = webhooks[0]
                except discord.errors.Forbidden:
                    error_log("Impossible d'obtenir les webhooks.",  # TODO change to english
                              "Le bot nécessite la permission de gérer les webhooks")
                    await ctx.author.send(strings.on_permission_error)
                except IndexError:
                    await ctx.send(_(strings.on_prez_webhook_not_found.format(channel=settings.announcement_channel)))
                else:
                    await ctx.send(_(strings.on_prez))
                    await ctx.author.send(
                        strings.on_prez_link.format(link=f"http://presentation.unionrolistes.fr?webhook={webhook.url}"))

    @staticmethod
    def get_credits():
        return resources.read_text(cog_presentation.info, 'credits.txt')

    @staticmethod
    def get_version():
        return resources.read_text(cog_presentation.info, 'version.txt')

    @staticmethod
    def get_name():
        return resources.read_text(cog_presentation.info, 'name.txt')
