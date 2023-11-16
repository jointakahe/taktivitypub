from typing import Literal

from pydantic import Field

from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType


class Document(APObject):
    """
    A note, commonly actually used as a microblogging post/status
    """

    type: Literal[ObjectType.Document] = ObjectType.Document

    media_type: str = Field("application/octet-stream", alias="mediaType")
    url: str
    name: str | None = None
    width: int | None = None
    height: int | None = None
    blurhash: str | None = None
    focal_point: tuple[float, float] | None = Field(None, alias="focalPoint")
