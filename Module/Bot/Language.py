from ..MultyType import LangType

__languages = {
    'ru': LangType.Language(
        welcome='Добро пожаловать, {username}!'
    )
}

lang: LangType.Language = __languages['ru']