from ..Bot import Action as Action

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, user

async def get_menu(menu: str, 
                   user: user.User
                   ) -> ReplyKeyboardMarkup|None:
    lang = await Action.get_language(user=user)

    if menu == 'start':
        menu = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=lang.button_start_menu_login),
                    KeyboardButton(text=lang.button_start_menu_singup)
                ]
            ],
            resize_keyboard=True,
            input_field_placeholder=lang.description_start_menu
        )

    else:
        menu = None

    return menu