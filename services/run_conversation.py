from openai import OpenAI # openai==1.2.0
import json
 
client = OpenAI(api_key="YOU_API_KEY", base_url="https://api.upstage.ai/v1/solar")
 
from tools.function_calls import functions as FUNCTIONS
from tools.function_calls import functions_description as FUNCTIONS_DESCRIPTION

def run_conversation():
    # Step 1: send the conversation and available functions to the model
    messages = [
        {
            "role": "user",
            "content": "How is the weather in San Francisco today?",
        }
    ]
    tools = FUNCTIONS_DESCRIPTION
    response = client.chat.completions.create(
        model="solar-1-mini-chat",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
 
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = FUNCTIONS
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
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
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model="solar-1-mini-chat",
            messages=messages,
        )  # get a new response from the model where it can see the function response
        return second_response
 
 
print(run_conversation())