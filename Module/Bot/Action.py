from ..Bot import verification as check
from ..Bot.Language import get_lang
from ..MultyType import LangType

from aiogram.types import user

async def get_language(user: user.User
             ) -> LangType.Language:
    language = check.Language(user=user)
    print(language.language_config.config.data[str(user.id)])
    lang = await get_lang() if not await language.lang_init() else await get_lang(lang=language.language_config.config.data[str(user.id)])

    return lang