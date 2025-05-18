"""The module is a script for running the bot."""

from hammett.core import Bot, Button, Screen
from hammett.core.constants import DEFAULT_STATE, SourceTypes
from hammett.core.mixins import StartMixin
from hammett.core.handlers import register_typing_handler

import requests
from bs4 import BeautifulSoup
from datetime import datetime



NEXT_SCREEN_DESCRIPTION = (
    'Good job 😎\n'
    'Now you see <b>NextScreen</b>. It also has a button. After pressing it, '
    '<b>StartScreen</b> re-renders into <b>NextScreen</b>.'
)

START_SCREEN_DESCRIPTION = (
    'Welcome to HammettSimpleJumpBot!\n'
    '\n'
    'This is <b>StartScreen</b> and it is a response to the /start command. '
    'Click the button below to jump to <b>NextScreen</b>.'
)


class NextScreen(Screen):
    """The class implements NextScreen, which is always sent as a new message."""

    description = NEXT_SCREEN_DESCRIPTION

    async def add_default_keyboard(self, _update, _context):
        """Set up the default keyboard for the screen."""
        return [[
            Button(
                '⬅️ Back',
                MeScreen,
                source_type=SourceTypes.MOVE_SOURCE_TYPE,
            ),
        ]]


class StartScreen(StartMixin):
    """The class implements StartScreen, which acts as a response
    to the /start command.
    """

    description = START_SCREEN_DESCRIPTION

    async def add_default_keyboard(self, _update, _context):
        """Set up the default keyboard for the screen."""
        return [
            [Button(
                'Next ➡️',
                NextScreen,
                source_type=SourceTypes.JUMP_SOURCE_TYPE,
            )],
            [Button(
                '📄 Source Code',
                'https://github.com/cusdeb-com/hammett/tree/main/demos/simple_jump_bot',
                source_type=SourceTypes.URL_SOURCE_TYPE)],
            [Button(
                '🎸 Hammett Homepage',
                'https://github.com/cusdeb-com/hammett',
                source_type=SourceTypes.URL_SOURCE_TYPE)],
        ]

class MeScreen(Screen):
    async def get_description(self, update, context):
        if context.user_data.get('text_input'):
            return (
                f'Вот твой список:\n'
                f'\n'
                f'{context.user_data["text_input"]}'
            )

        return 'Hey! Попробуй перечислить свой список через пробел!'

    @register_typing_handler
    async def handle_text_input(self, update, context):
        context.user_data['text_input'] = update.message.text

        return await self.jump(update, context)
    
def main():
    """Run the bot."""
    bot = Bot(
        'HammettSimpleJumpBot',
        entry_point=StartScreen,
        states={
            DEFAULT_STATE: {NextScreen, StartScreen, MeScreen},
        },
    )
    bot.run()


if __name__ == '__main__':
    main()
