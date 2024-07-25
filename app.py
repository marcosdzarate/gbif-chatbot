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


with open('/response_1720786934558_schema.json', 'r', encoding="utf8") as f:
    json_schema = json.load(f)

with open('/response_1720786934558_data.json', 'r', encoding="utf8") as f:
    json_data = json.load(f)


@cl.on_message
async def on_message(message: cl.Message):
    response = await client.chat.completions.create(
        messages=[
            {
                "content": """You are a chatbot named "GBIBot" designed to assist users with datasets published in the Global Biodiversity Information Facility (GBIF).
                Your expertise is focused solely on providing information about biodiversity datasets via GBIF. This includes metadata, institutions, locations, person, 
                dates, and general queries related to the metadata associated with the datasets. You do not provide information outside this scope. 
                If a question is not about biodiversity data, please reply: "I specialize only in queries related to biodiversity data from GBIF." 
                Always reply in Spanish""",
                "role": "system"
            },
            {
                "content": f"Tienes un archivo JSON con los siguientes datos: {json.dumps(json_data)}",
                "role": "system"
            },
            {
                "content": f"Tienes un archivo JSON schema describiendo los datos: {json.dumps(json_schema)}",
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