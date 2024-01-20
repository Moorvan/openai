from datetime import datetime

from chat_client import *

model = "gpt-3.5-turbo"

def get_time() -> str:
    return datetime.now().strftime("[%Y-%m-%d %H:%M]")

if __name__ == '__main__':
    message = [
        # root
        system("你是我的个人助理，对于我和你说的事情，你需要回答，当我和你说 mem 的时候，你需要返回一个 json，内容示例为：{\"mem\": true, \"content\": \"这是一个总结\"}, 其中前面的 mem 代表上面的内容是否需要记忆"),
        user(get_time() + "记得今天下午三点有个关于开放平台的会议"),
        assistant("好的，请问是在哪儿？"),
        user(get_time() + "在会议室 1"),
        assistant("好的，我已经记下来了"),
        user("mem"),
        assistant("{\"mem\": true, \"content\": \"2023-12-30 下午三点有个关于开放平台的会议，在会议室 1\"}"),

        # test
        user("[2023-12-30 12:00]我 明年 2 月 31 号需要买个牙刷"),
        assistant("好的")
    ]
    print(chat_to_gpt(model, message, "我什么时候需要买牙刷？"))