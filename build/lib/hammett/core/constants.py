"""The module contains the constants used in the core."""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING, TypedDict, cast

if TYPE_CHECKING:
    from os import PathLike

    from hammett.types import Attachments, Document, Keyboard, State

# Use 'cast' instead of 'State(0)' to avoid a circular import
DEFAULT_STATE = cast('State', '0')

EMPTY_KEYBOARD: 'Keyboard' = []

LATEST_SENT_MSG_KEY = 'latest_sent_msg'


class SourceTypes(Enum):
    """The class contains the available types of sources."""

    HANDLER_SOURCE_TYPE = auto()
    JUMP_ALONG_ROUTE_SOURCE_TYPE = auto()
    JUMP_SOURCE_TYPE = auto()
    MOVE_ALONG_ROUTE_SOURCE_TYPE = auto()
    MOVE_SOURCE_TYPE = auto()
    URL_SOURCE_TYPE = auto()
    WEB_APP_SOURCE_TYPE = auto()


@dataclass
class RenderConfig:
    """The class that represents a config for the Screen render method."""

    chat_id: int | None = 0
    message_id: int = 0
    as_new_message: bool = False
    cache_covers: bool = False
    cover: 'str | PathLike[str]' = ''
    description: str = ''
    attachments: 'Attachments | None' = None
    document: 'Document | None' = None
    keyboard: 'Keyboard | None' = None
    hide_keyboard: bool = False


@dataclass
class FinalRenderConfig(RenderConfig):
    """The class represents a final config intended for
    the Screen render method.
    """

    keyboard: 'Keyboard' = field(default_factory=list)


class LatestMessage(TypedDict):
    """The class represents information about the latest message sent."""

    chat_id: int
    message_id: int
    hide_keyboard: bool
