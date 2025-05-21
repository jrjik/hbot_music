import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from hammett.core import Button
from hammett.core.constants import DEFAULT_STATE, SourceTypes
from hammett.core.handlers import register_button_handler
from screens.base import BaseScreen

from database import get_user_list


class ArtistSearch(BaseScreen):
    async def get_description(self, update, context, **kwargs):
        if 'spotify_results' in context.user_data:
            return self._format_results(context.user_data['spotify_results'])
        return "Нажмите кнопку для поиска релизов"

    async def add_default_keyboard(self, update, context):
        return [
            [
                Button(
                    '🔍 Найти релизы',
                    source=self.search_releases_handler,
                    source_type=SourceTypes.HANDLER_SOURCE_TYPE
                )
            ],
            [
                self._get_back_button()
            ]
        ]

    @register_button_handler
    async def search_releases_handler(self, update, context):
        user_id = update.callback_query.from_user.id
        artists = get_user_list(user_id)

        if not artists:
            await update.callback_query.answer("Нет исполнителей для поиска", show_alert=True)
            return

        results = await self._fetch_spotify_data(artists, "2023-11-10")
        context.user_data['spotify_results'] = results

        return await self.move(update, context)

    async def _fetch_spotify_data(self, artists, target_date):
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
        if not results:
            return "На указанную дату релизов не найдено"

        message = "🎵 Найденные релизы (2023-11-10):\n\n"
        for artist, releases in results.items():
            message += f"🎤 {artist}:\n"
            for release in releases:
                message += f"▫️ {release['name']} ({release['album_type']})\n"
                message += f"   Ссылка: {release['external_urls']['spotify']}\n\n"

        return message