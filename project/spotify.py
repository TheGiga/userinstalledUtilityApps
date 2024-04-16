import asyncspotify
import os

auth = asyncspotify.ClientCredentialsFlow(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
)

SpotifyClient = asyncspotify.Client(auth)


async def setup_spotify_client():
    # authorizing spotify client
    await SpotifyClient.authorize()
