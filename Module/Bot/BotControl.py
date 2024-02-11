from ..Bot import verification as check
from ..Bot import ActionRegister as reg
from ..Bot import Menu as menu
from ..Bot import Action as Action
from ..DataBase import get_db_connection

import asyncio

from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
#from aiogram.enums import ParseMode
#from aiogram.utils.keyboard import InlineKeyboardBuilder

class Answer:

    def __init__(self,
                 bot: Bot
                 ) -> None:
        #self.message_register = reg.Message()
        self.bot = bot
        self.db = get_db_connection()

    async def start(self,
                    message: Message
                    ) -> None:
        user_data = message.from_user
        lang = await Action.get_language(user=user_data)

        #await self.message_register.delete_message(bot=self.bot,
        #                                           message=message,
        #                                           n=2,
        #                                           all=True)
        
        user = check.User(user=user_data)
        username = await user.get_name()

        #Register message(id and time)
        #await self.message_register.register_message(message=message)

        #Welcome and description message
        await message.answer(
                            text=f'{lang.welcome.format(username=username)}\n{lang.about}\n\n{lang.help}',
                            reply_markup=await menu.get_menu(menu='start', user=user_data)
        )
        #await self.message_register.register_message(message=send_message)

    async def start_questions(self,
                              message: Message
                              ) -> None:
        asker_key = message.text.split('"')[1]
        user_data = message.from_user
        #lang = await Action.get_language(user=user_data)
    
        #await self.message_register.register_message(message=message)

        #Delete message
        #await self.message_register.delete_message(bot=self.bot,
        #                                           message=message,
        #                                           n=3,
        #                                           all=True)
    
        #Get ask from databse
        ask_data = await Action.get_ask(asker_key=asker_key,
                                        ask_queue=1)
        if not ask_data:
            return
        
        await message.answer(text=ask_data[0][1],
                                reply_markup=ReplyKeyboardRemove())
        
        #await self.message_register.register_message(message=send_message)

        await Action.add_user_answer_template(user_id=user_data.id, 
                                                ask_data=ask_data, 
                                                asker_key=asker_key)

    async def get_answer(self,
                         message: Message
                         ) -> None:
        user_answer: tuple
        user_data = message.from_user
        lang = await Action.get_language(user=user_data)

        #await self.message_register.register_message(message=message)

        user_answers = await Action.get_user_answers(user_id=message.from_user.id)

        if user_answers:
            for answer in user_answers:
                if not answer[3]:
                    user_answer = answer

                    break
            
            else:
                #await self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                return

            await Action.add_user_answer(answer=message.text,
                                   user_id=message.from_user.id,
                                   ask_id=user_answer[0],
                                   asker_key=user_answer[1])
            
            await message.answer(text=lang.confirm_ask,
                                                reply_markup=await menu.get_confirmed_ask(user=user_data))
            #await self.message_register.register_message(message=send_message)
            

    
    async def confirmed_answer(self,
                               callback: CallbackQuery
                               ) -> None:
        user_answer: tuple
        message = callback.message
        user_data = callback.from_user
        lang = await Action.get_language(user=user_data)

        #Delete message
        #await self.message_register.delete_message(bot=self.bot,
        #                                           message=callback.message,
        #                                           n=3,
        #                                           all=True)
        await self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        
        user_answers = await Action.get_user_answers(user_id=user_data.id)

        if user_answers:
            user_answer = await Action.get_answer_from_list(list=user_answers)

            if not user_answer:
                return
            
            await Action.confirm_user_answer(user_id=user_data.id,
                                             ask_id=user_answer[0],
                                             asker_key=user_answer[1])
            
            #Get ask from databse
            ask_data = await Action.get_ask(asker_key=user_answer[1],
                                            ask_queue=user_answer[0]+1)
            if not ask_data:
                await self.bot.send_message(chat_id=message.chat.id,
                                                       text=lang.finished_question,
                                                       reply_markup=await menu.get_menu(menu='start', user=user_data))
            
            else:
                await self.bot.send_message(chat_id=message.chat.id,
                                                           text=ask_data[0][1],
                                                           reply_markup=ReplyKeyboardRemove())
                #await self.message_register.register_message(message=send_message)

                #Add user answer Null to database
                await Action.add_user_answer_template(user_id=user_data.id, 
                                                      ask_data=ask_data, 
                                                      asker_key=user_answer[1])
            
            await callback.answer()
    
    async def no_confirmed_answer(self,
                                  callback: CallbackQuery
                                  ) -> None:
        user_answer: tuple
        message = callback.message
        user_data = callback.from_user
        lang = await Action.get_language(user=user_data)

        #Delete message
        #await self.message_register.delete_message(bot=self.bot,
        #                                           message=message,
        #                                           n=3,
        #                                           all=True)
        await self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        
        user_answers = await Action.get_user_answers(user_id=user_data.id)

        if user_answers:
            user_answer = await Action.get_answer_from_list(list=user_answers)

            if not user_answer:
                return

            await Action.reset_user_answer(user_id=user_data.id,
                                           ask_id=user_answer[0],
                                           asker_key=user_answer[1])

            await self.bot.send_message(chat_id=message.chat.id,
                                                       text=lang.message_for_edit,
                                                       reply_markup=ReplyKeyboardRemove())
            #await self.message_register.register_message(message=send_message)

            await callback.answer()
    
    async def another_message(self,
                              message: Message
                              ) -> None:
        #Register message(id)
        #await self.message_register.register_message(message=message)
        #    
        #await self.message_register.delete_message(bot=self.bot,
        #                                           message=message,
        #                                           n=1)
        await self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)