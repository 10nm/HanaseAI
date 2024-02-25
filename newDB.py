import discord
from llama_cpp import Llama
from pydub import AudioSegment
import os
import time
from faster_whisper import WhisperModel

# Llama
llm = Llama(
    model_path = "../models/gguf/calm2-7b-chat-q4-k-s.gguf", n_gpu_layers=20,
    
)

# Whisper
model_size = "small"
wm=WhisperModel(model_size, device="cuda", compute_type="float16")


# Discord
GID = os.environ.get("GID")
GENBA = os.environ.get("GENBA")
BOTSC = os.environ.get("BOTSC")

intents = discord.Intents.all() 
bot = discord.Bot(intents=intents)

async def transcribe(user_id):
    audiopath = f"./{user_id}.mp3"
    result, info = wm.transcribe(audiopath, beam_size=1, language="ja")
    results = ""
    for segment in result:
        results += segment.text
    return results

# ChatLLM
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    elif message.channel.id == GENBA or message.channel.id == BOTSC:
        prompt = message.content
        print('Message from {0.author}: {0.content}'.format(message))
        start = time.time()
        msg = await nlp(prompt)
        end = time.time()
        t = round(end - start, 2)
        if msg != None:
            await message.channel.send(f"=>> CHAT {t}s **仮想友人**: {msg}")
    else:
        return

async def nlp(msg):
    if len(msg) <= 0:
        return
    else:
        response= llm(f"""### ユーザー: {msg} 
### アシスタント:""",max_tokens=100, stop=["###","ユーザー","アシスタント","\n"])
        if response['choices'][0]['text'] == 0:
            return "応答なし"
        else:
            return response['choices'][0]['text']

## Voice
@bot.slash_command(guild_ids=[GID])
async def rc(ctx:discord.ApplicationContext):
    try:
        await ctx.author.voice.channel.connect()
        await ctx.respond("started recording")

    except AttributeError:
        await ctx.respond("You are not in a voice channel")
        return

    ctx.author.voice.channel.voice_states
    
    ctx.voice_client.start_recording(
        discord.sinks.MP3Sink(), finished_callback, ctx
    )

async def finished_callback(sink:discord.sinks.MP3Sink, ctx:discord.ApplicationContext):
    print(list(sink.audio_data.items()))
    for user_id, audio in sink.audio_data.items():
        ad = AudioSegment.from_file(audio.file, format="mp3")
        ad.export(f"./{user_id}.mp3", format='mp3')
        username = bot.get_user(int(user_id))
        start = time.time()
        result = await transcribe(user_id)
        end = time.time()
        t = round(end - start, 2)
        if result != None:
            print(f"Transcription time: {end - start}")
            await ctx.channel.send(f"=>> VOICE {t}s **{username}**: {result}")
            start = time.time()
            chats = await nlp(result)
            end = time.time()
            t = round(end - start, 2)
            if chats != None:
                print(f"Chat time: {t}s")
                await ctx.channel.send(f"=>> VOICE {t}s: **仮想友人**: {chats}")


@bot.slash_command(guild_ids=[GID])
async def dc(ctx:discord.ApplicationContext):
    ctx.voice_client.stop_recording()
    try:
        await ctx.voice_client.disconnect()
        await ctx.respond("Disconnected from voice channel")
    except AttributeError:
        await ctx.respond("I'm not in a voice channel")
        return

token = os.environ.get("TOKEN")
bot.run(token)