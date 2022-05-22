A Moderation bot for your server(cannot be public)

import discord
import os
from discord.ext import commands
import random
import json
from keep_alive import keep_alive


def get_prefix(client,message):

  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]

activity = discord.Activity(type=discord.ActivityType.watching, name="rule breakers")
client = commands.Bot(command_prefix = '#', activity=activity,case_insensitive=True)



filtered_words = ["nigger","shithead","nigga","cunt","cum"]

images = [
  'https://i.imgur.com/JQGhevZ.jpg',
  'https://i.imgur.com/yl4U0ZY.jpg',
  'https://i.imgur.com/NuDbYN6.jpg',
  'https://i.imgur.com/OGwJeAX.jpg',
  'https://i.imgur.com/IFcT93v.jpg',
  'https://i.imgur.com/EAjMADM.jpg',
  'https://i.imgur.com/6AiIwzp.jpg',
  'https://i.imgur.com/SZWbVzh.jpg',
  'https://i.imgur.com/LWMk1N3.jpg',
  'https://i.imgur.com/VCmy1lp.jpg',
  'https://i.imgur.com/UIHtWjS.jpg',
  'https://i.imgur.com/9iUeAKt.jpg',
  'https://i.imgur.com/43IdSrp.jpg',
  'https://i.imgur.com/YYHB9Vm.jpg'
]

@client.event
async def on_message(msg):
  for word in filtered_words:
    if word in msg.content:
      await msg.delete()

  await client.process_commands(msg)

@client.event
async def on_command_error(ctx,error):
  if isinstance(error,commands.MissingPermissions):
    await ctx.send("You can't do that -_-")
    await ctx.message.delete()
  elif isinstance(error,commands.MissingRequiredArgument):
    await ctx.send("Please enter all the required arguements bruh.")
    await ctx.message.delete()
  else:
    raise error
    

@client.command()
async def hello(ctx):
  await ctx.send("This command is working! Or is it?")

@client.command(aliases=['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=2):
  await ctx.channel.purge(limit = amount)

@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "No reason was provided"):
  try:
    await member.send("You have been Kicked from Fiber. Because:"+reason)
  except:
    await ctx.send('The member has their DMs closed')
  
  await member.kick(reason=reason)

@client.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= "No reason was provided"):
  await member.send(member.name + "You have been banned from Fiber. Because: "+reason)
  await member.ban(reason=reason)

@client.command(aliases=['ub'])
@commands.has_permissions(ban_members=True)
async def unban(ctx,*,member):
  banned_users = await ctx.guild.bans()
  member_name, member_disc = member.split('#')

  for banned_entry in banned_users:
    user = banned_entry.user

    if(user.name, user.discriminator)==(member_name,member_disc):

      await ctx.guild.unban(user)
      await ctx.send(member_name +" has been unbanned succesfully")
      return

  await ctx.send(member+" was not found")

@client.command(aliases=['m'])
@commands.has_permissions(kick_members=True)
async def mute(ctx,member : discord.Member):
  muted_role = ctx.guild.get_role(977526507993964554)

  await member.add_roles(muted_role)

  await ctx.send(member.mention + " has been muted")



@client.command(aliases=['user','info'])
@commands.has_permissions(kick_members=True)
async def profile(ctx, member : discord.Member):
  embed = discord.Embed(title = member.name , description = member.mention , color = discord.Colour.red())
  embed.add_field(name = "ID", value = member.id , inline = True)
  embed.set_thumbnail(url = member.avatar_url)
  embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
  await ctx.send(embed=embed)



@client.command()
async def meme(ctx):
  embed = discord.Embed(color = discord.Colour.green())

  random_link = random.choice(images)
  
  embed.set_image(url = random_link)

  await ctx.send(embed = embed)
  




keep_alive()
client.run(os.environ['TOKEN'])
