from pydantic import Field

from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType
from taktivitypub.types import IRI, IRIOrPublic, ISODatetime, ListOrSingle


class Note(APObject):
    """
    A note, commonly actually used as a microblogging post/status
    """

    type: ObjectType = ObjectType.Note

    attributed_to: IRI | None = Field(None, alias="attributedTo")
    cc: ListOrSingle[IRIOrPublic] = []
    content_map: dict[str, str] | None = Field(None, alias="contentMap")
    content: str | None = None
    in_reply_to: IRI | None = Field(None, alias="inReplyTo")
    published: ISODatetime | None = None
    sensitive: bool = False
    to: ListOrSingle[IRIOrPublic] = []
    url: IRI | None = None
