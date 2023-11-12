from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType
from taktivitypub.types import IRIOrObject


class Follow(APObject):
    """
    A follow object, which may or may not contain an embedded Actor.
    """

    type: ObjectType = ObjectType.Follow

    actor: IRIOrObject
    object: IRIOrObject
