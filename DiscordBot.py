from http.client import responses

import discord
from discord.ext import commands
import random
import re
import asyncio

intents = discord.Intents.all()
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.bans = True
intents.messages = True
intents.guild_messages = True
intents.guilds = True
intents.guild_typing = True
intents.dm_messages = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

trolling_users = set()
link_pattern = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
def has_permission(ctx):
    return ctx.author.id in [614066142281072660, 1208078966456586270]

log_channel_id = 1138957199079649412

@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready!')

@bot.event
async def on_member_join(member):
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(f"**Member Joined**\nÜye: {member.mention}")

@bot.event
async def on_member_remove(member):
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(f"**Member Left**\nÜye: {member.mention}")

@bot.event
async def on_member_ban(guild, user):
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(f"**Member Banned**\nÜye: {user.mention}")

@bot.event
async def on_member_unban(guild, user):
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(f"**Member Unbanned**\nÜye: {user.mention}")

@bot.event
async def on_voice_state_update(member, before, after):
    log_channel = bot.get_channel(log_channel_id)
    if before.channel != after.channel:
        if after.channel:
            await log_channel.send(f"**Member Joined The Voice Channel**\nÜye: {member.mention}\nKanal: {after.channel.name}")
        elif before.channel:
            await log_channel.send(f"**Member Left Voice Channel**\nÜye: {member.mention}\nKanal: {before.channel.name}")

@bot.event
async def on_typing(channel, user, when):
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(f"**A Member Started Writing**\nÜye: {user.mention}\nKanal: {channel.mention}")

@bot.command()
async def troll(ctx, target_user: discord.Member):
    if ctx.author.voice and target_user.voice and has_permission(ctx):
        trolling_users.add(target_user.id)
        await ctx.send(f"{target_user.display_name} is carried over to all audio channels...")
        for guild in bot.guilds:
            for voice_channel in guild.voice_channels:
                try:
                    await target_user.move_to(voice_channel)
                except discord.Forbidden:
                    await ctx.send(f"{target_user.display_name} {voice_channel.name} Couldn't move to channel (Yetki eksik).")
                except discord.HTTPException:
                    await ctx.send(f"{target_user.display_name} {voice_channel.name} Couldn't move to channel (HTTP error).")
                except Exception as e:
                    await ctx.send(f"{target_user.display_name} {voice_channel.name} Could not move to channel (Unknown error: {e}).")
        await ctx.send(f"{target_user.display_name} moved to all audio channels.")
    else:
        await ctx.send("To use the command, both you and the target user must be in a voice channel and you must have certain authority..")

@bot.command()
async def untroll(ctx, target_user: discord.Member):
    if target_user.id in trolling_users and has_permission(ctx):
        trolling_users.remove(target_user.id)
        await ctx.send(f"{target_user.display_name} is removed from all audio channels...")
        for guild in bot.guilds:
            for voice_channel in guild.voice_channels:
                if target_user.voice and target_user.voice.channel == voice_channel:
                    try:
                        await target_user.move_to(None)
                    except discord.Forbidden:
                        await ctx.send(f"{target_user.display_name} {voice_channel.name} Could not be removed from the channel (Not authorized).")
                    except discord.HTTPException:
                        await ctx.send(f"{target_user.display_name} {voice_channel.name} could not be removed from the channel (HTTP error).")
                    except Exception as e:
                        await ctx.send(f"{target_user.display_name} {voice_channel.name} could not be removed from the channel (Unknown error: {e}).")
        await ctx.send(f"{target_user.display_name} removed from all audio channels.")
    else:
        await ctx.send(f"{target_user.display_name} you do not already have authority on all voice channels or a specific one.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    content = message.content.lower()
    if content in responses:
        await message.channel.send(responses[content])
    await bot.process_commands(message)

@bot.command()
async def come(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = ctx.voice_client
        if voice_client:
            await voice_client.move_to(channel)
        else:
            await channel.connect()
    else:
        await ctx.send("You are not on a voice channel.")

@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready!')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1217981719840555100)
    remaining_members = len(member.guild.members)
    message = f'**{member.mention}** joined the server! Currently on the server `{remaining_members}` has become.'
    await channel.send(message)

    role = discord.utils.get(member.guild.roles, name="Gardaşlar")
    await member.add_roles(role)

    dm_message = "Welcome to the server! If you want to get information about the server, you can contact me. Don't forget to invite your friends :)"
    await member.send(dm_message)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1217981719840555100)
    remaining_members = len(member.guild.members)
    message = f'**{member.display_name}** left the server. There are currently `{remaining_members}` remaining people on the server.'
    await channel.send(message)

@bot.command()
async def lock(ctx):
    allowed_user_id = 614066142281072660

    if ctx.author.id != allowed_user_id:
        await ctx.send("Sorry, only a specific user can use this command.")
        return

    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("The channel is locked. Only authorized people can send messages.")

@bot.command()
async def ac(ctx):
    allowed_user_id = 614066142281072660

    if ctx.author.id != allowed_user_id:
        await ctx.send("Sorry, only a specific user can use this command.")
        return

    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("The channel is open. Now everyone can send messages.")

@bot.event
async def on_command(ctx):
    print(f'{ctx.author} command called by: {ctx.message.content}')

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} kicked off the server.')

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} banned from server.')

@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} reversed the ban')
            return

warnings = {}


@bot.command()
async def delete(ctx, amount: int):
    if ctx.message.author.guild_permissions.manage_messages:
        try:
            await ctx.channel.purge(limit=amount + 1)
            message = await ctx.send(f'`{amount}` **message deleted.**')

            await asyncio.sleep(5)
            await message.delete()
        except Exception as e:
            await ctx.send(f'Hata oluştu: {str(e)}')
    else:
        await ctx.send('You do not have sufficient permissions to perform this action.')

@bot.command()
async def warn(ctx, member: discord.Member, *, reason=None):
    if member.id not in warnings:
        warnings[member.id] = []
    warnings[member.id].append(reason)
    await ctx.send(f'{member.mention} warned: {reason}')

@bot.event
async def on_message(message):
    if 'küfür' in message.content.lower():
        await message.delete()
        await message.channel.send(f'{message.author.mention}, Please do not use slang!')
    await bot.process_commands(message)

@bot.command()
async def nuke(ctx):
    if ctx.message.author.guild_permissions.manage_messages:
        try:
            await ctx.channel.purge()
            await ctx.send("Channel Cleared!")
        except Exception as e:
            await ctx.send(f'Error occurred: {str(e)}')
    else:
        await ctx.send('You do not have sufficient permissions for this operation.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if link_pattern.search(message.content):
        if not message.author.bot:
            await message.delete()
            sent_message = await message.channel.send(f"{message.author.mention},` It is forbidden to share messages containing links!`")
            await asyncio.sleep(10)
            await sent_message.delete()

    await bot.process_commands(message)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Commands Help Menu", description="Bot commands and uses", color=0x00ff00)

    embed.add_field(name="!kick", value="Kicks a specific user from the server.", inline=False)
    embed.add_field(name="Usage:", value="`!kick <user> [reason]`", inline=False)

    embed.add_field(name="!ban", value="Bans a specific user from the server.", inline=False)
    embed.add_field(name="Usage:", value="`!ban <user> [reason]`", inline=False)

    embed.add_field(name="!unban", value="Removes a server ban for a specific user.", inline=False)
    embed.add_field(name="Usage:", value="`!unban <user>`", inline=False)

    embed.add_field(name="!warn", value="Gives specific personal warning.", inline=False)
    embed.add_field(name="Usage:", value="`!warn <user> [reason]`", inline=False)

    embed.add_field(name="!delete", value="Deletes a partial number of messages.", inline=False)
    embed.add_field(name="Usage:", value="`!delete <number>`", inline=False)

    embed.add_field(name="!nuke", value="Deletes all messages in the channel.", inline=False)
    embed.add_field(name="Usage:", value="`!nuke`", inline=False)

    embed.add_field(name="!come", value="Joins the voice channel you are in.", inline=False)
    embed.add_field(name="Usage:", value="`!come`", inline=False)

    embed.add_field(name="!member_count", value="Shows the number of active and total members on the server.", inline=False)
    embed.add_field(name="Usage:", value="`!member_count`", inline=False)

    await ctx.send(embed=embed)


bot.run('MTI0MTc3MjUzNzI5MDE2NjI3Mg.GgLXj5.I8ouyctfSQkZeipq7eplo4i4LspGZU51dfRKvc')