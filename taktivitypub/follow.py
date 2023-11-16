from typing import Literal

from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType
from taktivitypub.types import IRI, IRIOrObject


class Follow(APObject):
    """
    A follow object, which may or may not contain an embedded Actor.
    """

    type: Literal[ObjectType.Follow] = ObjectType.Follow
    id: IRI

    actor: IRIOrObject
    object: IRIOrObject
