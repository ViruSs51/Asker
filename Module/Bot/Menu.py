from ..Bot import Action as Action
from ..DataBase import get_db_connection

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, user

async def get_menu(menu: str, 
                   user: user.User
                   ) -> ReplyKeyboardMarkup|None:
    db = get_db_connection()
    lang = await Action.get_language(user=user)
    connected_id = db.SQL(f"SELECT `connected_id` FROM `users`")

    if menu == 'start':
        connected = False
        for connect in connected_id:
            if str(user.id) in connect[0].split(','):
                connected = True
                break

        if connected:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text='Мой опросы')
                    ],
                    #[
                    #    KeyboardButton(text='Настройки')
                    #],
                    #[
                    #    KeyboardButton(text='Выйти')
                    #]
                ],
                resize_keyboard=True,
            )
        else:
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

async def get_ask_keyboard(ask_data: list[tuple]
                           ) -> InlineKeyboardMarkup|None:
    if ask_data[0][2] == 'note':
        keyboard = []
        
        for answer in ask_data[0][3].split(','):
            keyboard.append([InlineKeyboardButton(
                    text=answer,
                    callback_data=f'UserAnswer:{answer}',
                    
            )])

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    else:
        return None
    
async def get_exit_button(
                   ) -> ReplyKeyboardMarkup|None:
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='⬅️')
            ]
        ],
        resize_keyboard=True
    )

    return keyboard

async def get_menu_myasks(user_data: user.User) -> ReplyKeyboardMarkup|None:
    db = get_db_connection()
    connected_id = db.SQL(f"SELECT `connected_id`, `username` FROM `users`")

    connected_username = None
    for connect in connected_id:
        if str(user_data.id) in connect[0].split(','):
            connected_username = connect[1]

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Новый опрос'),
                KeyboardButton(text='⬅️')
            ]
        ] + [
            [KeyboardButton(text=button.split(':')[0])] 
            for button in db.SQL(f"SELECT `asker_key` FROM `users` WHERE `username` = '{connected_username}'")[0][0].split(',')
        ],
        resize_keyboard=True
    )

    return keyboard

async def get_menu_myask(asker_key:str) -> ReplyKeyboardMarkup|None:
    db = get_db_connection()
    asks = db.SQL(f"SELECT `ask` FROM `asks` WHERE `asker_key` = '{asker_key}'")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Новый вопрос'),
                KeyboardButton(text='⬅️')
            ]
        ] + ([
            [KeyboardButton(text=button[0])]
            for button in asks
        ] if asks else []),
        resize_keyboard=True
    )

    return keyboard

async def get_ask_type() -> InlineKeyboardMarkup|None:
    keyboard = [
        [
            InlineKeyboardButton(
                text='Текст',
                callback_data='SetNewAskType:text',
                )
        ],
        [
            InlineKeyboardButton(
                text='Кнопки',
                callback_data='SetNewAskType:note',
                )
        ],
        [
            InlineKeyboardButton(
                text='⬅️',
                callback_data='SetNewAskType:⬅️',
                )
        ]
    ]
        
    return InlineKeyboardMarkup(inline_keyboard=keyboard)