from ..MultyType import LangType

__languages = {
    'ru': LangType.Language(
        welcome='Добро пожаловать, {username}!',
        about='Тут вы можете пройти какой-либо опрос, или же создать свой персональный опрос, а потом отправить его другим.',
        help='Чтобы пройти опрос, перешлите пригласительное сообщение, которое вам прислали вместе с ссылкой на данного бота.',
        button_start_menu_login='Войти в аккаунт',
        button_start_menu_singup='Зарегистрироваться',
        description_start_menu='Зарегистрируйся или войти в аккаунт!'
    ),
    'en': LangType.Language(
        welcome='Welcome, {username}!',
        about='Here you can take any survey, or create your own personal survey, and then send it to others.',
        help='To take the survey, forward the invitation message you received along with the link to this bot.',
        button_start_menu_login='Log in',
        button_start_menu_singup='Sign up',
        description_start_menu='Sign up or log in to your account!'
    )
}

async def get_lang(lang: str='en'
             ) -> LangType.Language:
    return __languages[lang]