import discord
from discord.ext import commands
from python_aternos import Client, atserver


atclient = Client()
atclient.login("USERNAME", "PASSWORD")
aternos = atclient.account
servs = aternos.list_servers()


intents = discord.Intents.default()
intents.message_content = True


version = "1.0.0"
prefix = "$"


bot = commands.Bot(intents = intents, command_prefix = prefix)


bot.remove_command('help')


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name=f"{prefix}help - v{version}"))


@bot.command()
async def help(ctx):

    embedVar = discord.Embed(
        title = f"**Aternicord v{version} - Command List:**",
        description="**----------------**",
        color = 0x00ff00
        )
    
    embedVar.add_field(
        name = f"**{prefix}servers**",
        value = "List all avalible servers and their info",
        inline = False
        )
    
    embedVar.add_field(
        name = f"**{prefix}start [Server Name]**",
        value = "Start the specified server\n**Note:** This is very much use at your own risk as it technically breaks Aternos TOS",
        inline = False
        )
    
    embedVar.add_field(
        name = f"**{prefix}status [Server Name]**",
        value = "View the status of the specified server",
        inline = False
        )
    
    embedVar.add_field(
        name = f"**----------------**",
        value = "**Please report any issues to my GitHub:\nhttps://github.com/Chadwickjr**"
    )
    
    await ctx.send(embed=embedVar)


@bot.command()
async def servers(ctx):

    embedVar = discord.Embed(
        title = f"**Servers List:**",
        description="**----------------**",
        color = 0x0CC3CB
        )
    
    for server in servs:
        
        server.fetch()

        table = (
            f"Status: {server.status}\n" +
            f"Address: {server.address}\n" +
            f"Version: {server.edition}, {server.software}, {server.version}\n" +
            "**----------------**"
        )

        embedVar.add_field(
            name = f"**Name: {server.subdomain}**",
            value = table,
            inline = False
            )
    
    await ctx.send(embed=embedVar)


@bot.command()
async def status(ctx, arg):

    passed = False

    for server in servs:
        server.fetch()
        if arg.lower() == server.subdomain.lower():

            if server.status == "online":
                passed = True
                embedVar = discord.Embed(
                    title = f"**{server.subdomain} - Status:**",
                    description = (server.status).capitalize(),
                    color = 0x00FF15
                )
                break

            else:
                passed = True
                embedVar = discord.Embed(
                    title = f"**{server.subdomain} - Status:**",
                    description = (server.status).capitalize(),
                    color = 0xF70202
                )
                break

    if not passed:
        embedVar = discord.Embed(
            title = f"**Couldn't Find Server!**",
            description = "Double check that you have the right server name, then try again. You can view all server names with **$servers**",
            color = 0xF70202
        )
    
    await ctx.send(embed=embedVar)


@bot.command()
async def start(ctx, arg):

    passed = False

    for server in servs:
        server.fetch()
        if arg.lower() == server.subdomain.lower():

            if server.status != "online":
                passed = True

                try:
                    server.start()
                    embedVar = discord.Embed(
                        title = f"**Successfully Starting {server.subdomain}!**",
                        description = "This may take a moment. You can check when the server comes online using $status [Server Name]",
                        color = 0xFFBC05
                    )
                    
                except:
                    embedVar = discord.Embed(
                        title = f"**Failed to start!",
                        description = "This is likely an issue with the bot or Aternos itself",
                        color = 0xFFBC05
                    )
                break

            else:
                passed = True
                embedVar = discord.Embed(
                    title = f"**{server.subdomain} is already started!",
                    description = "Server is already running. Please try again when the server is offline",
                    color = 0xFFBC05
                )
                break


    if not passed:
        embedVar = discord.Embed(
            title = f"**Couldn't Find Server!**",
            description = "Double check that you have the right server name, then try again. You can view all server names with **$servers**",
            color = 0xF70202
        )
    
    await ctx.send(embed=embedVar)


bot.run("YOUR TOKEN")