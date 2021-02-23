import re
import json
import datetime
from io import BytesIO
from urllib.request import urlopen

import pytz
import discord
import requests
from discord.ext import commands
from colorthief import ColorThief


class Game(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='gametime', aliases=['gt'], description='Get Time for game daily and weekly reset')
    @commands.guild_only()
    async def get_game(self, ctx, *, game=None):

        with open("config.json", "r") as infile:
            config = json.load(infile)

        with open("extradata.json", "r") as infile:
            extradata = json.load(infile)

        r = requests.get("https://raw.githubusercontent.com/cicerakes/Game-Time-Master/master/script.js").content.decode()
        gamedata = r.split("// Initialise list of filtered/hidden games using gameData.")[0].split("var gameData = ")[1].rsplit("]")[0] + "]"
        fixed_data = (re.sub("\\n(\w+): \"", r'"\1":"', gamedata.replace("\t", ""))).replace("utcDailyReset", '"utcDailyReset"')
        game_list = json.loads(fixed_data)

        to_list = []
        if game:
            for each_game in game_list:
                if game.lower() in each_game["game"].lower():
                    to_list.append(each_game)
        else:
            favs = config['fav']
            for each_fav in favs:
                if isinstance(each_fav, list):
                    server = each_fav[1]
                    each_fav = each_fav[0]
                else:
                    server = None
                for each_game in game_list:
                    if each_fav in each_game["game"]:
                        if server is None or server == each_game["server"]:
                            to_list.append(each_game)
                            break

        for each_game in to_list:

            daily_time = each_game["dailyReset"]
            server = each_game["server"]
            server_timezone = each_game["timezone"]
            extra_gamedata = extradata[each_game['game']]
            if isinstance(extra_gamedata["name"], str):
                icon_url = "https://raw.githubusercontent.com/cicerakes/Game-Time-Master/master/game-icons/" + extra_gamedata["name"]
            else:
                icon_url = "https://raw.githubusercontent.com/cicerakes/Game-Time-Master/master/game-icons/" + extra_gamedata["name"][server]
            try:
                weekday = extra_gamedata["Day"]
            except KeyError:
                weekday = None

            daily_hour, daily_min = daily_time.split(":")
            daily_hour = int(daily_hour)
            daily_min = int(daily_min)
            current_time = datetime.datetime.now(pytz.timezone(server_timezone))

            if daily_hour >= current_time.hour:
                if daily_min < current_time.minute:
                    time_diff = datetime.timedelta(hours=daily_hour, minutes=daily_min) - datetime.timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second)
                else:
                    time_diff = datetime.timedelta(days=1) - datetime.timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second) + datetime.timedelta(hours=daily_hour, minutes=daily_min)
            else:
                time_diff = datetime.timedelta(days=1) - datetime.timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second) + datetime.timedelta(hours=daily_hour, minutes=daily_min)

            hours, minutes, seconds = time_diff.__str__().split(":")
            daily_remaining = f"{hours} hours {minutes} minutes"

            if weekday or weekday == 0:
                if weekday > current_time.weekday():
                    day_diff = weekday - current_time.weekday()
                else:
                    if daily_hour >= current_time.hour:
                        if daily_min < current_time.minute:
                            day_diff = 6 + weekday - current_time.weekday()
                        else:
                            day_diff = weekday - current_time.weekday()
                    else:
                        day_diff = 6 + weekday - current_time.weekday()

                weekly_remaining = f"{day_diff} days {daily_remaining}"
            else:
                weekly_remaining = f"Unknown"

            fd = urlopen(icon_url)
            f = BytesIO(fd.read())
            color_thief = ColorThief(f)
            rgb = color_thief.get_color(quality=1)
            color_code = '0x%02x%02x%02x' % rgb

            game_embed = (
                discord.Embed(
                    color=discord.Color(int(color_code, 16)),
                    timestamp=current_time,
                    title=f"{each_game['game']} ({server})"
                )
                .set_thumbnail(url=icon_url)
                .add_field(name="Time Until Daily Reset", value=daily_remaining, inline=False)
                .add_field(name="Time Until Weekly Reset", value=weekly_remaining, inline=False)
            )

            await ctx.send(embed=game_embed, delete_after=20)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Game(bot))
