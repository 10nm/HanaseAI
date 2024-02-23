import discord
from llama_cpp import Llama
import os

llm = Llama(
    model_path = "../models/gguf/calm2-7b-chat-q5km.gguf", n_gpu_layers=-1
)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
 
    async def on_message(self, message):
        ct = message.content

        if message.author == self.user:
            return
        
        print('Message from {0.author}: {0.content}'.format(message))

        if message.content == '!ping':
            await message.channel.send('pong')

        if message.content == '!join':
            await message.author.voice.channel.connect()    
        
        if message.content == '!leave':
            await message.guild.voice_client.disconnect()
        
        if ct.startswith('.') ==  True:
            prompt = (message.content)
            prompt = prompt.lstrip('.')
            completion = await nlp(prompt)
            await message.channel.send(completion)

async def nlp(prompt):
    response= llm(f"""### ユーザー: {prompt} 
### アシスタント:""",max_tokens=250, stop=["###","ユーザー","アシスタント"])
    if response['choices'][0]['text'] == 0:
        return "応答なし"
    else:
        return response['choices'][0]['text']

token = os.environ.get("TOKEN")

client = MyClient(intents=discord.Intents.all())
client.run(str(token))