import discord
from discord.ext import commands
import youtube_dl

TOKEN = 'Token'
PREFIX = '!'  # Prefixo para comandos do bot
BOT_ID = "BOT_ID"

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Bot está conectado como {bot.user}')

@bot.command()
async def join(ctx):
    # Verifica se o autor do comando está em um canal de voz
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Você precisa estar em um canal de voz para me chamar!")

@bot.command()
async def leave(ctx):
    # Verifica se o bot está em um canal de voz
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Eu não estou em um canal de voz.")

@bot.command()
async def play(ctx, *, query):
    # Verifica se o bot está em um canal de voz
    if not ctx.voice_client:
        await ctx.send("Eu não estou em um canal de voz. Use o comando !join primeiro.")
        return

    # Configura o youtube_dl para buscar a melhor qualidade de áudio
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # Extrai informações do vídeo do YouTube usando youtube_dl
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        url = info['formats'][0]['url']

    # Conecta-se ao canal de voz e reproduz a música
    voice_client = ctx.voice_client
    voice_client.stop()
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }
    voice_client.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
    await ctx.send(f"Tocando: {info['title']}")

@bot.command()
async def stop(ctx):
    # Verifica se o bot está em um canal de voz e para a reprodução
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Reprodução interrompida.")

@bot.command()
async def pause(ctx):
    # Verifica se o bot está em um canal de voz e pausa a reprodução
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Reprodução pausada.")

@bot.command()
async def resume(ctx):
    # Verifica se o bot está em um canal de voz e retoma a reprodução
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Reprodução retomada.")

bot.run(TOKEN)