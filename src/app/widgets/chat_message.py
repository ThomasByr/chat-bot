from dataclasses import dataclass

import flet as ft

from ...helper.auto_numbered import AutoNumberedEnum


__all__ = ["Message", "ChatMessage", "MessageType"]


class MessageType(AutoNumberedEnum):
    CHAT_MSG = ()
    LOGIN_MSG = ()


@dataclass
class Message:
    user_name: str
    text: str
    message_type: MessageType


class ChatMessage(ft.Row):
    def __init__(self, msg: Message):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(msg.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(msg.user_name),
            ),
            ft.Column(
                [
                    ft.Text(msg.user_name, weight="bold"),
                    ft.Text(msg.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    @staticmethod
    def get_initials(user_name: str):
        try:
            return user_name[:1].capitalize()
        except (TypeError, AttributeError):
            return "?"

    @staticmethod
    def get_avatar_color(user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]
