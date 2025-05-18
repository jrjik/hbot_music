"""The module is a script for running the bot."""

from hammett.core import Bot, Button, Screen
from hammett.core.constants import DEFAULT_STATE, RenderConfig, SourceTypes
from hammett.core.mixins import StartMixin
from hammett.core.handlers import register_typing_handler
from hammett.core.handlers import register_button_handler

from database import save_user_list  # Импортируем нашу функцию
from database import get_user_list
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

ARTISTLIST_SCREEN_DESCRIPTION = (
    'Перечисли свой список через пробел'
    '\n'
    'Ниже ты можешь вернуться на начальный экран'
)

class NextScreen(Screen):
    """The class implements NextScreen, which is always sent as a new message."""

    description = NEXT_SCREEN_DESCRIPTION

    async def add_default_keyboard(self, _update, _context):
        """Set up the default keyboard for the screen."""
        return [[
            Button(
                '⬅️ Back',
                StartScreen,
                source_type=SourceTypes.MOVE_SOURCE_TYPE,
            ),
            
        ]]

class ArtistListEdit(Screen):

    description = ARTISTLIST_SCREEN_DESCRIPTION

    async def add_default_keyboard(self, _update, _context):
        return [[
            Button(
                '⬅️ Back',
                StartScreen,
                source_type=SourceTypes.MOVE_SOURCE_TYPE,
            ),
            
        ]]
    @register_typing_handler
    async def handle_text_input(self, update, context):
        user_id = update.message.from_user.id  # Получаем ID пользователя
        user_text = update.message.text
        items = [item.strip() for item in user_text.split(",")]
        
        # Сохраняем в БД
        save_user_list(user_id, items)
        
        # Сообщение пользователю
        await update.message.reply_text(
            f"Список сохранён в базу данных!\n"
            f"Ваш список: {', '.join(items)}"
        )
        await self.render(update, context, config=RenderConfig(
            as_new_message=True,
            keyboard=[
                [Button(
                    'Вернуться на главный экран',
                    StartScreen,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                )],
                ],
        ))
       
class ArtistListShow(Screen):
    description = "Нажмите кнопку, чтобы увидеть ваш список исполнителей"

    async def add_default_keyboard(self, _update, _context):
        return [
            [
                Button(
                    '🎵 Показать моих исполнителей',
                    source=self.show_artists_handler,  # Указываем обработчик
                    source_type=SourceTypes.HANDLER_SOURCE_TYPE,
                ),
            ],
            [
                Button(
                    '⬅️ Back',
                    StartScreen,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                )
            ]
        ]

    @register_button_handler
    async def show_artists_handler(self, update, context):
        user_id = update.callback_query.from_user.id
        artists = get_user_list(user_id)  # Функция из database.py
        
        if not artists:
            await update.callback_query.answer(
                "У вас ещё нет сохранённых исполнителей",
                show_alert=True
            )
        else:
            artists_list = "\n".join(f"▫️ {artist}" for artist in artists)
            await update.callback_query.edit_message_text(
                f"🎤 Ваши исполнители:\n\n{artists_list}\n\nВсего: {len(artists)}"
            )
        
        return await self.move(update, context) 

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
                'Создать Список исполнителей',
                ArtistListEdit,
                source_type=SourceTypes.JUMP_SOURCE_TYPE)],
            [Button(
                'Мой список',
                ArtistListShow,
                source_type=SourceTypes.JUMP_SOURCE_TYPE)],
        ]


    
def main():
    """Run the bot."""
    bot = Bot(
        'HammettSimpleJumpBot',
        entry_point=StartScreen,
        states={
            DEFAULT_STATE: {NextScreen, StartScreen, ArtistListEdit, ArtistListShow},
        },
    )
    bot.run()


if __name__ == '__main__':
    main()
