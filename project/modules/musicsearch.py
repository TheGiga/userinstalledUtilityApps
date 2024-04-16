import discord
from project import ThisBot, ThisBotContext, SpotifyClient


async def track_searcher(ctx: discord.AutocompleteContext):
    return [
        discord.OptionChoice(name=track.name, value=track.link)
        for track in await SpotifyClient.search_tracks(q=ctx.value.lower(), limit=5)
    ] if len(ctx.value) > 0 else []


class Messages(discord.Cog):
    def __init__(self, bot: ThisBot):
        self.bot: ThisBot = bot

    music = discord.SlashCommandGroup(
        name="music", description="Spotify music related commands.",
        contexts={
            discord.InteractionContextType.bot_dm, discord.InteractionContextType.private_channel,
            discord.InteractionContextType.guild
        },
        integration_types={discord.IntegrationType.user_install},
    )

    @music.command(
        contexts={
            discord.InteractionContextType.bot_dm, discord.InteractionContextType.private_channel,
            discord.InteractionContextType.guild
        },
        integration_types={discord.IntegrationType.user_install},
        name='search'
    )
    async def music_search(self, ctx: ThisBotContext, track: discord.Option(name="query", autocomplete=track_searcher)):
        await ctx.respond(track)


def setup(bot):
    bot.add_cog(Messages(bot=bot))
