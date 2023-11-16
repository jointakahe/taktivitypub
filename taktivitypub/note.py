from typing import Literal

from pydantic import Field

from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType
from taktivitypub.document import Document
from taktivitypub.emoji import Emoji
from taktivitypub.hashtag import Hashtag
from taktivitypub.mention import Mention
from taktivitypub.types import IRI, IRIOrPublic, ISODatetime, ListOrSingle


class Note(APObject):
    """
    A note, commonly actually used as a microblogging post/status
    """

    type: Literal[ObjectType.Note] = ObjectType.Note
    id: IRI

    attachments: ListOrSingle[Document] = Field([], alias="attachment")
    attributed_to: IRI | None = Field(None, alias="attributedTo")
    cc: ListOrSingle[IRIOrPublic] = []
    content_map: dict[str, str] | None = Field(None, alias="contentMap")
    content: str | None = None
    in_reply_to: IRI | None = Field(None, alias="inReplyTo")
    published: ISODatetime | None = None
    sensitive: bool = False
    tags: ListOrSingle[Hashtag | Mention | Emoji] = Field([], alias="tag")
    to: ListOrSingle[IRIOrPublic] = []
    url: IRI | None = None
