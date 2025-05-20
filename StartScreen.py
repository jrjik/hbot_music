from hammett.core import Button
from hammett.core.constants import SourceTypes
from hammett.core.mixins import StartMixin


START_SCREEN_DESCRIPTION = (
    '🎶 <b>HMusicBot</b>\n'
    '\n'
    'Храните список любимых артистов и получайте информацию о новых релизах:\n'
    '\n'
    '<i>Выберите действие в меню ниже</i>'
)
   
class StartScreen(StartMixin):
    
    description = START_SCREEN_DESCRIPTION

    async def add_default_keyboard(self, _update, _context):

        from ArtistSearch import ArtistSearch
        from ArtistListEdit import ArtistListEdit
        from ArtistListShow import ArtistListShow

        return [
            [Button(
                'Поиск релизов',
                ArtistSearch,
                source_type=SourceTypes.MOVE_SOURCE_TYPE,
            )],
            [Button(
                'Создать Список исполнителей',
                ArtistListEdit,
                source_type=SourceTypes.MOVE_SOURCE_TYPE)],
            [Button(
                'Мой список',
                ArtistListShow,
                source_type=SourceTypes.MOVE_SOURCE_TYPE)],
        ]