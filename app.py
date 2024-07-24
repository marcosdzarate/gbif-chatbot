from openai import AsyncOpenAI
import chainlit as cl
import json

client = AsyncOpenAI()

# Instrument the OpenAI client
cl.instrument_openai()

settings = {
    "model": "gpt-4",
    "temperature": 0,
    "max_tokens": 200,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stop": ["```"]

}

with open('./response_1720786934558_data.json', 'r') as f:
    json_data = json.load(f)

@cl.on_message
async def on_message(message: cl.Message):
    response = await client.chat.completions.create(
        messages=[
            {
                "content": "You are a helpful bot, you always reply in Spanish",
                "role": "system"
            },
            {
                "content": f"Tienes un archivo JSON con el siguiente contenido: {json.dumps(json_data)}",
                "role": "system"
            },
            {
                "content": message.content,
                "role": "user"
            }
        ],
        **settings
    )
    await cl.Message(content=response.choices[0].message.content).send()