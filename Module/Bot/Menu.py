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
                    [
                        KeyboardButton(text='Ответы')
                    ],
                    [
                        KeyboardButton(text='Помощь'),
                        KeyboardButton(text='⬅️')
                    ],
                    #[
                    #    KeyboardButton(text='Настройки')
                    #],
                ],
                resize_keyboard=True,
            )
        else:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=lang.b1),
                        KeyboardButton(text=lang.b2)
                    ],
                    [
                        KeyboardButton(text='Помощь')
                    ]
                ],
                resize_keyboard=True,
                input_field_placeholder=lang.p4
            )

    else:
        keyboard = None

    return keyboard

async def get_confirmed_ask(user: user.User,
                            asker_key: str
                            ) -> InlineKeyboardMarkup:
    lang = await Action.get_language(user=user)
    db = get_db_connection()
    ask_len = len(db.SQL(sql_command=f"SELECT queue, ask, type, answers FROM asks WHERE asker_key='{asker_key}'"))

    keyboard = [
            [
                InlineKeyboardButton(text=lang.b3,
                                     callback_data='answer-confirmed'),
                #InlineKeyboardButton(text=lang.b4,
                #                     callback_data='answer-no-confirmed')
            ]  
        ]
    row = 2
    for answer in range(ask_len):
        while len(keyboard) < row: keyboard.append([])
        if len(keyboard[row-1]) <= 5:
            keyboard[row-1].append(InlineKeyboardButton(
                    text=str(answer+1),
                    callback_data=f'UserAnswer:{answer}',  
            ))
        
        else:
            row += 1
            keyboard.append([])
            keyboard[row-1].append(InlineKeyboardButton(
                    text=str(answer+1),
                    callback_data=f'UserAnswer:{answer}',  
            ))
        


    keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
    
    return keyboard

async def get_ask_keyboard(ask_data: list[tuple]
                           ) -> InlineKeyboardMarkup|None:
    if ask_data[0][2] == 'note':
        keyboard = []

        row = 1
        for answer in ask_data[0][3].split('#'):
            while len(keyboard) < row: keyboard.append([])

            if len(answer) <= 1:
                if len(keyboard[row-1]) <= 5:
                    keyboard[row-1].append(InlineKeyboardButton(
                            text=answer,
                            callback_data=f'UserAnswer:{answer}',  
                    ))
                
                else:
                    row += 1
                    keyboard.append([])
                    keyboard[row-1].append(InlineKeyboardButton(
                            text=answer,
                            callback_data=f'UserAnswer:{answer}',  
                    ))

            elif len(answer) <= 2:
                if len(keyboard[row-1]) <= 4:
                    keyboard[row-1].append(InlineKeyboardButton(
                            text=answer,
                            callback_data=f'UserAnswer:{answer}',  
                    ))
                
                else:
                    row += 1
                    keyboard.append([])
                    keyboard[row-1].append(InlineKeyboardButton(
                            text=answer,
                            callback_data=f'UserAnswer:{answer}',  
                    ))
            elif len(answer) <= 4:
                if len(keyboard[row-1]) <= 3:
                    keyboard[row-1].append(InlineKeyboardButton(
                            text=answer,
                            callback_data=f'UserAnswer:{answer}',  
                    ))
                
                else:
                    row += 1
                    keyboard.append([])
                    keyboard[row-1].append(InlineKeyboardButton(
                            text=answer,
                            callback_data=f'UserAnswer:{answer}',  
                    ))
            
            elif len(answer) <= 6:
                if len(keyboard[row-1]) <= 2:
                    keyboard[row-1].append(InlineKeyboardButton(
                            text=answer,
                            callback_data=f'UserAnswer:{answer}',  
                    ))
                
                else:
                    row += 1
                    keyboard.append([])
                    keyboard[row-1].append(InlineKeyboardButton(
                            text=answer,
                            callback_data=f'UserAnswer:{answer}',  
                    ))
            
            elif len(answer) > 6:
                row += 1
                keyboard.append([])
                keyboard[row-1].append(InlineKeyboardButton(
                        text=answer,
                        callback_data=f'UserAnswer:{answer}',  
                ))

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

async def get_menu_myask(asker_key: str) -> ReplyKeyboardMarkup|None:
    db = get_db_connection()
    asks = db.SQL(f"SELECT `ask` FROM `asks` WHERE `asker_key` = '{asker_key}'")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Новый вопрос'),
                KeyboardButton(text='Изменить названия')
            ],
            [
                KeyboardButton(text='🚫Удалить опрос🚫'),
                KeyboardButton(text='⬅️')
            ]
        ] + ([
            [KeyboardButton(text=button[0])]
            for button in asks
        ] if asks else []),
        resize_keyboard=True
    )

    return keyboard

async def get_confirm_delete_asker() -> InlineKeyboardMarkup|None:
    keyboard = [
        [
            InlineKeyboardButton(
                text='Удалить',
                callback_data='DeleteAsker:yes',
                )
        ],
        [
            InlineKeyboardButton(
                text='Не удалять',
                callback_data='DeleteAsker:no',
                )
        ]
    ]
        
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def get_menu_myaskask() -> ReplyKeyboardMarkup|None:
    kb = [
            [
                KeyboardButton(text='Редактировать текст')
            ],
            [            
                KeyboardButton(text='Редактировать формат ответов')
            ],
            [            
                KeyboardButton(text='Редактировать ответы')
            ],
            [
                KeyboardButton(text='Редактировать последовательность')
            ],
            [
                KeyboardButton(text='🚫Удалить вопрос🚫')
            ],
            [
                KeyboardButton(text='⬅️')
            ]
        ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
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

async def help_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Связаться с службой поддержки')
            ],
            [
                KeyboardButton(text='⬅️')
            ]
        ],
        resize_keyboard=True
    )