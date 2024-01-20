import json

from openai import OpenAI
from models import *

client = OpenAI(api_key="sk-xxx",
                base_url="xx")


model_3_5_turbo = "gpt-3.5-turbo"
model_4 = "gpt-4"


def system(text: str) -> dict:
    return {
        "role": "system",
        "content": text
    }


def user(text: str) -> dict:
    return {
        "role": "user",
        "content": text
    }


def assistant(text: str) -> dict:
    return {
        "role": "assistant",
        "content": text
    }


def assistant_func(name: str, args: dict) -> dict:
    return {
        "role": "assistant",
        "content": "",
        "function_call": {
            "name": name,
            "arguments": json.dumps(args)
        }
    }


def function(func: Func) -> dict:
    return {
        "role": "function",
        "name": func.name,
        "content": json.dumps(func.arguments)
    }


debug = False


def set_debug(b=True):
    global debug
    debug = b


def chat_to_gpt(model: str, base_message: list[dict], text: str) -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=base_message + [user(text)]
    )
    if debug:
        print(resp)
    if resp.choices[0].finish_reason != "stop":
        raise Exception("[chat_to_gpt] failed")
    return resp.choices[0].message.content


def get_json_data(model: str, text: str, funcs: list[FuncDef]) -> Func:
    resp = client.chat.completions.create(
        model=model,
        messages=[
            user(text)
        ],
        functions=list(map(lambda x: x.to_dict(), funcs))
    )
    if debug:
        print(resp)
    if len(resp.choices) == 0:
        raise Exception("[get_json_data] failed")
    if resp.choices[0].message.function_call is None:
        raise Exception(f"[get_json_data] failed: {resp.choices[0].message.content}")
    func_call = resp.choices[0].message.function_call
    return Func.convert_from_fun_call(desc=func_call.name, func_call=func_call)


def get_message_from_json(model: str, base_message: list[dict], func_json: Func, funcs: list[FuncDef]) -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=base_message + [function(func_json)],
        functions=list(map(lambda x: x.to_dict(), funcs)),
    )
    if debug:
        print(resp)
    if resp.choices[0].finish_reason != "stop":
        raise Exception("[get_message_from_json] failed")
    return resp.choices[0].message.content


if __name__ == '__main__':
    pass
