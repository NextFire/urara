import logging

import discord
from discord import app_commands
from pydantic_ai import ModelMessage

from urara.agent import agent

logger = logging.getLogger(__name__)


class UraraClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.user: discord.ClientUser
        self.tree = app_commands.CommandTree(self)
        self.message_history: list[ModelMessage] = []

    async def setup_hook(self):
        await self.tree.sync()


client = UraraClient()


@client.event
async def on_ready():
    logger.info(
        f"Logged in as {client.user} "
        f"https://discord.com/oauth2/authorize?client_id={client.user.id}"
    )


@client.tree.command()
async def urara_ask(interaction: discord.Interaction, prompt: str):
    """Asks Urara a question."""
    await interaction.response.defer()
    try:
        result = await agent.run(prompt, message_history=client.message_history)
        await interaction.followup.send(result.output)
        client.message_history = result.all_messages()
    except Exception as e:
        await interaction.followup.send(str(e))
        raise


@client.tree.command()
async def urara_reset(interaction: discord.Interaction):
    """Resets the message history."""
    client.message_history = []
    await interaction.response.send_message("Message history cleared.", ephemeral=True)
