from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType
from taktivitypub.types import IRI


class Actor(APObject):
    type: ObjectType = ObjectType.Actor
    inbox: IRI
    outbox: IRI
