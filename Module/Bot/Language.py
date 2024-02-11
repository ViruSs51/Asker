from ..MultyType import LangType

__languages = {
    'ru': LangType.Language(
        welcome='Добро пожаловать, {username}!',
        about='Тут вы можете пройти какой-либо опрос, или же создать свой персональный опрос, а потом отправить его другим.',
        help='Чтобы пройти опрос, перешлите пригласительное сообщение, которое вам прислали вместе с ссылкой на данный бот.',
        button_start_menu_login='Войти в аккаунт',
        button_start_menu_signup='Зарегистрироваться',
        description_start_menu='Зарегистрируйтесь или войдите в аккаунт!',
        confirm_ask='Подтвердите ответ:',
        confirm_ask_button_continue='Продолжить',
        confirm_ask_button_edit='Редактировать ответ',
        message_for_edit='Отправьте новый ответ на вопрос выше в замен предыдущему:',
        finished_question='Поздравляю! Вы прошли данный опрос!'
    ),
    'en': LangType.Language(
        welcome='Welcome, {username}!',
        about='Here you can take any survey, or create your own personal survey, and then send it to others.',
        help='To take a survey, forward the invitation message sent to you along with a link to this bot.',
        button_start_menu_login='Log in to account',
        button_start_menu_signup='Sign up',
        description_start_menu='Sign up or log in to your account!',
        confirm_ask='Confirm the answer:',
        confirm_ask_button_continue='Continue',
        confirm_ask_button_edit='Edit answer',
        message_for_edit='Send a new answer to the question above to replace the previous one:',
        finished_question='Congratulations! You have completed this survey!'
    ),
    'ro': LangType.Language(
        welcome='Bun venit, {username}!',
        about='Aici poți lua orice sondaj sau crea propriul tău sondaj personal și apoi să-l trimiți altora.',
        help='Pentru a lua un sondaj, trimiteți mesajul de invitație trimis vouă împreună cu un link către acest bot.',
        button_start_menu_login='Conectați-vă la cont',
        button_start_menu_signup='Înscrieți-vă',
        description_start_menu='Înscrieți-vă sau conectați-vă la contul dvs.!',
        confirm_ask='Confirmați răspunsul:',
        confirm_ask_button_continue='Continuați',
        confirm_ask_button_edit='Editați răspunsul',
        message_for_edit='Trimiteți un nou răspuns la întrebarea de mai sus pentru a-l înlocui pe cel anterior:',
        finished_question='Felicitări! Ai completat acest sondaj!'
    )
}

async def get_lang(lang: str='ru'
             ) -> LangType.Language:
    return __languages[lang]