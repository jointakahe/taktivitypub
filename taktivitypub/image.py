from typing import Literal

from pydantic import Field

from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType


class Image(APObject):
    """
    An image.

    Weirdly not used by Mastodon when attaching images to Notes (those are
    Documents), but is used as part of Emoji.
    """

    type: Literal[ObjectType.Image] = ObjectType.Image

    media_type: str = Field("application/octet-stream", alias="mediaType")
    url: str
