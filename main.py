import discord
from discord.ext import commands
import random
import os
import time

file_path = {
    "test": "test.txt"
}
vouch_channelid = 123
free_channelid = 123
log1 = 123
prefix = ""
token = "Your Token Here"
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is running with Silver Gen\n We're Better! ❤️")
    status = [
        "Running with Silvergen 🔥",
        "Silvergen is the best! 👑",
        "Silvergen on top! 💯",
        "Life Is Better When Using Silvergen."
    ]
    r = random.choice(status)
    await bot.change_presence(activity=discord.Game(r))
    await bot.tree.sync()
    print("Slash Commands Synced!")

@bot.tree.command(name="stock", description="Displays the current stock.")
async def stock(interaction: discord.Interaction):
    if interaction.channel_id != free_channelid:
        redembed = discord.Embed(title="Wrong Channel!", description=f"Please use <#{free_channelid}> to use this command." , color=0xFF0000)
        await interaction.response.send_message(embed=redembed, ephemeral=True)
        return
    stock_data = {}

    for key, path in file_path.items():
        content = ""
        if os.path.exists(path):
            with open(path, "r") as f:
                content = f.read().strip()
                stock_data[key] = "0" if not content else content.splitlines()
        else:
            stock_data[key] = "I CAN'T FIND IT!"

    embed = discord.Embed(title="Silvergen Stock", color=discord.Color.green(), description="Here is the current stock:")

    for service, counts in stock_data.items():
        if isinstance(counts, list):
            count = len(counts)
            embed.add_field(name=f"**{service}**", value=f"`{count}`", inline=False)
        else:
            embed.add_field(name=f"**{service}**", value=f"**{counts}**", inline=False)

    embed.set_image(url="https://media.discordapp.net/attachments/960440723369517106/996423763522506782/rainbow-border.gif?ex=670d2b71&is=670bd9f1&hm=c09480d50b847e2057dc00338bcb918f40dde7546a9a4c08faf7fc3d08f2c530&")
    embed.add_field(name="**Silvergen**", value="[**DISCORD**](https://discord.gg/HvvsbpVz7d)", inline=False)
    embed.set_footer(text="Made By Silvergen! ❤️‍🔥")

    await interaction.response.send_message(embed=embed)

user_cooldown = {}

@bot.tree.command(name="free", description="Generate a specified service.")
async def free(interaction: discord.Interaction, service: str):
    if interaction.channel_id != free_channelid:
        redembed = discord.Embed(title="Wrong Channel!", description=f"Please use <#{free_channelid}> to use this command." , color=0xFF0000)
        await interaction.response.send_message(embed=redembed, ephemeral=True)
        return
    cooldown_time = 10  
    current_time = time.time()
    
    if interaction.user.id in user_cooldown:
        remaining_time = cooldown_time - (current_time - user_cooldown[interaction.user.id])
        if remaining_time > 0:
            await interaction.response.send_message(
                f"## Please wait **{remaining_time:.0f}** seconds before generating another account.",
                ephemeral=True
            )
            return

    user_cooldown[interaction.user.id] = current_time

    if service in file_path:
        file_name = file_path[service]

        with open(file_name, "r") as f:
            lines = f.readlines()

        if not lines:
            await interaction.response.send_message("## No stock for this service or this is an error.", ephemeral=True)
            del user_cooldown[interaction.user.id]  
            return
        
        line = random.choice(lines).strip()  
        await interaction.response.send_message(f"**GENERATED ✅** `Please Check Your DMs`\n|| {interaction.user.mention} ||")

        dm_embed = discord.Embed(title="Generated Free Account", color=discord.Color.green())
        dm_embed.add_field(name="Service", value=service, inline=False)
        dm_embed.add_field(name="Account", value=f"```{line}```", inline=False)
        dm_embed.set_image(url="https://media.discordapp.net/attachments/960440723369517106/996423763522506782/rainbow-border.gif?ex=670d2b71&is=670bd9f1&hm=c09480d50b847e2057dc00338bcb918f40dde7546a9a4c08faf7fc3d08f2c530&")
        dm_embed.add_field(name="**Join Our Discord!**", value="[**DISCORD**](https://discord.gg/HvvsbpVz7d)", inline=False)
        dm_embed.set_footer(text="Made By Silvergen! ❤️‍🔥")
        
        await interaction.user.send(embed=dm_embed)

        lines = [l.strip() for l in lines if l.strip() != line]  
        with open(file_name, "w") as f:
            f.writelines([l + "\n" for l in lines])  

        log_channel = bot.get_channel(log1)  
        log_embed = discord.Embed(title="Service Used", description=f"{interaction.user} generated a {service}.", color=discord.Color.blue())
        log_embed.add_field(name="Generated Line", value=f"`{line}`", inline=False)
        await log_channel.send(embed=log_embed)

    else:
        await interaction.response.send_message("## Invalid service provided.", ephemeral=True)
        del user_cooldown[interaction.user.id]

@bot.tree.command(name="restock", description="Restock a service.")
async def restock(interaction: discord.Interaction, service: str, file: discord.Attachment):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("## You do not have permission to use this command.", ephemeral=True)
        return      
    if service not in file_path:
        await interaction.response.send_message("## Invalid service.", ephemeral=True)
        return

    file_name = file_path[service]

    try:
        stock_content = (await file.read()).decode("utf-8").splitlines()

        with open(file_name, "a") as f:
            f.writelines([f"{line}\n" for line in stock_content])

        await interaction.response.send_message(f"**Restocked `{len(stock_content)}` items for {service}.**")
    
    except Exception as e:
        await interaction.response.send_message(f"## Failed to restock: {str(e)}", ephemeral=True)


@bot.tree.command(name="vouch", description="Give a vouch for Silvergen.")
async def vouch(interaction: discord.Interaction):
    if interaction.channel_id != vouch_channelid:
        redembed = discord.Embed(title="Wrong Channel!", description=f"Please use <#{vouch_channelid}> to use this command." , color=0xFF0000)
        await interaction.response.send_message(embed=redembed, ephemeral=True)
        return
    vouch_embed = discord.Embed(
        title="Vouch for Silvergen",
        description="Thank you for your support! 💖 **Silvergen** truly appreciates your trust in our services!",
        color=discord.Color.magenta()
    )
    vouch_embed.set_image(url="https://media.discordapp.net/attachments/960440723369517106/996423763522506782/rainbow-border.gif")
    vouch_embed.set_footer(text="Made By Silvergen! ❤️‍🔥")

    await interaction.response.send_message(embed=vouch_embed)


bot.run(token)
