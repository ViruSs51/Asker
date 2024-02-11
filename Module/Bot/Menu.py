from ..Bot import Action as Action

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, user

async def get_menu(menu: str, 
                   user: user.User
                   ) -> ReplyKeyboardMarkup|None:
    lang = await Action.get_language(user=user)

    if menu == 'start':
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=lang.button_start_menu_login),
                    KeyboardButton(text=lang.button_start_menu_signup)
                ]
            ],
            resize_keyboard=True,
            input_field_placeholder=lang.description_start_menu
        )

    else:
        keyboard = None

    return keyboard

async def get_confirmed_ask(user: user.User
                            ) -> InlineKeyboardMarkup:
    lang = await Action.get_language(user=user)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=lang.confirm_ask_button_continue,
                                     callback_data='answer-confirmed'),
                InlineKeyboardButton(text=lang.confirm_ask_button_edit,
                                     callback_data='answer-no-confirmed')
            ]
        ]
    )
    
    return keyboard