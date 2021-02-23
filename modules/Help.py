import discord
import random

from discord.ext import commands


colors = {
  'DEFAULT': 0x000000,
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'GREY': 0x95A5A6,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_GREY': 0x979C9F,
  'DARKER_GREY': 0x7F8C8D,
  'LIGHT_GREY': 0xBCC0C0,
  'DARK_NAVY': 0x2C3E50,
  'BLURPLE': 0x7289DA,
  'GREYPLE': 0x99AAB5,
  'DARK_BUT_NOT_BLACK': 0x2C2F33,
  'NOT_QUITE_BLACK': 0x23272A
}

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name='help', description='The help command!', aliases=['commands', 'command'], usage='<cogname>')
    async def help_command(self, ctx, cog="all"):

        color_list = [c for c in colors.values()]
        help_embed = discord.Embed(
            title='Help',
            color=random.choice(color_list)
        )
        help_embed.set_thumbnail(url=self.bot.user.avatar_url)
        help_embed.set_footer(
            text=f'Requested by {ctx.message.author.name}',
            icon_url=self.bot.user.avatar_url
        )

        cogs = [c for c in self.bot.cogs.keys()]
        cogs_to_remove = []
        for each_cog in cogs_to_remove:
            cogs.pop(cogs.index(each_cog))

        if cog == 'all':

            cogs.append(cogs.pop(cogs.index("Help"))) 

            for cog in cogs:

                cog_commands = [c for c in self.bot.get_cog(cog).walk_commands()]
                commands_list = ''

                for comm in cog_commands:
                    if len(comm.qualified_name.split()) > 1:
                        cog_commands.pop(0)
                        break

                for comm in cog_commands:
                    commands_list += f'**{comm.qualified_name}** - *{comm.description}*\n'

                help_embed.add_field(
                    name=cog,
                    value=commands_list,
                    inline=False
                )

        else:

            lower_cogs = [c.lower() for c in cogs]

            if cog.lower() in lower_cogs:

                commands_list = [c for c in self.bot.get_cog( cogs[ lower_cogs.index(cog.lower()) ] ).walk_commands()]
                help_text=''

                for command in commands_list:
                    help_text += f'```{command.qualified_name}```\n' \
                        f'**{command.description}**\n\n'

                    if len(command.aliases) > 0:
                        help_text += f'**Aliases :** `{"`, `".join(command.aliases)}`\n\n'
                    else:
                        help_text += ''

                    prefix_list = await self.bot.get_prefix(ctx.message)
                    other_prefixes = prefix_list[2:]
                    usage_list = []

                    usage_list.append(f'Format: `@{self.bot.user.name}#{self.bot.user.discriminator}' \
                        f' {command.qualified_name} {command.usage if command.usage is not None else ""}`')

                    if other_prefixes:
                        for prefix in other_prefixes:
                            usage_list.append(f'`{prefix}{command.qualified_name} {command.usage if command.usage is not None else ""}`')

                    help_text += ',\n'.join(usage_list) + '\n\n'
                    
                help_embed.description = help_text
            else:

                await ctx.send('Invalid cog specified.\nUse `help` command to list all cogs.')
                return

        await ctx.send(embed=help_embed)


def setup(bot):
    bot.add_cog(Help(bot))
