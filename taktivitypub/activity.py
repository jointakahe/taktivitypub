from typing import Annotated, Literal

from pydantic.functional_serializers import PlainSerializer
from pydantic.functional_validators import BeforeValidator

from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType
from taktivitypub.types import (
    IRI,
    ISODatetime,
    serialize_iri_or_object,
    validate_iri_or_object,
)

# We have to define this here to avoid circular imports
IRIOrObject = Annotated[
    str | APObject,
    BeforeValidator(validate_iri_or_object),
    PlainSerializer(serialize_iri_or_object),
]


class Activity(APObject):
    """
    A generic ActivityPub activity, represnting something happening.

    The object can either be embedded or be represented as just an IRI,
    depending on the server and what it is.
    """

    type: Literal[
        ObjectType.Accept,
        ObjectType.Announce,
        ObjectType.Block,
        ObjectType.Create,
        ObjectType.Delete,
        ObjectType.Follow,
        ObjectType.Like,
        ObjectType.Move,
        ObjectType.Undo,
        ObjectType.Update,
    ]

    id: IRI

    # The Actor IRI of the entity that is publishing the activity.
    # Note that this does not necessarily have to match any authorship attached
    # to the object, for example attributedTo on Note, so if you care about
    # that sort of stuff you should do an extra check when consuming them.
    actor: IRIOrObject

    # The embedded object or IRI referencing it
    object: IRIOrObject

    # If the activity takes a target, the thing it is targeting
    target: IRIOrObject | None = None

    # The time that the create was itself created; can be far in the past,
    # and also does not need to match any embedded dates in the object.
    published: ISODatetime | None = None

    @property
    def actor_iri(self) -> str:
        if isinstance(self.actor, str):
            return self.actor
        return self.actor.id

    @property
    def object_iri(self) -> str:
        if isinstance(self.object, str):
            return self.object
        return self.object.id

    @property
    def target_iri(self) -> str | None:
        if self.target is None:
            return None
        if isinstance(self.target, str):
            return self.target
        return self.target.id


class Create(Activity):
    """
    An activity that signifies that the "object" was created.
    Usually used when an object is first published.
    """

    type: Literal[ObjectType.Create] = ObjectType.Create


class Delete(Activity):
    """
    An activity that signifies that the "object" was deleted.
    You'll often find a Tombstone as the object, that just has the IRI ID
    of the thing that vanished and nothing else.
    """

    type: Literal[ObjectType.Delete] = ObjectType.Delete


class Follow(Activity):
    """
    An actor trying to follow another actor.
    Usually warrants an Accept or Reject activity as a response.
    """

    type: Literal[ObjectType.Follow] = ObjectType.Follow
