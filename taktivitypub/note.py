from typing import Literal

from pydantic import Field

from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType
from taktivitypub.document import Document
from taktivitypub.emoji import Emoji
from taktivitypub.hashtag import Hashtag
from taktivitypub.mention import Mention
from taktivitypub.types import IRI, ISODatetime, ListOrSingle


class Note(APObject):
    """
    A note, commonly actually used as a microblogging post/status and the
    backbone of the microblogging ActivityPub sphere.
    """

    type: Literal[ObjectType.Note] = ObjectType.Note
    id: IRI

    # The author of this note
    attributed_to: IRI = Field(alias="attributedTo")

    # The actual text of the post/note.
    content: str

    # The time this was published (note that this may be significantly
    # earlier in time than when we received it!)
    published: ISODatetime | None = None

    # If the note has a content warning and/or should have its images hidden
    # by default (on some clients). This is normally only set to True if
    # summary is also supplied. AP extension.
    sensitive: bool = False

    # Specify some concrete subclasses for attachments
    attachments: ListOrSingle[Document] = Field([], alias="attachment")
    tags: ListOrSingle[Hashtag | Mention | Emoji] = Field([], alias="tag")

    # Notes also usually come with these common Object fields:
    # attributed_to
    # cc
    # in_reply_to
    # published
    # summary (used as content warning text)
    # to
    # updated
    # url
