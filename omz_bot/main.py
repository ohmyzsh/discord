import discord

TOKEN = ""

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready for action!")

CONFIG = {
    642496866407284746: {
        "banMsg": "You have been banned by our automated spam prevention! If you believe this to be in error, contact @thetechrobo or @oliviawolfie to get unbanned.",
        "channel": 710190946268217384
    },
}

@bot.event
async def on_message(message):
    if not message.guild:
        print("Invalid guild for message", message)
        return
    config = CONFIG.get(message.guild.id)
    if not config:
        print("No config for guild", message.guild)
        return
    if message.channel.id != config['channel']:
        return
    if message.author == bot.user:
        return
    try:
        await message.author.send(config['banMsg'])
    except KeyError:
        print("WARNING: No ban msg setup for guild", message.guild)
    await message.author.ban(reason="Dared to speak in the sacred channel", delete_message_days=1)
    print(f"Caught someone! [{message.created_at.timestamp()}] <{message.author} ({message.author.id})> in {message.guild}")

bot.run(TOKEN)
