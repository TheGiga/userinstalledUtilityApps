import os
import asyncio
from dotenv import load_dotenv

# from tortoise import connections

load_dotenv()

# Any project imports should be used after the load of .env
from project import ThisBot, spotify


# from project.database import db_init


async def main():
    # await db_init()
    await spotify.setup_spotify_client()
    await ThisBot.start(token=os.getenv("TOKEN"))


@ThisBot.event
async def on_ready():
    print("Started up and ready!")


if __name__ == "__main__":

    ThisBot.load_modules()
    event_loop = asyncio.get_event_loop_policy().get_event_loop()

    try:
        event_loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        print("🛑 Shutting Down")
        event_loop.run_until_complete(ThisBot.close())
        # event_loop.run_until_complete(connections.close_all(discard=True))
        event_loop.stop()
