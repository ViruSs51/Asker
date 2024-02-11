from dataclasses import dataclass

@dataclass
class Language:
    welcome: str
    about: str
    help: str
    button_start_menu_login: str
    button_start_menu_signup: str
    description_start_menu: str
    confirm_ask: str
    confirm_ask_button_continue: str
    confirm_ask_button_edit: str
    message_for_edit: str
    finished_question: str