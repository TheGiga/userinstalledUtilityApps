from abc import ABC
import discord
import config


class ThisBotContext(discord.ApplicationContext):
    def __init__(self, bot: 'ThisBot', interaction: discord.Interaction):
        super().__init__(bot, interaction)


class _ThisBot(discord.Bot, ABC):
    def __init__(self, *args, **options):
        super().__init__(*args, **options)

    def load_modules(self) -> None:
        """
        Loads extensions, prints out loaded extensions.
        :return: doesn't return anything
        """
        for module in config.ENABLED_MODULES:
            self.load_extension(module), print(f"{module} loaded!")

    async def get_application_context(
            self, interaction: discord.Interaction, cls=ThisBotContext
    ):
        # Subclassing ApplicationContext.
        return await super().get_application_context(interaction, cls=cls)


ThisBot = _ThisBot(intents=discord.Intents.all())
