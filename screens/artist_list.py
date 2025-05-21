from screens.base import BaseScreen
from database import get_user_list


class ArtistListShow(BaseScreen):
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
                self._get_back_button()
            ]
        ]