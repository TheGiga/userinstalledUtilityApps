import discord
from asyncspotify import BadRequest
from project import ThisBot, ThisBotContext, SpotifyClient


async def track_searcher(ctx: discord.AutocompleteContext):
    try:
        return [
            discord.OptionChoice(
                name=", ".join(map(lambda a: a.name, track.artists)) + f" - {track.name}",
                value=track.id
            ) for track in await SpotifyClient.search_tracks(q=ctx.value.lower(), limit=5)
        ] if len(ctx.value) > 0 else []
    except discord.HTTPException:
        pass


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
    async def music_search(
            self, ctx: ThisBotContext, track_id: discord.Option(name="query", autocomplete=track_searcher),
            send_spotify_embed: discord.Option(
                bool, description="if True, bot will send default discord spotify embed, instead of custom one"
            ) = False
    ):
        try:
            track = await SpotifyClient.get_track(track_id)
        except BadRequest:
            return await ctx.respond(":x: Invalid ID. Most likely, you didn't actually select a track.", ephemeral=True)

        if send_spotify_embed:
            return await ctx.respond(track.link)

        embed = discord.Embed(
            colour=discord.Color.embed_background(),
            title=", ".join(map(lambda a: a.name, track.artists)) + f" - {track.name}"
        )

        if hasattr(track.album, "images"):
            embed.set_thumbnail(url=track.album.images[0])

        m, s = divmod(track.duration.total_seconds(), 60)

        embed.add_field(name='⌛ Duration', value=f"{round(m)}:{round(s):02d}")
        embed.add_field(name='🔞 Explicit', value='Yes' if track.explicit else 'No')

        embed.description = f"[> Click to open in Spotify <]({track.link})"

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Messages(bot=bot))
