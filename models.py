import json

from openai.types.chat.chat_completion_message import FunctionCall


class Func:
    def __init__(self, name: str, description: str, arguments: dict):
        self.name = name
        self.description = description
        self.arguments = arguments

    @classmethod
    def convert_from_fun_call(cls, desc: str, func_call: FunctionCall):
        return Func(
            name=func_call.name,
            description=desc,
            arguments=json.loads(func_call.arguments)
        )


class FuncProperty:
    def __init__(self, type: str, enum: list[object] = None, description: str = None):
        self.type = type
        self.enum = enum
        self.description = description


class FuncParameter:
    def __init__(self, type: str, properties: dict[str, FuncProperty], required: list[str]):
        self.type = type
        self.properties = properties
        self.required = required


class FuncDef:
    def __init__(self, name: str, description: str, parameters: FuncParameter):
        self.name = name
        self.description = description
        self.parameters = parameters

    def to_dict(self):
        return convert_to_dict(self)


def convert_to_dict(obj):
    if isinstance(obj, dict):
        return {key: convert_to_dict(value) for key, value in obj.items() if value is not None}
    elif isinstance(obj, list):
        return [convert_to_dict(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return convert_to_dict(obj.__dict__)
    else:
        return obj
