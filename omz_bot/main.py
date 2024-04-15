import discord
import json

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents = intents)
tree = discord.app_commands.CommandTree(bot)

with open("config.json", "r") as f:
    config = json.load(f)

with open("omz-faq.json", "r") as f:
    faqEntries = json.load(f)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"{bot.user} is ready for action!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif not message.guild:
        print("Invalid guild for message", message)
        return

    spamConf = config["spamtrap"].get(str(message.guild.id))

    if not spamConf:
        print("No config for guild", message.guild)
        return
    channel = spamConf['channel']
    if isinstance(channel, int):
        if message.channel.id != channel:
            return
    else:
        if message.channel.id not in channel:
            return

    try:
        await message.author.send(spamConf['banMsg'])
    except KeyError:
        print("WARNING: No ban msg setup for guild", message.guild)
    except discord.errors.Forbidden:
        # Ignore errors for DM failures
        pass
    await message.author.ban(reason="Dared to speak in the sacred channel", delete_message_days=1)
    print(f"Caught someone! [{message.created_at.timestamp()}] <{message.author} ({message.author.id})> in {message.guild}")

@tree.command(name = "alive", description = "Ensures the bot is live")
@discord.app_commands.checks.has_permissions(manage_messages=True)
async def alive(interaction: discord.Interaction):
    await interaction.response.send_message("No, I'm dead.", ephemeral = True)

@tree.command(name = "faq", description = "Sends an FAQ link")
async def faq(interaction: discord.Interaction, key: str = "_all", mention: discord.User = None):
    url = None
    message = None
    if (key == "_all"):
        url = "https://github.com/ohmyzsh/ohmyzsh/wiki/FAQ"
        message = "The entire FAQ is available on ohmyzsh's GitHub:"
    elif key not in faqEntries:
        await interaction.response.send_message("That's not a valid key. Try again.", ephemeral = True)
        return
    else:
        url = faqEntries[key]
        if mention is None:
            message = f"FAQ entry \"{key}\":"
        else:
            message = f"FAQ entry for \"{key}\":"

    ping = ""
    if mention is not None:
        ping = f"{mention.mention}, "
        if key == "_all":
            message = message[0].lower() + message[1:]
        else:
            ping += "see the "

    await interaction.response.send_message(f"{ping}{message} <{url}>")

@faq.autocomplete("key")
async def faq_autocomplete(interaction: discord.Interaction, current: str):
    result = [
        discord.app_commands.Choice(name = title, value = title) for title, url in faqEntries.items() if current is None or current.lower() in title.lower()
    ]

    if len(result) > 25:
        return result[0:24]
    return result

bot.run(config["token"])
