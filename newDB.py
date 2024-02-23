import discord
from llama_cpp import Llama
from pydub import AudioSegment
import os
from faster_whisper import WhisperModel

# # Llama
# llm = Llama(
#     model_path = "../models/gguf/calm2-7b-chat-q5km.gguf", n_gpu_layers=-1
# )

# Whisper
model_size = "medium"
model=WhisperModel(model_size, device="cuda", compute_type="float16")


# Discord
GID = 1204383625865465886
GENBA = 1205840329849176084
BOTSC = 1205072146288607262

intents = discord.Intents.all() 
bot = discord.Bot(intents=intents)

# # ChatLLM
# @bot.event
# async def on_message(message):
#     if message.author.bot:
#         return
    
#     elif message.channel.id == GENBA or message.channel.id == BOTSC:
#         prompt = message.content
#         print('Message from {0.author}: {0.content}'.format(message))
#         msg = await nlp(prompt)
#         if msg != None:
#             await message.channel.send(msg)
#     else:
#         return

# async def nlp(msg):
#     if len(msg) <= 3:
#         return
#     else:
#         response= llm(f"""### ユーザー: {msg} 
# ### アシスタント:""",max_tokens=50, stop=["###","ユーザー","アシスタント"])
#         if response['choices'][0]['text'] == 0:
#             return "応答なし"
#         else:
#             return response['choices'][0]['text']
         

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
    
    for user_id, audio in sink.audio_data.items():
        song = AudioSegment.from_file(audio.file, format="mp3")
        song.export(f"./{user_id}.mp3", format='mp3')
        await whisp(user_id, ctx)
    

async def whisp(user_id, ctx):
    segments, info = model.transcribe(f"{user_id}.mp3", beam_size=1, language="ja")
    for segment in segments:
        text = segment.text
        username  = bot.get_user(user_id)
        await ctx.channel.send(f"{username}:{text}")

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