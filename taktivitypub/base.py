import pydantic

from taktivitypub.constants import ObjectType
from taktivitypub.exceptions import ActivityPubError
from taktivitypub.ld import canonicalise
from taktivitypub.types import IRI


class APObject(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        validate_default=True,
        validate_return=True,
    )

    id: IRI | None
    type: ObjectType

    @classmethod
    def load(cls, content: dict) -> "APObject":
        """
        Parses an ActivityPub message and returns the specific APObject
        subclass that represents it.
        """
        from taktivitypub.actor import Actor
        from taktivitypub.note import Note

        # Run it through the canonicaliser to standardise all the keys
        content = canonicalise(content)

        # Extract type
        if "type" not in content:
            raise ActivityPubError("Type is not present")
        if not isinstance(content["type"], str):
            raise ActivityPubError("Type is not a string")
        type_name = ObjectType.by_iname(content["type"])

        # Work out the class to use based on the type
        if type_name == ObjectType.Actor:
            object_class = Actor
        if type_name == ObjectType.Note:
            object_class = Note
        else:
            raise ActivityPubError(f"Unknown type {type_name}")

        return object_class(**content)

    def dump(self):
        """
        Dumps out an ActivityPub message as a JSON-compatible dict
        after making sure it's valid
        """
        content = self.model_dump(mode="json", by_alias=True)
        content = canonicalise(content)
        return content
