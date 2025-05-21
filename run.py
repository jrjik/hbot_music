"""The module is a script for running the bot."""
from screens.search_releases import ArtistSearch
from screens.artist_list_edit import ArtistListEdit
from screens.artist_list import ArtistListShow
from screens.start_screen import StartScreen

from dotenv import load_dotenv
from hammett.core import Bot
from hammett.core.constants import DEFAULT_STATE

load_dotenv()

               
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
