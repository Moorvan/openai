from chat_client import *


def test_chat():
    res = chat_to_gpt(model_3_5_turbo, [], text="Please return OK")
    print(res)


func_def = FuncDef(
    name="get_current_weather",
    description="Get the current weather in a given location",
    parameters=FuncParameter(
        type="object",
        properties={
            "location": FuncProperty(
                type="string",
                description="The city and state, e.g. San Francisco, CA"
            ),
            "unit": FuncProperty(
                type="string",
                enum=["celsius", "fahrenheit"],
                description="The unit of temperature"
            )
        },
        required=["location", "unit"]
    )
)


def test_get_json_data():
    func = get_json_data(model_3_5_turbo, text="What is the weather like in Shanghai?", funcs=[func_def])
    print(f"func name: {func.name}, func arguments: {func.arguments}")


def test_get_message_from_json():
    print(get_message_from_json(model=model_3_5_turbo, base_message=[
        user("What is the weather like in Boston?"),
        assistant_func("get_current_weather", {
            "location": "Boston, MA"
        })
    ], func_json=Func(
        name="get_current_weather",
        description="Get the current weather in a given location",
        arguments={
            "temperature": "22",
            "unit": "celsius",
            "description": "Sunny"
        }
    ), funcs=[func_def]))


if __name__ == '__main__':
    set_debug()
    # test_get_json_data()
    test_chat()
    # test_get_message_from_json()
