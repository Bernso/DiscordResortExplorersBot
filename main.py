try:
    import discord
    from discord.ext import commands, tasks
    from discord import app_commands
    import random
    from dotenv import load_dotenv
    import traceback
    import sys
    import os
    from discord import Embed
    import sqlite3
    import pickle
    import loguru
    from discord.ui import Button, View, Select
    from typing import Optional
    from datetime import datetime, timedelta
    from pydantic import BaseModel
except ImportError as e:
    input(e)
    quit()
os.system('cls')

class myLogger:
    def info(message):
        loguru.logger.info(message)

    def warning(message):
        loguru.logger.warning(message)

    def error(message):
        loguru.logger.error(message)

    def success(message):
        loguru.logger.success(message)








        
# Intents setup
intents = discord.Intents.all()
intents.message_content = True


# Bot setup
bot_prefix = ''
characters = "qwertyuiopasdfghjklzxcvbnm1234567890"
for i in range(24):
    bot_prefix += random.choice(characters)
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)


# DB stuff
con = sqlite3.connect('level.db')
cur = con.cursor()

# Vars
ENABLED_USER_ID = 712946563508469832
RECORDS_FILENAME = 'message_records.pkl'
BOT_LOG_CHANNEL_ID = 1284184011085713420
VERIFIED_ROLE_NAME = "Verified"
VERIFY_CHANNEL = 1284184528323215411


# Load existing message records
try:
    with open(RECORDS_FILENAME, 'rb') as file:
        message_records = pickle.load(file)
except FileNotFoundError:
    message_records = []
    myLogger.warning("Message records file not found. Creating a new one.")
    yes = open('message_records.pkl', 'w')
    yes.close()
except EOFError:
    message_records = []
    myLogger.error("The message records file is empty or corrupted.")






class Verification(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.verified_role_id = 1284184639707283476  # Replace with your Verified role ID
        # self.unverified_role_id = 1234090964549767212  # Optionally replace with Unverified role ID if needed

    @discord.ui.button(label="Verify", custom_id="Verify", style=discord.ButtonStyle.success)
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        verified_role = interaction.guild.get_role(self.verified_role_id)
        # unverified_role = interaction.guild.get_role(self.unverified_role_id)  # Optional unverified role
        
        if verified_role:
            if verified_role in user.roles:
                await interaction.response.send_message("You are already verified.", ephemeral=True)
            else:
                # Add the verified role
                await user.add_roles(verified_role)
                # Optionally remove the unverified role
                # if unverified_role:
                #     await user.remove_roles(unverified_role)
                
                await interaction.response.send_message("You have been verified!", ephemeral=True)
                await user.send("You have been verified!")
        else:
            await interaction.response.send_message("Verified role not found.", ephemeral=True)




class RoleButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    role_1_name = "YouTuber"
    role_2_name = "Thoosie"
    role_3_name = "QOTD"
    
    @discord.ui.button(label='1', custom_id="role_1", style=discord.ButtonStyle.primary)
    async def role_1_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role_id = 1284645866107568129  # Replace with your Role 1 ID
        user = interaction.user
        role = interaction.guild.get_role(role_id)
        
        if role:
            if role in user.roles:
                await user.remove_roles(role)
                await interaction.response.send_message(f"Role '{self.role_1_name}' has been removed from you!", ephemeral=True)
            else:
                await user.add_roles(role)
                await interaction.response.send_message(f"Role '{self.role_1_name}' has been added to you!", ephemeral=True)
        else:
            await interaction.response.send_message("Role not found.", ephemeral=True)

    @discord.ui.button(label='2', custom_id="role_2", style=discord.ButtonStyle.primary)
    async def role_2_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role_id = 1284203390611623966  # Replace with your Role 2 ID
        user = interaction.user
        role = interaction.guild.get_role(role_id)
        
        if role:
            if role in user.roles:
                await user.remove_roles(role)
                await interaction.response.send_message(f"Role '{self.role_2_name}' has been removed from you!", ephemeral=True)
            else:
                await user.add_roles(role)
                await interaction.response.send_message(f"Role '{self.role_2_name}' has been added to you!", ephemeral=True)
        else:
            await interaction.response.send_message("Role not found.", ephemeral=True)

    @discord.ui.button(label='3', custom_id="role_3", style=discord.ButtonStyle.primary)
    async def role_3_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role_id = 1284203499915186249  # Replace with your Role 3 ID
        user = interaction.user
        role = interaction.guild.get_role(role_id)
        
        if role:
            if role in user.roles:
                await user.remove_roles(role)
                await interaction.response.send_message(f"Role '{self.role_3_name}' has been removed from you!", ephemeral=True)
            else:
                await user.add_roles(role)
                await interaction.response.send_message(f"Role '{self.role_3_name}' has been added to you!", ephemeral=True)
        else:
            await interaction.response.send_message("Role not found.", ephemeral=True)



async def delete_all_messages(channel: discord.TextChannel):
    # Fetch and delete messages in chunks
    async for message in channel.history(limit=100):  # Adjust limit if needed
        try:
            await message.delete()
        except discord.Forbidden:
            print(f"Bot does not have permission to delete messages in channel {channel.id}")
        except discord.HTTPException as e:
            print(f"Failed to delete message: {e}")



@bot.command(help="Creates the verify message people can use to verify.")
async def start_verify(ctx):
    if ctx.author.guild_permissions.administrator or ctx.author.id == ENABLED_USER_ID:
        embed = discord.Embed(title="Verification", description="Click below to verify.")
        await ctx.send(embed=embed, view=Verification())
    else:
        await ctx.reply("You cannot use this command. Required = Administrator")



@bot.event
async def on_ready():
    myLogger.info(f'Logged in as {bot.user.name}')
    myLogger.info(f'Bot ID: {bot.user.id}')
    myLogger.info(' ')

    await bot.change_presence(status=discord.Status.dnd,
                              activity=discord.Activity(type=discord.ActivityType.watching, name="Resort Explorer"))

    await bot.tree.sync()  # Sync commands with Discord
    myLogger.info("Commands synced")

    # Role selection
    channel = bot.get_channel(1284646235290075176)  # Replace with your channel ID
    if channel:
        view = RoleButtons()

        # Delete all messages in the channel
        await delete_all_messages(channel)

        embed = discord.Embed(
            title="Role Selection",
            description="Click the buttons below to assign or remove roles from yourself.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Roles", value="1. YouTuber\n2. Thoosie\n3. QOTD", inline=False)

        await channel.send(embed=embed, view=view)

    # Verification
    verify_channel = bot.get_channel(VERIFY_CHANNEL)
    if verify_channel:
        try:
            async for message in verify_channel.history():
                await message.delete()
            embed = discord.Embed(title="Verification", description="Click below to verify.")
            await verify_channel.send(embed=embed, view=Verification())
        except Exception as e:
            myLogger.error(f"An error occurred: {e}")
    else:
        myLogger.error("Could not send verification message because VERIFY_CHANNEL is None or not set correctly.")

    # Bot status update
    rex_channel = bot.get_channel(1284214603856744549)
    if rex_channel:
        embed = discord.Embed(
            title="Bot Status",
            description="The bot is currently **online**.",
            color=discord.Color.green()
        )
        await rex_channel.send(embed=embed)

    # Change avatar (only if necessary)
    try:
        with open('channels4_profile (2).jpg', 'rb') as f:
            avatar_bytes = f.read()

        # Check if the current avatar is already set to avoid unnecessary changes
        if bot.user.avatar != avatar_bytes:
            await bot.user.edit(avatar=avatar_bytes)
            await bot.user.edit(username="RE bot")
        else:
            myLogger.info("Avatar is already set to the desired one.")
    except discord.errors.HTTPException as e:
        if e.code == 50035:
            myLogger.error("You are changing the avatar too fast. Try again later.")
        else:
            myLogger.error(f"An error occurred while changing avatar: {e}")




@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user:
        return

    if '#' in str(message.author):
        return

    # Record the message details
    message_record = {
        'channel': str(message.channel),
        'user_id': str(message.author.id),
        'username': str(message.author),
        'message_content': message.content,
        'server_id': str(message.guild),
        'server_name': str(message.guild),
    }
    message_records.append(message_record)

    # Save the updated records to a pickle file
    with open(RECORDS_FILENAME, 'wb') as file:
        pickle.dump(message_records, file)

    myLogger.info(
        f'\nChannel([{message_record["channel"]}]) \nUser id({message_record["user_id"]}) \nUsername({message_record["username"]}) \nMessage({message_record["message_content"]})\nServer name({message_record["server_name"]})\n')

    # Process commands after logging
    await bot.process_commands(message)
    
    if message.author == bot.user:
        return

    try:
        # Fetch the user's current XP
        cur.execute(f"SELECT exp FROM GUILD_{message.guild.id} WHERE user_id={message.author.id}")
        result = cur.fetchone()
        
        if result:
            current_exp = result[0]
            if current_exp == 999999:
                # User has "infinite" XP, so skip normal XP processing
                return
            
            # Normal XP processing
            cur.execute(f"SELECT exp FROM GUILD_{message.guild.id} WHERE user_id={message.author.id}")
            result = cur.fetchone()
            
            if result:
                if result[0] == 99:
                    cur.execute(
                        f"UPDATE GUILD_{message.guild.id} SET exp=0, lvl={result[2] + 1} WHERE user_id={message.author.id}")
                    con.commit()
                else:
                    cur.execute(
                        f"UPDATE GUILD_{message.guild.id} SET exp={result[0] + 1} WHERE user_id={message.author.id}")
                    con.commit()

    except sqlite3.OperationalError:
        pass
    except Exception as e:
        myLogger.error(f"An error has occurred: {e}")

@bot.tree.command(name="sendmessage", description="Send a custom message to a specific channel or the current channel if not specified")
@app_commands.describe(channel="The channel where the message will be sent", message="The message you want to send")
async def sendmessage(interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
    if interaction.user.id == ENABLED_USER_ID:
        # Use the current channel if no channel is specified
        if channel is None:
            channel = interaction.channel

        # Send the message to the specified or current channel
        await channel.send(message)
        await interaction.response.send_message(f"Message sent to {channel.mention}: {message}", ephemeral=True)
    else:
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
    
@bot.tree.command(name="ping", description="Get the bot's latency")
async def ping(interaction: discord.Interaction):
    
    await interaction.response.send_message(f"Pong! Latency: {round(bot.latency * 1000)}ms", ephemeral=True)



@bot.tree.command(name="eos", description="This command puts the bot offline.")
async def eos(interaction: discord.Interaction):
    
    if interaction.user.id == ENABLED_USER_ID:

        # Create an embed for the offline message
        embed = discord.Embed(
            title="Bot Status",
            description="The bot is currently **offline**.",
            color=discord.Color.red()
        )
        
        
        # List of channels to send the offline message
        special_channels = [1284214603856744549]
        
        for ch_id in special_channels:
            channel = bot.get_channel(ch_id)
            if channel:
                await channel.send(embed=embed)
        
        
        # List of channels to send the offline message
        offline_channels = [1284184528323215411, 1284646235290075176]
        
        for ch_id in offline_channels:
            channel = bot.get_channel(ch_id)
            if channel:
                async for message in channel.history():
                    await message.delete()
                await channel.send(embed=embed)

        response_message = interaction.response.send_message("All tasks complete. Logging off...", ephemeral=True)
        
        
        # Shut down the bot
        await bot.close()
        await quit()
    else:
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)





@bot.tree.command(name="get-prefix", description="Gets the bots prefix")
async def get_prefix(interaction: discord.Interaction):
    await interaction.response.send_message(f"My prefix is {bot_prefix}", ephemeral=True)





########################### ALL THIS FOR THE MUTE COMMAND ###########################
class Time(BaseModel):
    name: str
    value: int


class TimeChoices:
    def __init__(self) -> None:
        self.time = []
    
    def add_time(self, unit: Time):
        self.time.append(unit)
    
    def get_time(self):
        return [app_commands.Choice(name=unit.name, value=str(unit.value)) for unit in self.time]

timeChoices = TimeChoices()

timeChoices.add_time(Time(name='Seconds', value=1))
timeChoices.add_time(Time(name='Minutes', value=60))
timeChoices.add_time(Time(name='Hour', value=3600))
timeChoices.add_time(Time(name='Days', value=86400))
timeChoices.add_time(Time(name='Weeks', value=604800))
timeChoices.add_time(Time(name='Months', value=2629746))


choicesTime = timeChoices.get_time()




@bot.tree.command(name="mute", description="Mute a user")
@app_commands.describe(member="User to mute", duration="Duration to mute", unit="Time unit (seconds, minutes, hours)")
@app_commands.choices(unit=choicesTime)
async def mute(interaction: discord.Interaction, member: discord.Member, duration: int, unit: discord.app_commands.Choice[str]):
    # Check user permissions
    if not (interaction.user.guild_permissions.manage_roles or interaction.user.id == ENABLED_USER_ID):
        await interaction.response.send_message("You don't have permission to mute users.", ephemeral=True)
        return

    # Ensure valid duration
    if duration <= 0:
        await interaction.response.send_message("Invalid duration. Please enter a positive number.", ephemeral=True)
        return

    # Convert duration to seconds
    fulTime = duration * int(unit.value)  # Convert the string value to an integer

    # Mute the user
    try:
        timeout_until = discord.utils.utcnow() + timedelta(seconds=fulTime)
        await member.timeout(timeout_until, reason=f"Muted by {interaction.user}")
        await interaction.response.send_message(f"Muted out {member.mention} for {duration} {unit.name}.")
        # Log successful mute (optional)
        myLogger.info(f"{interaction.user} muted {member} for {duration} {unit.name}.")
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to mute this user.", ephemeral=True)
    except Exception as e:
        myLogger.error(f"Error muting user: {e}")
        await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)


@bot.tree.command(name="unmute", description="Unmute a user")
@app_commands.describe(member="User to unmute")
async def unmute(interaction: discord.Interaction, member: discord.Member):
    # Check user permissions
    if not (interaction.user.guild_permissions.manage_roles or interaction.user.id == ENABLED_USER_ID):
        await interaction.response.send_message("You don't have permission to unmute users.", ephemeral=True)
        return

    # Check if the member is already unmuted
    if member.timed_out_until is None:
        await interaction.response.send_message(f"{member.mention} is not muted.", ephemeral=True)
        return

    # Unmute the user
    try:
        await member.timeout(None, reason=f"Unmuted by {interaction.user}")
        await interaction.response.send_message(f"Unmuted {member.mention}.")
        # Log successful unmute (optional)
        myLogger.info(f"{interaction.user} unmuted {member}.")
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to unmute this user.", ephemeral=True)
    except Exception as e:
        myLogger.error(f"Error unmuting user: {e}")
        await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)




@bot.tree.command(name='ban', description="Bans the user inputted.")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    # Check if the user invoking the command has the necessary permissions
    if interaction.user.id == ENABLED_USER_ID or interaction.user.guild_permissions.ban_members:
        # Ban the member
        await member.send(f"You have been banned from Resort Explorers for this reason: {reason}")
        await member.ban(reason=reason)
        # Send a confirmation message
        await interaction.response.send_message(f"{member.mention} has been banned from the server.")
    else:
        # If the user doesn't have the necessary permissions, reply with an error message
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)



@bot.tree.command(name='unban', description="Unbans the user by their ID.")
async def unban(interaction: discord.Interaction, user_id: str):
    # Check if the user invoking the command has the necessary permissions
    if interaction.user.id == ENABLED_USER_ID or interaction.user.guild_permissions.ban_members:
        try:
            # Convert the input to an integer
            user_id = int(user_id)
        except ValueError:
            await interaction.response.send_message("Please provide a valid user ID (integer).", ephemeral=True)
            return

        # Search for the user in the list of banned members
        async for ban_entry in interaction.guild.bans():
            if ban_entry.user.id == user_id:
                # Unban the user
                await interaction.guild.unban(ban_entry.user)
                await interaction.response.send_message(f"{ban_entry.user.mention} has been unbanned from the server.")
                return

        # If the user wasn't found in the banned list
        await interaction.response.send_message("User not found in the ban list.", ephemeral=True)
    else:
        # If the user doesn't have the necessary permissions, reply with an error message
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)





@bot.tree.command(name="create_role", description="Creates a mentionable role with a name and color, and optionally assigns it to mentioned members.")
async def create_role(interaction: discord.Interaction, name: str, color: str, members: Optional[discord.Member] = None):
    # Check if the user has administrator permissions
    if interaction.user.guild_permissions.administrator or interaction.user.id == ENABLED_USER_ID:
        guild = interaction.guild

        # Convert the color string to a discord.Color object
        try:
            color = discord.Color(int(color.strip('#'), 16))  # Convert hex code to discord.Color
        except ValueError:
            await interaction.response.send_message("Invalid color format. Please provide a valid hex color code (e.g., #FF5733).", ephemeral=True)
            return

        # Check if the role already exists
        if discord.utils.get(guild.roles, name=name):
            embed = discord.Embed(
                title="Error",
                description=f"Role '{name}' already exists.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Create the role with the specified name and color
        new_role = await guild.create_role(name=name, color=color, mentionable=True)

        # Set the position of the new role
        await new_role.edit(position=1)

        # Assign the role to each member, if any are provided
        if members:
            await members.add_roles(new_role)

        # Generate a response
        embed = discord.Embed(
            title="Role Created",
            description=f"Role '{name}' created by {interaction.user.mention}.",
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed, ephemeral=False)
    else:
        # If the user doesn't have the necessary permissions
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)






@bot.event
async def on_member_join(member):
    # Get the log channel
    log_channel = bot.get_channel(BOT_LOG_CHANNEL_ID)
    general_chat = bot.get_channel(1284146525001482280) # channel for joins

    

    # Database setup
    cur.execute(
        f'''CREATE TABLE IF NOT EXISTS GUILD_{member.guild.id} (user_id int NOT NULL, exp int DEFAULT 0, lvl int DEFAULT 0) ''')

    # Add all existing members to the database if not already present
    for x in member.guild.members:
        if not x.bot:
            cur.execute(f"INSERT INTO GUILD_{member.guild.id} (user_id) VALUES ({x.id})")

    con.commit()

    if log_channel:
        # Create an embedded message for member join event
        embed = discord.Embed(title="Member Joined", description=f"{member.mention} has joined the server! \nWelcome!",
                              color=discord.Color.green())
        await log_channel.send(embed=embed)
        await general_chat.send(embed=embed)
    else:
        myLogger.info("Log channel not found.")



# Member Leave Event
@bot.event
async def on_member_remove(member):
    log_channel = bot.get_channel(BOT_LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(title="Member Left", description=f"{member.mention} has left the server.",
                              color=discord.Color.red())
        await log_channel.send(embed=embed)
    else:
        myLogger.error("Log channel not found for on_member_remove.")



# Member Join Event
@bot.event
async def on_member_join(member):
    log_channel = bot.get_channel(BOT_LOG_CHANNEL_ID)
    general_chat = bot.get_channel(1284146525001482280)

    # Add the new member to the database
    cur.execute(f'''CREATE TABLE IF NOT EXISTS GUILD_{member.guild.id} (user_id int PRIMARY KEY, exp int DEFAULT 0, lvl int DEFAULT 0)''')

    # Use a parameterized query to avoid SQL injection
    try:
        for x in member.guild.members:
            if not x.bot:
                cur.execute(f"INSERT OR IGNORE INTO GUILD_{member.guild.id} (user_id) VALUES (?)", (x.id,))
        con.commit()
    except Exception as e:
        myLogger.error(f"Error updating database for {member.name}: {e}")

    if log_channel:
        embed = discord.Embed(title="Member Joined", description=f"{member.mention} has joined the server! Welcome!",
                              color=discord.Color.green())
        await log_channel.send(embed=embed)
        await general_chat.send(embed=embed)
    else:
        myLogger.error("Log channel not found for on_member_join.")



# Stickers Update Event
@bot.event
async def on_guild_stickers_update(guild, before, after):
    added_stickers = [sticker for sticker in after if sticker not in before]
    deleted_stickers = [sticker for sticker in before if sticker not in after]

    try:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.sticker_create):
            moderator = entry.user
            break
    except Exception as e:
        myLogger.error(f"Error retrieving audit logs for sticker changes: {e}")
        return

    log_channel = bot.get_channel(1284184011085713420)
    if log_channel:
        if added_stickers:
            embed = discord.Embed(title="Sticker Created", color=discord.Color.green())
            for sticker in added_stickers:
                embed.add_field(name="Sticker Created", value=f"{moderator.mention} created {sticker.name}", inline=False)
            await log_channel.send(embed=embed)
        if deleted_stickers:
            embed = discord.Embed(title="Sticker Deleted", color=discord.Color.red())
            for sticker in deleted_stickers:
                embed.add_field(name="Sticker Deleted", value=f"{moderator.mention} deleted {sticker.name}", inline=False)
            await log_channel.send(embed=embed)
    else:
        myLogger.error("Log channel not found for sticker updates.")



@bot.event
async def on_guild_emojis_update(guild, before, after):
    added_emojis = [emoji for emoji in after if emoji not in before]  # Check added emojis
    deleted_emojis = [emoji for emoji in before if emoji not in after]  # Check deleted emojis

    # Initialize moderator as None
    moderator = None

    # Get the moderator who modified the emojis
    try:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.emoji_create):
            if added_emojis and entry.target in added_emojis:  # Check if the entry matches the added emoji
                moderator = entry.user
                break  # Found the correct moderator for emoji creation

        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.emoji_delete):
            if deleted_emojis and entry.target in deleted_emojis:  # Check if the entry matches the deleted emoji
                moderator = entry.user
                break  # Found the correct moderator for emoji deletion
    except discord.Forbidden:
        myLogger.error("Bot does not have permission to view audit logs.")
    except Exception as e:
        myLogger.error(f"Unexpected error when retrieving audit logs: {e}")

    # If no moderator is found, handle it
    if moderator is None:
        myLogger.warning("No moderator found in the audit logs.")
        return  # Abort if we can't find the moderator responsible for the changes

    # Log emoji creation/deletion in a specific channel
    channel_id = 1284184011085713420  # Replace with the ID of your desired channel
    log_channel = bot.get_channel(channel_id)

    if log_channel:
        if added_emojis:
            embed = discord.Embed(title="Emoji Created", color=discord.Color.green())

            for emoji in added_emojis:
                embed.add_field(name="Emoji Created", value=f"{moderator.mention} created :{emoji.name}:", inline=False)

            await log_channel.send(embed=embed)
            myLogger.info(f"Sent: {emoji.name} created")

        if deleted_emojis:
            embed = discord.Embed(title="Emoji Deleted", color=discord.Color.red())

            for emoji in deleted_emojis:
                embed.add_field(name="Emoji Deleted", value=f"{moderator.mention} deleted :{emoji.name}:", inline=False)

            await log_channel.send(embed=embed)
            myLogger.info(f"Sent: {emoji.name} deleted")
    else:
        myLogger.error("Log channel not found or is inaccessible.")



@bot.event
async def on_text_channel_update(before, after):
    if before.overwrites != after.overwrites:
        # Determine the permission changes
        added_overwrites = [overwrite for overwrite in after.overwrites if overwrite not in before.overwrites]
        removed_overwrites = [overwrite for overwrite in before.overwrites if overwrite not in after.overwrites]

        # Get the moderator who did the modification
        moderator = after.guild.get_member(after.guild.owner_id)

        # Log permission changes in a specific channel
        channel_id = 1284184011085713420  # Replace with the ID of your desired channel
        channel = bot.get_channel(channel_id)
        if channel:
            for overwrite in added_overwrites:
                embed = discord.Embed(title="Permission Changes", color=discord.Color.green())
                embed.add_field(name="Permission Added",
                                value=f"{moderator.mention} added permission {overwrite[0].mention} for {overwrite[1].mention} in {after.mention}",
                                inline=False)
                await channel.send(embed=embed)
                myLogger.info(f"Sent: Channel perms updated (adding perms)")

            for overwrite in removed_overwrites:
                embed = discord.Embed(title="Permission Changes", color=discord.Color.red())
                embed.add_field(name="Permission Removed",
                                value=f"{moderator.mention} removed permission {overwrite[0].mention} for {overwrite[1].mention} in {after.mention}",
                                inline=False)
                await channel.send(embed=embed)
                myLogger.info(f"Sent: channel perms updated (removing perms)")



@bot.event
async def on_guild_channel_create(channel):
    # Get the moderator who created the channel
    async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
        moderator = entry.user
        break  # Only need the latest channel creation entry

    # Log channel creation in a specific channel
    channel_id = 1284184011085713420  # Replace with the ID of your desired channel
    log_channel = bot.get_channel(channel_id)

    if log_channel:
        embed = discord.Embed(title="Channel Changes", color=discord.Color.green())
        embed.add_field(name="Channel Created", value=f"{moderator.mention} created channel '{channel.name}'",
                        inline=False)
        await log_channel.send(embed=embed)
        myLogger.info(f"Sent: {channel.name} (channel) created")



@bot.event
async def on_guild_channel_delete(channel):
    # Get the moderator who deleted the channel
    async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
        moderator = entry.user
        break  # Only need the latest channel deletion entry

    # Log channel deletion in a specific channel
    channel_id = 1284184011085713420  # Replace with the ID of your desired channel
    log_channel = bot.get_channel(channel_id)

    if log_channel:
        embed = discord.Embed(title="Channel Changes", color=discord.Color.red())
        embed.add_field(name="Channel Deleted", value=f"{moderator.mention} deleted channel '{channel.name}'",
                        inline=False)
        await log_channel.send(embed=embed)
        myLogger.info(f"Sent: {channel.name} (channel) deleted")



@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        # Determine the role changes (added or removed roles)
        added_roles = [role for role in after.roles if role not in before.roles and str(role)]
        removed_roles = [role for role in before.roles if role not in after.roles and str(role)]

        # Get the moderator who did the modification
        moderator = after.guild.get_member(after.guild.owner_id)

        # Log role changes in a specific channel
        channel_id = 1284184011085713420  # Replace with the ID of your desired channel
        channel = bot.get_channel(channel_id)
        if channel:
            if added_roles:
                for role in added_roles:
                    embed = discord.Embed(title="Role Changes", color=discord.Color.green())
                    embed.add_field(name="Role Added",
                                    value=f"{moderator.mention} added role {role.mention} to {after.mention}",
                                    inline=False)
                    myLogger.info(f"Sent: {role.mention} (role) created")
            if removed_roles:
                for role in removed_roles:
                    embed = discord.Embed(title="Role Changes", color=discord.Color.red())
                    embed.add_field(name="Role Removed",
                                    value=f"{moderator.mention} removed role {role.mention} from {after.mention}",
                                    inline=False)
                    myLogger.info(f"Sent: {role.mention} (role) removed")
            await channel.send(embed=embed)
                


@bot.event  # Note: Remove parentheses here
async def on_guild_role_create(role):
    # Get the moderator who created the role
    moderator = role.guild.get_member(role.guild.owner_id)

    # Log role creation in a specific channel
    channel_id = 1284184011085713420  # Replace with the ID of your desired channel
    channel = bot.get_channel(channel_id)
    if channel:
        embed = discord.Embed(title="Role Changes", color=discord.Color.green())
        embed.add_field(name="Role Created", value=f"{moderator.mention} created role {role.mention}", inline=False)
        await channel.send(embed=embed)
        myLogger.info(f"Sent: {role.mention} (role) created")



@bot.event  # Note: Remove parentheses here
async def on_guild_role_delete(role):
    moderator = role.guild.get_member(role.guild.owner_id)
    channel_id = 1284184011085713420
    channel = bot.get_channel(channel_id)

    if channel:
        embed = discord.Embed(title="Role Changes", color=discord.Color.red())
        embed.add_field(name="Role Deleted", value=f"{moderator.mention} deleted role '{role.name}'", inline=False)
        await channel.send(embed=embed)
        myLogger.info(f"Sent: {role.mention} (role) removed")






def get_level_and_remaining_exp(xp):
    """
    Calculates the level, remaining XP for the current level, 
    and the XP required for the next level based on the increasing XP requirement.
    
    :param xp: The current XP of the user.
    :return: A tuple containing the user's level, the remaining XP, and XP needed for the next level.
    """
    if xp == 999999:  # Check for infinite XP case
        return "infinite", "infinite", "infinite"

    level = 1
    total_xp_for_next_level = 50  # Initial XP required for level 2
    total_xp_for_current_level = 0

    # Determine current level and remaining XP for the next level
    while xp >= total_xp_for_next_level:
        level += 1
        total_xp_for_current_level = total_xp_for_next_level
        total_xp_for_next_level += 50 + (level - 1) * 3  # XP for next level increases by 3 per level

    # Calculate remaining XP and XP needed for the next level
    remaining_xp = xp - total_xp_for_current_level
    xp_for_next_level = total_xp_for_next_level - total_xp_for_current_level

    return level, remaining_xp, xp_for_next_level





@bot.tree.command(name="init", description="Starts up the leveling system if it hasn't already.")
async def init(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator or interaction.user.id == ENABLED_USER_ID:
        cur.execute(
            f'''CREATE TABLE IF NOT EXISTS GUILD_{interaction.guild.id} (user_id int NOT NULL, exp int DEFAULT 0, lvl int DEFAULT 0)''')

        for member in interaction.guild.members:
            if not member.bot:
                cur.execute(f"INSERT INTO GUILD_{interaction.guild.id} (user_id) VALUES ({member.id})")

        con.commit()
        await interaction.response.send_message("Leveling system initialized")
    else:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)



@bot.tree.command(name="editxp", description="Edit a user's XP. Use 'reset' to reset, or 'infinite' for infinite XP.")
@app_commands.describe(user="The user whose XP to edit", amount="The XP amount to add, 'reset' to reset, or 'infinite' for infinite XP")
async def editxp(interaction: discord.Interaction, user: discord.Member, amount: str):
    if interaction.user.guild_permissions.administrator or interaction.user.id == ENABLED_USER_ID:
        try:
            cur.execute(f"SELECT * FROM GUILD_{interaction.guild.id} WHERE user_id={user.id}")
            result = cur.fetchone()

            if result:
                if amount == "reset":
                    new_exp = 0
                elif amount == "infinite":
                    new_exp = 999999  # Use a large number to denote infinite XP
                else:
                    new_exp = max(0, result[1] + int(amount))  # Ensure the new XP is non-negative

                # Use get_level_and_remaining_exp to calculate old and new levels
                old_level, remaining_exp_old, next_level_exp_old = get_level_and_remaining_exp(result[1])
                new_level, remaining_exp_new, next_level_exp_new = get_level_and_remaining_exp(new_exp)

                cur.execute(f"UPDATE GUILD_{interaction.guild.id} SET exp={new_exp} WHERE user_id={user.id}")
                con.commit()

                # Create an embedded message to show changes
                embed = discord.Embed(title="XP and Level Change", color=discord.Color.gold())
                embed.set_thumbnail(url=user.avatar.url)
                embed.add_field(name="User", value=user.mention, inline=False)
                embed.add_field(name="Old XP", value=f"{remaining_exp_old}/{next_level_exp_old} (Level {old_level})", inline=False)
                embed.add_field(name="New XP", value=f"{remaining_exp_new}/{next_level_exp_new} (Level {new_level})", inline=False)

                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("User not found in the database.")
        except sqlite3.OperationalError as e:
            await interaction.response.send_message("Database error occurred.")
            myLogger.error(f"SQLite Error: {e}")
    else:
        await interaction.response.send_message("You do not have permission to use this command.")







@bot.tree.command(name="xp", description="Shows the specified user's experience and levels.")
@app_commands.describe(user="The user whose XP you want to check. Leave blank for yourself.")
async def xp(interaction: discord.Interaction, user: discord.User = None):
    try:
        if user is None:
            user = interaction.user

        cur.execute(f"SELECT * FROM GUILD_{interaction.guild.id} WHERE user_id={user.id}")
        result = cur.fetchone()

        if result is not None:
            exp = result[1]
            if exp == 999999:
                level = "infinite"
                remaining_exp = "infinite"
                next_level_exp = "infinite"
            else:
                level, remaining_exp, next_level_exp = get_level_and_remaining_exp(exp)

            embed = discord.Embed(title=f"{user.display_name}", color=discord.Color.green())
            embed.set_thumbnail(url=user.avatar.url)
            embed.add_field(name="XP", value=f"{remaining_exp}/{next_level_exp} XP" if exp != 999999 else "infinite", inline=True)
            embed.add_field(name="Level", value=level, inline=True)

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Hmm no such user in the database")
    except sqlite3.OperationalError:
        await interaction.response.send_message("Database not initialized")







@bot.tree.command(name="leaderboard", description="Shows the top 5 highest level people in the server.")
async def leaderboard(interaction: discord.Interaction):
    try:
        cur.execute(f"""
            SELECT DISTINCT user_id, exp
            FROM GUILD_{interaction.guild.id}
            ORDER BY CASE WHEN exp = 999999 THEN 1 ELSE 0 END DESC, exp DESC
            LIMIT 5;
        """)
        results = cur.fetchall()

        # Log results for debugging
        myLogger.info(f"Leaderboard Query Results: {results}")

        if results:
            embed = discord.Embed(title="Leaderboard", color=discord.Color.blue())

            for index, (user_id, exp) in enumerate(results, start=1):
                try:
                    user = await interaction.guild.fetch_member(user_id)
                    if exp == 999999:
                        level_display = "infinite"
                        exp_display = "infinite"
                    else:
                        level, remaining_exp, next_level_exp = get_level_and_remaining_exp(exp)
                        level_display = level
                        exp_display = f"{remaining_exp} / {next_level_exp}"

                    embed.add_field(
                        name=f"{index}. {user.display_name}",
                        value=f"    XP: {exp_display} \n    Level: {level_display}",
                        inline=False
                    )
                except discord.NotFound:
                    embed.add_field(
                        name=f"{index}. [User not found]",
                        value=f"    XP: {'infinite' if exp == 999999 else exp} \n    Level: {'infinite' if exp == 999999 else 'Unknown'}",
                        inline=False
                    )
                except Exception as e:
                    myLogger.error(f"Error fetching user {user_id}: {e}")
                    embed.add_field(
                        name=f"{index}. [Error]",
                        value=f"An error occurred while fetching the user.",
                        inline=False
                    )

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No users found in the database.")
    except sqlite3.OperationalError:
        await interaction.response.send_message("Database not initialized.")
    except Exception as e:
        myLogger.error(f"An error has occurred: {e}")









@bot.tree.command(name="change_name", description="Change the nickname of a user.")
@app_commands.describe(user="The user to change the nickname of", nickname="The new nickname")
async def change_name(interaction: discord.Interaction, user: discord.User, nickname: str):
    # Check if the user is an administrator or matches the ENABLED_USER_ID
    if interaction.user.guild_permissions.administrator or interaction.user.id == ENABLED_USER_ID:
        # Convert discord.User to discord.Member by finding the user in the guild
        member = interaction.guild.get_member(user.id)

        if member:
            try:
                # Attempt to change the member's nickname
                await member.edit(nick=nickname)
                await interaction.response.send_message(f"Changed nickname of {member.mention} to {nickname}", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("I don't have permission to change this user's nickname.", ephemeral=True)
            except discord.HTTPException:
                await interaction.response.send_message("An error occurred while trying to change the nickname.", ephemeral=True)
        else:
            await interaction.response.send_message(f"User '{user}' is not a member of this guild.", ephemeral=True)
    else:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)



@bot.tree.command(name="remove_name", description="Remove a nickname from a user.")
@app_commands.describe(user="The user to remove the nickname from")
async def remove_nickname(interaction: discord.Interaction, user: discord.User):
    if interaction.user.guild_permissions.administrator or interaction.user.id == ENABLED_USER_ID:
        member = discord.utils.get(interaction.guild.members, id=user.id)
        if member:
            await member.edit(nick=None)
            await interaction.response.send_message(f"Removed nickname of {member.mention}")
        else:
            await interaction.response.send_message(f"User '{user}' does not exist.", ephemeral=True)
    else:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)



@bot.tree.command(name="purge", description="Delete a specified number of messages in a channel.")
@app_commands.describe(amount="The number of messages to delete", channel="The channel to delete messages from (optional)")
async def purge(interaction: discord.Interaction, amount: int, channel: discord.TextChannel = None):
    if interaction.user.guild_permissions.administrator or interaction.user.id == ENABLED_USER_ID:
        # Determine the channel to use
        target_channel = channel if channel else interaction.channel
        
        await interaction.response.send_message(f"Deleting messages in {target_channel.mention}... 0/{amount} messages deleted so far.", ephemeral=True)

        # Fetch messages to delete
        messages_to_delete = []
        async for message in target_channel.history(limit=amount):
            messages_to_delete.append(message)

        # Delete the messages
        await target_channel.delete_messages(messages_to_delete)
        await interaction.edit_original_response(content=f"Deleted {len(messages_to_delete)} out of {amount} messages in {target_channel.mention}.")
    else:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)



@bot.tree.command(name="depression", description="Adds the 'depressed' role to the user.")
async def depression(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, name='depressed')
    if role is None:
        role = await interaction.guild.create_role(name='depressed', color=discord.Color.dark_gray())
        await interaction.response.send_message(f"Created '{role}' role.")
    
    if str(interaction.user) == "kefayt_":
        role2 = discord.utils.get(interaction.guild.roles, name='depressed-king')
        if role2 is None:
            role2 = await interaction.guild.create_role(name='depressed-king', color=discord.Color.dark_gray())
            await interaction.response.send_message(f"Created '{role2}' role.")
        await interaction.response.send_message("You can't make a depressed person depressed.")
    else:
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"Role '{role}' added to you!")



@bot.tree.command(name="search", description="Search for available commands.")
@app_commands.describe(command_name="The name of the command to search for")
async def search_command(interaction: discord.Interaction, command_name: str):
    command_names = [cmd.name for cmd in bot.tree.get_commands()]
    if command_name in command_names:
        command = bot.tree.get_command(command_name)
        if command:
            command_help = command.description if command.description else "No help information available."
            embed = discord.Embed(title=f"Command: {command_name}", description=f"**Help:**\n{command_help}",
                                  color=discord.Color.blue())
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"The command **{command_name}** is available.")
    else:
        await interaction.response.send_message(f"The command **{command_name}** is not available.")



# Error handling for interactions
@bot.event
async def on_application_command_error(interaction: discord.Interaction, error: Exception):
    if isinstance(error, commands.CommandNotFound):
        await interaction.response.send_message("That command does not exist.", ephemeral=True)

    elif isinstance(error, commands.MissingRequiredArgument):
        await interaction.response.send_message("Missing required arguments.", ephemeral=True)

    elif isinstance(error, commands.BadArgument):
        await interaction.response.send_message("Bad argument provided.", ephemeral=True)

    elif isinstance(error, commands.CommandOnCooldown):
        await interaction.response.send_message(f"This command is on cooldown. Try again in {round(error.retry_after)} seconds.", ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("You don't have the necessary permissions to run this command.", ephemeral=True)

    elif isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message("The bot doesn't have the necessary permissions to execute this command.", ephemeral=True)

    elif isinstance(error, commands.DisabledCommand):
        await interaction.response.send_message("This command is currently disabled.", ephemeral=True)

    elif isinstance(error, commands.NoPrivateMessage):
        await interaction.response.send_message("This command cannot be used in private messages.", ephemeral=True)

    elif isinstance(error, commands.CheckFailure):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

    elif isinstance(error, commands.CommandInvokeError):
        await interaction.response.send_message("An error occurred while executing the command.", ephemeral=True)
        myLogger.error(f'An error occurred during command execution: {error}')

    else:
        myLogger.error(f'An unexpected error occurred: {error}')



# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("That command does not exist.")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("Missing required arguments.")

    elif isinstance(error, commands.BadArgument):
        await ctx.reply("Bad argument provided.")

    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(f"This command is on cooldown. Try again in {round(error.retry_after)} seconds.")

    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply("You don't have the necessary permissions to run this command.")

    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.reply("The bot doesn't have the necessary permissions to execute this command.")

    elif isinstance(error, commands.DisabledCommand):
        await ctx.reply("This command is currently disabled.")

    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.reply("This command cannot be used in private messages.")

    elif isinstance(error, commands.CheckFailure):
        await ctx.reply("You do not have permission to use this command.")

    elif isinstance(error, commands.CommandInvokeError):
        await ctx.reply("An error occurred while executing the command.")
        # Log the original exception
        original_error = getattr(error, "original", error)
        myLogger.info('An error occurred during command execution:', file=sys.stderr)
        traceback.myLogger.info_exception(type(error), error, error.__traceback__, file=sys.stderr)

    else:
        myLogger.error(f'An error occurred during command execution: {error}')



if __name__ == '__main__':
    # Run the bot
    load_dotenv()
    TOKEN = os.getenv('ENVDISCORD_TOKEN')
    bot.run(TOKEN)