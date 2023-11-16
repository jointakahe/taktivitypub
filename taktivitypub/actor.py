from typing import Literal

from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType
from taktivitypub.types import IRI


class Actor(APObject):
    type: Literal[ObjectType.Actor, ObjectType.Person] = ObjectType.Actor
    id: IRI

    inbox: IRI
    outbox: IRI
