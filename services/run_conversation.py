import json
import os

import dotenv
from openai import OpenAI  # openai==1.2.0

dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"), base_url="https://api.upstage.ai/v1/solar")

from tools.function_calls import functions as FUNCTIONS
from tools.function_calls import function_descriptions as FUNCTION_DESCRIPTIONS


def run_conversation(message):
    messages = [
        {
            "role": "user",
            "content": message,
        }
    ]
    tools = FUNCTION_DESCRIPTIONS
    response = client.chat.completions.create(
        model="solar-1-mini-chat",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    print(f'tool_calls: {tool_calls}')

    if tool_calls:
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = FUNCTIONS[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        print(f'messages: {messages}')
        return client.chat.completions.create(
            model="solar-1-mini-chat",
            messages=messages,
        )


print(run_conversation("Hi, Please recommend a place to eat near east-kareum"))
