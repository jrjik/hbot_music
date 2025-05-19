"""The module is a script for running the bot."""
import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from hammett.core import Bot, Button, Screen
from hammett.core.constants import DEFAULT_STATE, RenderConfig, SourceTypes
from hammett.core.mixins import StartMixin
from hammett.core.handlers import register_typing_handler
from hammett.core.handlers import register_button_handler


from database import save_user_list  # Импортируем нашу функцию
from database import get_user_list

load_dotenv()


START_SCREEN_DESCRIPTION = (
    '🎶 <b>HMusicBot</b>\n'
    '\n'
    'Храните список любимых артистов и получайте информацию о новых релизах:\n'
    '\n'
    '<i>Выберите действие в меню ниже</i>'
)

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
    
       
class ArtistListShow(Screen):
    async def get_description(self, update, context, **kwargs):
        user_id = update.callback_query.from_user.id if update.callback_query else update.message.from_user.id
        artists = get_user_list(user_id)
        
        if not artists:
            return "🎤 Ваш список исполнителей пуст"
            
        artists_list = "\n".join(f"▫️ {artist}" for artist in artists)
        return f"🎤 Ваши исполнители:\n\n{artists_list}\n\nВсего: {len(artists)}"

    async def add_default_keyboard(self, update, context):
        """Создаем клавиатуру с кнопкой возврата"""
        return [
            [
                Button(
                    '⬅️ В главное меню',
                    source=StartScreen,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE
                )
            ]
        ]
        

class StartScreen(StartMixin):
    description = START_SCREEN_DESCRIPTION

    async def add_default_keyboard(self, _update, _context):
        return [
            [Button(
                'Поиск релизов',
                ArtistSearch,
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


class ArtistSearch(Screen):
    async def get_description(self, update, context, **kwargs):
        """Динамическое описание экрана с результатами поиска"""
        if 'spotify_results' in context.user_data:
            return self._format_results(context.user_data['spotify_results'])
        return "Нажмите кнопку для поиска релизов"

    async def add_default_keyboard(self, update, context):
        """Клавиатура с кнопкой поиска и возврата"""
        return [
            [
                Button(
                    '🔍 Найти релизы',
                    source=self.search_releases_handler,
                    source_type=SourceTypes.HANDLER_SOURCE_TYPE
                )
            ],
            [
                Button(
                    '⬅️ Назад',
                    StartScreen,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE
                )
            ]
        ]

    @register_button_handler
    async def search_releases_handler(self, update, context):
        """Обработчик поиска релизов"""
        user_id = update.callback_query.from_user.id
        artists = get_user_list(user_id)  
        
        if not artists:
            await update.callback_query.answer("Нет исполнителей для поиска", show_alert=True)
            return
        
        results = await self._fetch_spotify_data(artists, "2023-11-10")
        context.user_data['spotify_results'] = results
        
        return await self.move(update, context)

    async def _fetch_spotify_data(self, artists, target_date):
        """Запрос к Spotify API"""
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        results = {}
        for artist in artists:
            try:
                query = f"artist:{artist} year:2023"
                releases = sp.search(q=query, type='album', limit=10)
                
                matched_releases = [
                    item for item in releases['albums']['items']
                    if item['release_date'] == target_date
                ]
                
                if matched_releases:
                    results[artist] = matched_releases
            except Exception as e:
                print(f"Ошибка при запросе для {artist}: {e}")
        
        return results

    def _format_results(self, results):
        """Форматирование результатов для вывода"""
        if not results:
            return "На указанную дату релизов не найдено"
            
        message = "🎵 Найденные релизы (2023-11-10):\n\n"
        for artist, releases in results.items():
            message += f"🎤 {artist}:\n"
            for release in releases:
                message += f"▫️ {release['name']} ({release['album_type']})\n"
                message += f"   Ссылка: {release['external_urls']['spotify']}\n\n"
        
        return message
    
def main():
    """Run the bot."""
    bot = Bot(
        'HammettSimpleJumpBot',
        entry_point=StartScreen,
        states={
            DEFAULT_STATE: {StartScreen, ArtistListEdit, ArtistListShow, ArtistSearch},
        },
    )
    bot.run()


if __name__ == '__main__':
    main()
