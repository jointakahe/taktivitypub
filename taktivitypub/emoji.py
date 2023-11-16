from typing import Literal

from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType
from taktivitypub.image import Image
from taktivitypub.types import IRI, ISODatetime


class Emoji(APObject):
    """
    A custom emoji that is not from the Unicode emoji set.

    These are a Mastodon-specced extension, typed as http://joinmastodon.org/ns#Emoji.
    Our context sets it up so we see it as just Emoji.
    """

    id: IRI

    type: Literal[ObjectType.Emoji] = ObjectType.Emoji

    # The text that gets replaced with the emoji in the post - this includes
    # delimiters, e.g. ":takahe:"
    name: str

    # Optional updated field - lets servers cache the emoji locally and flush
    # them through if it changes
    updated: ISODatetime | None

    # The actual emoji
    icon: Image
