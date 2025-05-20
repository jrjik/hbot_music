from hammett.core import Bot, Button, Screen
from hammett.core.constants import DEFAULT_STATE, RenderConfig, SourceTypes
from hammett.core.handlers import register_typing_handler

from database import save_user_list

from StartScreen import StartScreen

ARTISTLIST_SCREEN_DESCRIPTION = (
    'Перечисли список любимых исполнителей через пробел'
    '\n'
    'Ниже ты можешь вернуться на начальный экран'
)


class ArtistListEdit(Screen):

    description = ARTISTLIST_SCREEN_DESCRIPTION

    async def add_default_keyboard(self, _update, _context):
        return [[
            Button(
                '⬅️ Назад',
                StartScreen,
                source_type=SourceTypes.MOVE_SOURCE_TYPE,
            ),
            
        ]]


    @register_typing_handler
    async def handle_text_input(self, update, context):
        user_id = update.message.from_user.id  
        user_text = update.message.text
        items = [item.strip() for item in user_text.split(",")]
        
        save_user_list(user_id, items)
        
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