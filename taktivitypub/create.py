from typing import Literal

from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType
from taktivitypub.note import Note
from taktivitypub.types import IRI, IRIOrPublic, ISODatetime, ListOrSingle


class Create(APObject):
    """
    A note, commonly actually used as a microblogging post/status
    """

    type: Literal[ObjectType.Create] = ObjectType.Create

    id: IRI

    actor: IRI
    cc: ListOrSingle[IRIOrPublic] = []
    object: IRI | Note
    published: ISODatetime
    to: ListOrSingle[IRIOrPublic] = []
