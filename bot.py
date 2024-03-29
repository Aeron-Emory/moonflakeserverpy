import discord
from discord.ext import commands
from discord import app_commands
import requests
import exaroton
import os

from threading import Thread
from flask import Flask

app = Flask(__name__)

@app.route('/healthz')
def health():
    return "OK", 200

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

# Bot and Exaroton configuration
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
EXAROTON_API_KEY = os.environ.get('EXAROTON_API_KEY')
EXAROTON_SERVER_ID = os.environ.get('EXAROTON_SERVER_ID')

# Initialize bot with all intents enabled
intents = discord.Intents.all()
# bot = commands.Bot(command_prefix="", intents=intents)
bot = commands.Bot(command_prefix=lambda bot, msg: "", intents=intents)

# Initialize Exaroton API client
exaroton_client = exaroton.Exaroton(EXAROTON_API_KEY)


@bot.event
async def on_ready():
  print("Bot is Up and Ready!")
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
  except Exception as e:
    print(e)


# Slash command for starting the server
@bot.tree.command(name="start", description="Start the Minecraft server")
async def start(interaction: discord.Interaction):
  try:
    response = exaroton_client.start(EXAROTON_SERVER_ID)
    await interaction.response.send_message("Minecraft server is starting...")
  except Exception as e:
    await interaction.response.send_message(
        f"Failed to start the server. Error: {e}", ephemeral=True)


# Run the bot
bot.run(DISCORD_TOKEN)
