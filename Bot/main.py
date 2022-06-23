import random
import discord
from discord import Color
import discord.utils
import requests
import asyncio
import json


from discord.ext import commands


with open("config.json") as f:
  data = json.load(f)


#cogs = [music]
#for i in range(len(cogs)):
#  cogs[i].setup()

token = data["token"]

prefix = "!"
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(prefix, intents=intents)

c = ["praying-to-god", "lost-ark"]

fbLinksAllowed = True

maxFbLinks = 3

usersWarnings = {}


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.playing, name=f"with your pp"))
    print(discord.__version__ + "\n")
    random.seed()


@bot.command(name="insult")
async def insult(ctx, target="", language="en"):
    link = "https://insult.mattbas.org/api/insult"
    response = requests.get(link)

    if target != "":
        title = ""
        target = target.replace('@', "")
        target = target.replace('<', "")
        target = target.replace('>', "")
        try:
            user = await bot.fetch_user(target)
            if user is not None:
                title = response.text.lower()
                embed = discord.Embed(title=f"{user.name}" + ", " + title,
                                      color = 0xe74c3c)
                await ctx.send(embed=embed)
                return
        except discord.HTTPException:
            pass
        title = target.capitalize() + ", " + response.text.lower()
    else:
        title = response.text

    embed = discord.Embed(title=f"**{title}**", color = 0xe74c3c)
    await ctx.send(embed=embed)


@bot.command(name="rn")
async def rn(ctx, min=0, max=1000):
    await ctx.message.delete()
    min = float(min)
    max = float(max)

    rnd = random.uniform(min, max)
    rnd = int(rnd)
    embed = discord.Embed(title=f"Entre 1 e 1999\n\n**Saiu {rnd}**",
                          color=0x00beff)
    await ctx.send(embed=embed)


@bot.command(name="lol")
async def lol(ctx):
    await ctx.message.delete()
    await ctx.channel.send("Olá Mauro. Estou de olho em ti")


@bot.command(name="ajuda")
async def ajuda(ctx):
    await ctx.channel.send("Work in progress")


@bot.command(name="fb")
async def fb(ctx):
  global fbLinksAllowed
  
  await ctx.message.delete()
  
  
  if fbLinksAllowed == True:
    embed = discord.Embed(title="Desbloqueados",
                              description="Sim sim metam links à vontade lol",
                              color = 0x3498db)
    await ctx.channel.send(embed=embed)
    return
  elif fbLinksAllowed == False:
    embed = discord.Embed(title="Bloqueados",
                              description="Quem meter links do facebook ta fodido",
                              color = 0xe74c3c)
    await ctx.channel.send(embed=embed)


@bot.command(name="allowFb")
async def allowFb(ctx, allow="true"):
    global fbLinksAllowed
  
    await ctx.message.delete()
    if (allow.lower() == "true"):
        fbLinksAllowed = True
        embed = discord.Embed(title="Links do facebook desbloqueados",
                              description="Pronto metam prai links à vontade",
                              color = 0x3498db)
        embed.set_author(name="Officer Pepega")
        embed.set_footer(text="Para bloquear: !allowFb false")
        await ctx.send(embed=embed)
    elif (allow.lower() == "false"):
        fbLinksAllowed = False
        embed = discord.Embed(title="Links do facebook bloqueados",
                              description="Acabaram-se os links do facebook",
                              color = 0xe74c3c)
        embed.set_author(name="Officer Pepega")
        embed.set_footer(text="Para desbloquear: !allowFb true")
        await ctx.send(embed=embed)


@bot.command()
async def clear(ctx, amount=1):
  
  if amount > 25:
      await ctx.channel.send('Só 25 de cada vez oh caralho')
      return
    
  amount = int(amount)
  if amount == -194669:
    await ctx.channel.purge()
  elif amount > 0 and amount < 101:
    await ctx.channel.purge(limit=amount)


@bot.event
async def on_message(message):

    channelName = str(message.channel.name)
    _user_message = str(message.content)
  
    if message.author == bot.user or channelName not in c:
        return

    #if allowFb == False:
    if 'pepega' in _user_message.lower():
      await message.channel.send('Tou aqui')
      
				
	
    await check_facebook_links(message)
    await bot.process_commands(message)


async def check_facebook_links(message):

    _username = str(message.author).split('#')[0]
    _user_message = str(message.content)
    _channel = str(message.channel.name)

    afkChannel = bot.get_channel(768138979715055618) 
    

    s = _user_message.lower().split("/")

    if 'facebook.' in _user_message.lower() and 'video' in s or 'facebook.' in _user_message.lower() and 'group' in s or 'fb.watch' in _user_message.lower():

      if _username in usersWarnings:

        wAmount = usersWarnings[_username]
        wAmount += 1
        usersWarnings[_username] = wAmount

        if usersWarnings[_username] >= maxFbLinks:
          await message.channel.send(f'O {message.author.mention} precisou de ir descansar um pouco.\nDeus perdoa mas o Officer Pepega não')
          await message.author.move_to(afkChannel, reason=None)
          return
        
        file = discord.File('nofb.png')
        await message.delete()
        await asyncio.sleep(1)
        await message.channel.send(
            f'{message.author.mention}, aqui não se partilham links do facebook. É o teu {usersWarnings[_username]} aviso\nAos {maxFbLinks} vais descansar um bocado\n',
            file=file)
                
      else:
        file = discord.File('nofb.png')
        usersWarnings[_username] = 1
        await message.delete()
        await asyncio.sleep(1)
        await message.channel.send(
          f'{message.author.mention}, aqui não se partilham links do facebook. É o teu 1 aviso\nAos {maxFbLinks} vais descansar um bocado\n',
          file=file)

      


bot.run(token)

#users = bot.get_all_members()
#user = None
#for u in users:          --> CASO SE QUEIRA DAR MENTION <--
#if u.name == target:
#user = u
#break
#if user is not None:
#await ctx.channel.send(user.mention)
