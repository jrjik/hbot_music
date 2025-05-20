from hammett.core import Bot, Button, Screen
from hammett.core.constants import DEFAULT_STATE, RenderConfig, SourceTypes
from hammett.core.mixins import StartMixin
from hammett.core.handlers import register_typing_handler
from hammett.core.handlers import register_button_handler

from StartScreen import StartScreen

from database import get_user_list


class ArtistListShow(Screen):
    async def get_description(self, update, context, **kwargs):
        user_id = update.callback_query.from_user.id if update.callback_query else update.message.from_user.id
        artists = get_user_list(user_id)
        
        if not artists:
            return "🎤 Ваш список исполнителей пуст"
            
        artists_list = "\n".join(f"▫️ {artist}" for artist in artists)
        return f"🎤 Ваши исполнители:\n\n{artists_list}\n\nВсего: {len(artists)}"

    async def add_default_keyboard(self, update, context):
        return [
            [
                Button(
                    '⬅️ В главное меню',
                    source=StartScreen,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE
                )
            ]
        ]