from urllib import parse
from typing import *

from Message import MessageSegment
import inspect

on_event_func_list: List[Callable] = []
on_message_func_list: List[Callable] = []
on_command_func_list: List[Callable] = []
group_join_func_list: List[Callable] = []
group_leave_func_list: List[Callable] = []
bot_followed_func_list: List[Callable] = []
bot_unfollowed_func_list: List[Callable] = []
button_report_inline_func_list: List[Callable] = []


def message_convert(data):
    content_type = data["event"]["message"]["contentType"]
    content: Dict[str, (str | List[dict])] = data["event"]["message"]["content"]
    match content_type:
        case "text":
            data = {
                "type": "text",
                "data": {"text": content["text"]}
            }
        case "markdown":
            data = {
                "type": "markdown",
                "data": {"text": content["text"]}
            }
        case "image":
            data = {
                "type": "image",
                "data": {
                    "name": parse.urlparse(content["imageUrl"]).path[1:],
                    "url": content["imageUrl"]
                }
            }
    return data


class UserInfo:
    def __init__(self, user_data):
        self.id_ = user_data["senderId"]
        self.type = user_data["senderType"]
        self.level = user_data["senderUserLevel"]
        self.nickname = user_data["senderNickname"]


class Event:
    def __init__(self, data):
        self.event_id = data["header"]["eventId"]
        self.event_time = data["header"]["eventTime"]
        self.event_type = data["header"]["eventType"]

        match self.event_type:
            case "message.receive.normal":
                self.chat_type = data["event"]["message"]["chatType"]
                self.chat_id = data["event"]["message"]["chatId"]
                self.message_id = data["event"]["message"]["msgId"]
                self.message_parent_id = data["event"]["message"]["parentId"]
                self.message = message_convert(data)
                self.sender_info = UserInfo(data["event"]["sender"])
            case "message.receive.instruction":
                self.chat_type = data["event"]["message"]["chatType"]
                self.chat_id = data["event"]["message"]["chatId"]
                self.message_id = data["event"]["message"]["msgId"]
                self.message_parent_id = data["event"]["message"]["parentId"]
                self.message = message_convert(data)
                self.sender_info = UserInfo(data["event"]["sender"])

            case "bot.followed":
                pass
            case "bot.unfollowed":
                pass

            case "group.join":
                pass
            case "group.leave":
                pass

            case "button.report.inline":
                pass

            case _:
                pass


async def event_handle(data: dict):
    event = Event(data)

    match event.event_type:
        case "message.receive.normal":
            for func in on_message_func_list:
                signature = inspect.signature(func)
                if len(signature.parameters) == 0:
                    await func()
                elif len(signature.parameters) == 1:
                    await func(Event(data))
                else:
                    print(f"on_message 处理时 {func.__name__} 参数数量错误")
        case "message.receive.instruction":
            for func in on_command_func_list:
                signature = inspect.signature(func)
                if len(signature.parameters) == 0:
                    await func()
                elif len(signature.parameters) == 1:
                    await func(Event(data))
                else:
                    print(f"on_message 处理时 {func.__name__} 参数数量错误")
        case "bot.followed":
            for func in bot_followed_func_list:
                signature = inspect.signature(func)
                if len(signature.parameters) == 0:
                    await func()
                elif len(signature.parameters) == 1:
                    await func(Event(data))
                else:
                    print(f"on_message 处理时 {func.__name__} 参数数量错误")
        case "bot.unfollowed":
            for func in bot_unfollowed_func_list:
                signature = inspect.signature(func)
                if len(signature.parameters) == 0:
                    await func()
                elif len(signature.parameters) == 1:
                    await func(Event(data))
                else:
                    print(f"on_message 处理时 {func.__name__} 参数数量错误")
        case "group.join":
            for func in group_join_func_list:
                signature = inspect.signature(func)
                if len(signature.parameters) == 0:
                    await func()
                elif len(signature.parameters) == 1:
                    await func(Event(data))
                else:
                    print(f"on_message 处理时 {func.__name__} 参数数量错误")
        case "group.leave":
            for func in group_leave_func_list:
                signature = inspect.signature(func)
                if len(signature.parameters) == 0:
                    await func()
                elif len(signature.parameters) == 1:
                    await func(Event(data))
                else:
                    print(f"on_message 处理时 {func.__name__} 参数数量错误")
        case "button.report.inline":
            for func in button_report_inline_func_list:
                signature = inspect.signature(func)
                if len(signature.parameters) == 0:
                    await func()
                elif len(signature.parameters) == 1:
                    await func(Event(data))
                else:
                    print(f"on_message 处理时 {func.__name__} 参数数量错误")

    for func in on_event_func_list:
        signature = inspect.signature(func)
        if len(signature.parameters) == 0:
            await func()
        elif len(signature.parameters) == 1:
            await func(Event(data))
        else:
            print(f"on 处理时 {func.__name__} 参数数量错误")
