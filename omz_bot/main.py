import discord
import json

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents = intents)


with open("config.json", "r") as f:
    config = json.load(f)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready for action!")

@bot.event
async def on_message(message):
    if not message.guild:
        print("Invalid guild for message", message)
        return
    spamConf = config["spamtrap"].get(str(message.guild.id))
    if not spamConf:
        print("No config for guild", message.guild)
        return
    if message.channel.id != spamConf['channel']:
        return
    if message.author == bot.user:
        return
    try:
        await message.author.send(spamConf['banMsg'])
    except KeyError:
        print("WARNING: No ban msg setup for guild", message.guild)
    await message.author.ban(reason="Dared to speak in the sacred channel", delete_message_days=1)
    print(f"Caught someone! [{message.created_at.timestamp()}] <{message.author} ({message.author.id})> in {message.guild}")

bot.run(config["token"])
