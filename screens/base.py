from hammett.core import Screen, Button
from hammett.core.constants import SourceTypes
from screens.start_screen import  StartScreen


class BaseScreen(Screen):
    @staticmethod
    def _get_back_button():
        return Button(
                    '⬅️ В главное меню',
                    source=StartScreen,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE
                )