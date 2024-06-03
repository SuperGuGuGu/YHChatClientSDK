from Event import event_handle, on_message_func_list, on_command_func_list, group_join_func_list, group_leave_func_list, \
    bot_followed_func_list, bot_unfollowed_func_list, button_report_inline_func_list, on_event_func_list
from fastapi import FastAPI, Body

app = FastAPI()


@app.post("/")
def _(data=Body(...)):
    event_handle(data)


def on_message(func):
    on_message_func_list.append(func)


def on_command(func):
    on_command_func_list.append(func)


def group_join(func):
    group_join_func_list.append(func)


def group_leave(func):
    group_leave_func_list.append(func)


def bot_followed(func):
    bot_followed_func_list.append(func)


def bot_unfollowed(func):
    bot_unfollowed_func_list.append(func)


def button_report_inline(func):
    button_report_inline_func_list.append(func)


def on_event(func):
    on_event_func_list.append(func)
