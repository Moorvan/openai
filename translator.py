from chat_client import *

root_message = [
    system("You are a translation expert. Translate Chinese to English, English to Chinese, and other language to English and Chinese at the same time."),
    user("你好"),
    assistant("Hello"),
    user("おはようございます"),
    assistant("en: Good morning\nch: 早上好")
]


def translate(text: str):
    return chat_to_gpt("gpt-3.5-turbo", root_message, text)


if __name__ == '__main__':
    # set_debug()
    print(translate("仕事したくありません"))
