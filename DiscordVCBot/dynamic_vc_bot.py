import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import asyncio
import json
import os
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

# Bot configuration
class DynamicVCBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.voice_states = True
        intents.guilds = True
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

        # Initialize database
        self.init_database()

        # Store temporary channels and their data
        self.temp_channels = {}  # {temp_channel_id: {'hub_id': hub_id, 'creator_id': user_id}}

    def init_database(self):
        self.conn = sqlite3.connect('dynamic_vc_bot.db')
        self.cursor = self.conn.cursor()

        # Create table for VC hubs if not exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vc_hubs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                channel_id INTEGER NOT NULL UNIQUE,
                user_limit INTEGER DEFAULT NULL,
                channel_limit INTEGER DEFAULT NULL,         -- NEW
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Alter table if missing channel_limit column
        try:
            self.cursor.execute("ALTER TABLE vc_hubs ADD COLUMN channel_limit INTEGER DEFAULT NULL")
        except sqlite3.OperationalError:
            pass  # Column already exists

        # temp_channels table unchanged
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS temp_channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id INTEGER NOT NULL UNIQUE,
                hub_id INTEGER NOT NULL,
                creator_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (hub_id) REFERENCES vc_hubs (channel_id)
            )
        """)

        self.conn.commit()

    async def setup_hook(self):
        """Setup hook called when bot starts"""
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}")

    def is_vc_hub(self, channel_id: int) -> Optional[tuple]:
        self.cursor.execute("SELECT channel_id, user_limit, channel_limit FROM vc_hubs WHERE channel_id = ?", (channel_id,))
        result = self.cursor.fetchone()
        return result if result else None

    def add_temp_channel(self, temp_channel_id: int, hub_id: int, creator_id: int):
        """Add temporary channel to database"""
        self.cursor.execute(
            "INSERT OR REPLACE INTO temp_channels (channel_id, hub_id, creator_id) VALUES (?, ?, ?)",
            (temp_channel_id, hub_id, creator_id)
        )
        self.conn.commit()
        self.temp_channels[temp_channel_id] = {'hub_id': hub_id, 'creator_id': creator_id}

    def remove_temp_channel(self, temp_channel_id: int):
        """Remove temporary channel from database"""
        self.cursor.execute("DELETE FROM temp_channels WHERE channel_id = ?", (temp_channel_id,))
        self.conn.commit()
        if temp_channel_id in self.temp_channels:
            del self.temp_channels[temp_channel_id]

    def is_temp_channel(self, channel_id: int) -> bool:
        """Check if a channel is a temporary channel"""
        return channel_id in self.temp_channels

    async def close(self):
        """Close database connection when bot shuts down"""
        self.conn.close()
        await super().close()

bot = DynamicVCBot()

@bot.event
async def on_ready():
    """Event triggered when bot is ready"""
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')

    # Load existing temporary channels from database
    bot.cursor.execute("SELECT channel_id, hub_id, creator_id FROM temp_channels")
    for temp_channel_id, hub_id, creator_id in bot.cursor.fetchall():
        bot.temp_channels[temp_channel_id] = {'hub_id': hub_id, 'creator_id': creator_id}

    print(f'Loaded {len(bot.temp_channels)} temporary channels from database')

@bot.event
async def on_voice_state_update(member, before, after):
    """Handle voice state changes - main logic for dynamic VC creation/deletion"""

    # User joined a channel
    if after.channel and after.channel.id != getattr(before.channel, 'id', None):
        hub_data = bot.is_vc_hub(after.channel.id)

        if hub_data:
            hub_channel_id, user_limit, channel_limit = hub_data

            # Count existing temp channels for this hub
            bot.cursor.execute("SELECT COUNT(*) FROM temp_channels WHERE hub_id = ?", (hub_channel_id,))
            current_count = bot.cursor.fetchone()[0]

            if channel_limit is not None and current_count >= channel_limit:
                # Optional: send a message if you want to notify user
                try:
                    if member.guild.system_channel:
                        await member.guild.system_channel.send(
                            f"⚠ {after.channel.name} has reached its sub-channel limit ({channel_limit})."
                        )
                except Exception:
                    pass  # Ignore if we cannot send message
                print(f"⚠ Hub {after.channel.name} reached its sub-channel limit ({channel_limit}).")
                return  # Stop here — don't create another sub-channel

            try:
                # Create temporary voice channel in the same category as the hub
                category = after.channel.category

                # Use new naming format: "{Hub Name}: Sub VC"
                temp_channel_name = f"{after.channel.name}: Sub VC"

                # Create the temporary channel
                overwrites = after.channel.overwrites
                temp_channel = await after.channel.guild.create_voice_channel(
                    name=temp_channel_name,
                    category=category,
                    user_limit=user_limit,
                    overwrites=overwrites
                )

                # Move the user to the temporary channel
                await member.move_to(temp_channel)

                # Add to tracking
                bot.add_temp_channel(temp_channel.id, hub_channel_id, member.id)

                print(f"✅ Created temporary channel '{temp_channel_name}' for {member.display_name}")

            except discord.errors.Forbidden:
                print(f"❌ Missing permissions to create voice channel in {after.channel.guild.name}")
            except Exception as e:
                print(f"❌ Error creating temporary channel: {e}")

    # User left a channel — handle deletion of temporary channels when empty
    if before.channel and bot.is_temp_channel(before.channel.id):
        if len(before.channel.members) == 0:
            try:
                temp_channel_name = before.channel.name
                await before.channel.delete(reason="Temporary channel empty")

                # Remove from tracking
                bot.remove_temp_channel(before.channel.id)

                print(f"🗑 Deleted empty temporary channel '{temp_channel_name}'")

            except discord.errors.NotFound:
                # Channel was already deleted — ensure DB/ref cleaned up
                bot.remove_temp_channel(before.channel.id)
            except Exception as e:
                print(f"❌ Error deleting temporary channel: {e}")

# Slash Commands
@bot.tree.command(name="add-vc-hub", description="Add a voice channel as a VC hub")
@app_commands.describe(
    channel="The voice channel to make into a VC hub",
    limit="User limit for created temporary channels (optional)",
    channel_limit="Maximum number of sub-channels that can be created from this hub (optional)"
)
async def add_vc_hub(
    interaction: discord.Interaction,
    channel: discord.VoiceChannel,
    limit: Optional[int] = None,
    channel_limit: Optional[int] = None
):
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message("❌ You need 'Manage Channels' permission to use this command.", ephemeral=True)
        return

    if limit is not None and (limit < 1 or limit > 99):
        await interaction.response.send_message("❌ User limit must be between 1 and 99.", ephemeral=True)
        return

    if channel_limit is not None and channel_limit < 1:
        await interaction.response.send_message("❌ Channel limit must be at least 1.", ephemeral=True)
        return

    try:
        if bot.is_vc_hub(channel.id):
            await interaction.response.send_message(f"❌ {channel.name} is already a VC hub.", ephemeral=True)
            return

        bot.cursor.execute(
            "INSERT INTO vc_hubs (guild_id, channel_id, user_limit, channel_limit) VALUES (?, ?, ?, ?)",
            (interaction.guild.id, channel.id, limit, channel_limit)
        )
        bot.conn.commit()

        await interaction.response.send_message(
            f"✅ Added {channel.name} as a VC hub"
            + (f" (VC user limit: {limit})" if limit else "")
            + (f" (Sub-channel limit: {channel_limit})" if channel_limit else "")
        )

    except Exception as e:
        await interaction.response.send_message(f"❌ Error adding VC hub: {e}", ephemeral=True)


@bot.tree.command(name="remove-vc-hub", description="Remove a VC hub")
@app_commands.describe(channel="The voice channel to remove from VC hubs")
async def remove_vc_hub(interaction: discord.Interaction, channel: discord.VoiceChannel):
    """Remove a voice channel from VC hubs"""

    # Check if user has manage channels permission
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message("❌ You need 'Manage Channels' permission to use this command.", ephemeral=True)
        return

    try:
        # Check if channel is a VC hub
        if not bot.is_vc_hub(channel.id):
            await interaction.response.send_message(f"❌ {channel.name} is not a VC hub.", ephemeral=True)
            return

        # Remove from database
        bot.cursor.execute("DELETE FROM vc_hubs WHERE channel_id = ?", (channel.id,))
        bot.conn.commit()

        if bot.cursor.rowcount > 0:
            await interaction.response.send_message(f"✅ Removed {channel.name} from VC hubs")
        else:
            await interaction.response.send_message(f"❌ {channel.name} was not found in VC hubs.", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(f"❌ Error removing VC hub: {e}", ephemeral=True)

@bot.tree.command(name="list-vc-hubs", description="List all VC hubs in this server")
async def list_vc_hubs(interaction: discord.Interaction):
    """List all VC hubs in the current server"""

    try:
        # Get all VC hubs for this guild
        bot.cursor.execute(
            "SELECT channel_id, user_limit FROM vc_hubs WHERE guild_id = ?",
            (interaction.guild.id,)
        )
        hubs = bot.cursor.fetchall()

        if not hubs:
            await interaction.response.send_message("❗ No VC hubs configured in this server.", ephemeral=True)
            return

        # Build embed
        embed = discord.Embed(
            title="🎙️ VC Hubs",
            description="Voice channels that create temporary channels",
            color=discord.Color.blue()
        )

        for channel_id, user_limit in hubs:
            channel = interaction.guild.get_channel(channel_id)
            if channel:
                limit_text = f" (limit: {user_limit})" if user_limit else " (no limit)"
                embed.add_field(
                    name=f"#{channel.name}",
                    value=f"ID: {channel_id}{limit_text}",
                    inline=False
                )
            else:
                embed.add_field(
                    name=f"Deleted Channel",
                    value=f"ID: {channel_id} (channel no longer exists)",
                    inline=False
                )

        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message(f"❌ Error listing VC hubs: {e}", ephemeral=True)

@bot.tree.command(name="help", description="Show a list of all available commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📜 Borgir Utilities - Help Menu",
        description="Here’s a list of all available commands and what they do:",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="/add-vc-hub `channel:` `limit:` `channel_limit:`",
        value="Make a voice channel into a VC hub. When someone joins the hub, a sub‑VC is created. "
              "`limit` sets sub‑VC user limit, `channel_limit` sets max number of sub‑VCs from the hub.",
        inline=False
    )
    embed.add_field(
        name="/remove-vc-hub `channel:`",
        value="Remove a channel from being a VC hub.",
        inline=False
    )
    embed.add_field(
        name="/list-vc-hubs",
        value="List all configured VC hubs in this server.",
        inline=False
    )
    embed.add_field(
        name="/help",
        value="Display this help menu.",
        inline=False
    )

    embed.set_footer(text="⚡ Borgir Utilities Bot • Dynamic Voice Channels & Utilities")

    await interaction.response.send_message(embed=embed, ephemeral=True)

# Error handling for commands
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """Handle slash command errors"""
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
    elif isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"❌ Command is on cooldown. Try again in {error.retry_after:.2f} seconds.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ An error occurred while processing the command.", ephemeral=True)
        print(f"Command error: {error}")

# Run the bot
if __name__ == "__main__":
    # Load token from environment variable or config file
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')

    if not TOKEN:
        # Try to load from config.json
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                TOKEN = config.get('token')
        except FileNotFoundError:
            print("Error: No token found. Set DISCORD_BOT_TOKEN environment variable or create config.json")
            exit(1)

    if not TOKEN:
        print("Error: No bot token provided")
        exit(1)

    bot.run(TOKEN)