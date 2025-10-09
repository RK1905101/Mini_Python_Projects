import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import yt_dlp
import asyncio
from collections import deque
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
keep_alive()

SONG_QUEUES = {}

async def search_ytdlp_async(query, ydl_opts):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: _extract(query, ydl_opts))

def _extract(query, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(query, download=False)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} has connected to Discord!")

@bot.tree.command(name="play", description="Play a song or add it to the queue")
@app_commands.describe(song_query="Search query")
async def play(interaction: discord.Interaction, song_query: str):
    await interaction.response.defer()

    voice_channel = interaction.user.voice.channel
    if voice_channel is None:
        await interaction.followup.send("Please connect to a voice channel")
        return

    voice_client = interaction.guild.voice_client
    if voice_client is None:
        voice_client = await voice_channel.connect()
    elif voice_channel != voice_client.channel:
        await voice_client.move_to(voice_channel)

    ydl_opts = {
        'format': 'bestaudio[abr<=96]/bestaudio',
        "noplaylist": True,
        "youtube_include_dash_manifest": False,
        "youtube_include_hls_manifest": False,
        "cookies" : os.path.join(os.getcwd(), 'cookies.txt'),
        "quiet" : True,
        "no_warnings" : True,
    }

    query = "ytsearch1: " + song_query
    result = await search_ytdlp_async(query, ydl_opts)
    tracks = result.get('entries', [])

    if tracks is None:
        await interaction.followup.send("No songs found")
        return

    first_track = tracks[0]
    webpage_url = first_track['webpage_url']
    title = first_track.get('title', "Untitled")

    guild_id = str(interaction.guild_id)
    if SONG_QUEUES.get(guild_id) is None:
       SONG_QUEUES[guild_id] = deque()

    SONG_QUEUES[guild_id].append((webpage_url, title))

    if voice_client.is_playing() or voice_client.is_paused():
        await interaction.followup.send(f"Added to the queue: **{title}**")
    else:
        await interaction.edit_original_response(content=f"Now playing: **{title}**")
        await play_next_song(voice_client, guild_id, interaction.channel)

@bot.tree.command(name="skip", description="Skips the current song")
async def skip(interaction: discord.Interaction):
    if interaction.guild.voice_client and (interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused()):
        interaction.guild.voice_client.stop()
        await interaction.response.send_message("Skipped to the next song!!")
    else:
        await interaction.response.send_message("Not playing anything to skip!")

@bot.tree.command(name="pause", description="Pauses the current playing song")
async def pause(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client

    if voice_client is None:
        return await interaction.response.send_message("I'm not in a voice channel")

    if not voice_client.is_playing():
        return await interaction.response.send_message("Nothing is playing currently")

    voice_client.pause()
    await interaction.response.send_message("Paused")
    return None

@bot.tree.command(name="resume", description="Resumes the current playing song")
async def resume(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client

    if voice_client is None:
        return await interaction.response.send_message("I'm not in a voice channel")

    if not voice_client.is_paused():
        return await interaction.response.send_message("I'm not paused right now")

    voice_client.resume()
    await interaction.response.send_message("Resumed")
    return None

@bot.tree.command(name="stop", description="Stops the current playing song")
async def stop(interaction: discord.Interaction):
    await interaction.response.defer()
    voice_client = interaction.guild.voice_client

    if not voice_client or not voice_client.is_connected():
        await interaction.followup.send("I'm not connected to any voice channel")
        return None

    guild_id = str(interaction.guild_id)
    if guild_id in SONG_QUEUES:
        SONG_QUEUES[guild_id].clear()

    if voice_client.is_playing() or voice_client.is_paused():
        voice_client.stop()

    await interaction.followup.send("Stopped the playback and disconnected")

    await voice_client.disconnect()
    return None

async def play_next_song(voice_client, guild_id, channel):
    if not SONG_QUEUES[guild_id]:
        await voice_client.disconnect()
        SONG_QUEUES[guild_id] = deque()
        return

    webpage_url, title = SONG_QUEUES[guild_id].popleft()

    ydl_opts = {
        'format': 'bestaudio[abr<=96]/bestaudio',
        "noplaylist": True,
        "cookies": os.path.join(os.getcwd(), 'cookies.txt')
    }

    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, lambda: _extract(webpage_url, ydl_opts))

    if not result:
        await channel.send(f"Failed to fetch audio for **{title}**. Skipping.")
        await play_next_song(voice_client, guild_id, channel)
        return

    audio_url = result['url']

    ffmpeg_opts = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn -c:a libopus -b:a 96k",
    }

    source = discord.FFmpegOpusAudio(audio_url, **ffmpeg_opts, executable="bin\\ffmpeg\\ffmpeg.exe")

    def after_play(error):
        if error:
            print(f"Error playing {title}: {error}")
        asyncio.run_coroutine_threadsafe(play_next_song(voice_client, guild_id, channel), bot.loop)

    voice_client.play(source, after=after_play)
    await channel.send(f"Now playing: **{title}**")

bot.run(TOKEN)