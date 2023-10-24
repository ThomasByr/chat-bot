import logging
import flet as ft

from .widgets import (
    Message,
    MessageType,
    ChatMessage,
    SignInForm,
    SignUpForm,
    TypingIndicator,
)
from ..db import UsersDB
from ..bot import Model

__all__ = ["home_page"]


def home_page(page: ft.Page):
    logger = logging.getLogger("home_page")
    logger.info("starting home page")

    page.title = "Chat Flet NILS"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    logger.info("loading model")
    bot_name = "NILS"
    model = Model()  # new model per session

    # %% Functions
    def dropdown_changed(_):
        new_message.value = new_message.value + emoji_list.value
        page.update()

    def close_banner(_):
        page.banner.open = False
        page.update()

    def open_dlg(d):
        page.dialog = d
        dlg.open = True
        page.update()

    def close_dlg(_):
        dlg.open = False
        page.route = "/"
        page.update()

    def sign_in(user: str, password: str):
        db = UsersDB()
        if not db.read_db(user, password):
            logger.warning("User does not exist ...")
            page.banner.open = True
            page.update()
        else:
            logger.info("Redirecting to chat ...")
            page.session.set("user", user)
            page.route = "/chat"
            page.pubsub.send_all(
                Message(
                    user_name=user,
                    text=f"{user} has joined the chat.",
                    message_type=MessageType.LOGIN_MSG,
                )
            )
            page.update()

    def sign_up(user: str, password: str):
        db = UsersDB()
        if db.write_db(user, password):
            logger.info("Successfully Registered User...")
            open_dlg(dlg)

    def on_message(message: Message):
        if message.message_type == MessageType.CHAT_MSG:
            m = ChatMessage(message)
        elif message.message_type == MessageType.LOGIN_MSG:
            m = ft.Text(message.text, italic=True, color=ft.colors.WHITE, size=12)
        elif message.message_type == MessageType.TYPING:
            m = TypingIndicator(message.user_name)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    def build_response(message: str):
        # maybe preprocess message
        return model.get_build_response(message)

    def send_message_click(_):
        if not new_message.value or new_message.value.isspace():
            return
        page.pubsub.send_all(
            Message(
                user_name=page.session.get("user"),
                text=new_message.value,
                message_type=MessageType.CHAT_MSG,
            )
        )
        tmp = new_message.value
        new_message.value = ""
        new_message.focus()

        # typing indicator
        page.pubsub.send_all(
            Message(
                user_name=bot_name,
                text="",
                message_type=MessageType.TYPING,
            )
        )
        res = build_response(tmp)
        # find and remove last typing indicator without the risk of removing a message
        for i, c in enumerate(chat.controls):
            if isinstance(c, TypingIndicator):
                del chat.controls[i]
                break
        if res:
            page.pubsub.send_all(
                Message(
                    user_name=bot_name,
                    text=res,
                    message_type=MessageType.CHAT_MSG,
                )
            )
        page.update()

    def btn_signin(_):
        page.route = "/"
        page.update()

    def btn_signup(_):
        page.route = "/signup"
        page.update()

    def btn_exit(_):
        page.session.remove("user")
        page.route = "/"
        page.update()

    def check_device():
        if model.get_device() < 0:
            logger.warning("No GPU found, using CPU instead")
            page.banner = ft.Banner(
                bgcolor=ft.colors.BLACK45,
                leading=ft.Icon(ft.icons.ERROR, color=ft.colors.RED, size=40),
                content=ft.Text("No GPU found, using CPU instead"),
                actions=[
                    ft.TextButton("Ok", on_click=close_banner),
                ],
            )
            page.banner.open = True
            page.update()

    # %% Application UI
    principal_content = ft.Column(
        [
            ft.Icon(ft.icons.WECHAT, size=200, color=ft.colors.BLUE),
            ft.Text(value="Chat Flet NILS", size=50, color=ft.colors.WHITE),
        ],
        height=400,
        width=600,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    emoji_list = ft.Dropdown(
        on_change=dropdown_changed,
        options=[
            ft.dropdown.Option("😃"),
            ft.dropdown.Option("😊"),
            ft.dropdown.Option("😂"),
            ft.dropdown.Option("🤔"),
            ft.dropdown.Option("😭"),
            ft.dropdown.Option("😉"),
            ft.dropdown.Option("🤩"),
            ft.dropdown.Option("🥰"),
            ft.dropdown.Option("😎"),
            ft.dropdown.Option("❤️"),
            ft.dropdown.Option("🔥"),
            ft.dropdown.Option("✅"),
            ft.dropdown.Option("✨"),
            ft.dropdown.Option("👍"),
            ft.dropdown.Option("🎉"),
            ft.dropdown.Option("👉"),
            ft.dropdown.Option("⭐"),
            ft.dropdown.Option("☀️"),
            ft.dropdown.Option("👀"),
            ft.dropdown.Option("👇"),
            ft.dropdown.Option("🚀"),
            ft.dropdown.Option("🎂"),
            ft.dropdown.Option("💕"),
            ft.dropdown.Option("🏡"),
            ft.dropdown.Option("🍎"),
            ft.dropdown.Option("🎁"),
            ft.dropdown.Option("💯"),
            ft.dropdown.Option("💤"),
        ],
        width=50,
        value="😃",
        alignment=ft.alignment.center,
        border_color=ft.colors.AMBER,
        color=ft.colors.AMBER,
    )

    signin_UI = SignInForm(sign_in, btn_signup)
    signup_UI = SignUpForm(sign_up, btn_signin)

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    page.banner = ft.Banner(
        bgcolor=ft.colors.BLACK45,
        leading=ft.Icon(ft.icons.ERROR, color=ft.colors.RED, size=40),
        content=ft.Text("Log in failed, Incorrect User Name or Password"),
        actions=[
            ft.TextButton("Ok", on_click=close_banner),
        ],
    )

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Container(
            content=ft.Icon(
                name=ft.icons.CHECK_CIRCLE_OUTLINED, color=ft.colors.GREEN, size=100
            ),
            width=120,
            height=120,
        ),
        content=ft.Text(
            value="Congratulations,\n your account has been successfully created\n Please Sign In",
            text_align=ft.TextAlign.CENTER,
        ),
        actions=[
            ft.ElevatedButton(
                text="Continue", color=ft.colors.WHITE, on_click=close_dlg
            )
        ],
        actions_alignment="center",
        on_dismiss=lambda _: logger.debug("Dialog dismissed!"),
    )

    # %% Routes
    def route_change(_):
        if page.route == "/":
            page.clean()
            page.add(
                ft.Row(
                    [principal_content, signin_UI],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        if page.route == "/signup":
            page.clean()
            page.add(
                ft.Row(
                    [principal_content, signup_UI],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        if page.route == "/chat":
            if page.session.contains_key("user"):
                page.clean()
                close_banner(None)
                page.add(
                    ft.Row(
                        [
                            ft.Text(value="Chat Flet NILS", color=ft.colors.WHITE),
                            ft.ElevatedButton(
                                text="Log Out",
                                bgcolor=ft.colors.RED_800,
                                on_click=btn_exit,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    )
                )
                page.add(
                    ft.Container(
                        content=chat,
                        border=ft.border.all(1, ft.colors.OUTLINE),
                        border_radius=5,
                        padding=10,
                        expand=True,
                    )
                )
                page.add(
                    ft.Row(
                        controls=[
                            emoji_list,
                            new_message,
                            ft.IconButton(
                                icon=ft.icons.SEND_ROUNDED,
                                tooltip="Send message",
                                on_click=send_message_click,
                            ),
                        ],
                    )
                )
                # make chat bot say hello
                page.pubsub.send_all(
                    Message(
                        user_name=bot_name,
                        text=model.build_welcome_msg(page.session.get("user")),
                        message_type=MessageType.CHAT_MSG,
                    )
                )
                check_device()

            else:
                page.route = "/"
                page.update()

    page.on_route_change = route_change
    page.add(
        ft.Row([principal_content, signin_UI], alignment=ft.MainAxisAlignment.CENTER)
    )
