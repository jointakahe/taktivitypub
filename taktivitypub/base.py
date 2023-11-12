import pydantic
from taktivitypub.ld import canonicalise
from taktivitypub.exceptions import ActivityPubError
from taktivitypub.constants import ObjectType
import dateutil.parser
import dateutil.tz
import datetime


class APObject(pydantic.BaseModel, validate_assignment=True):
    id: str | None
    type: ObjectType

    allow_null_id = False

    def __init__(self, id: str | None):
        self.id = id

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
        # Extract the ID now
        if "id" not in content:
            raise ActivityPubError("ID is not present")
        instance = object_class(id=content["id"])
        # Dispatch to that class
        instance.parse(content)
        instance.validate()
        return instance

    ### Parsing ###

    @classmethod
    def parse(cls, content: dict):
        """
        Should be overridden in subclasses
        """
        pass

    @classmethod
    def parse_list(cls, container, key) -> list:
        """
        Given a JSON-LD value (that can be either a list, or a dict if it's just
        one item), always returns a list"""
        if key not in container:
            return []
        value = container[key]
        if not isinstance(value, list):
            return [value]
        return value

    @classmethod
    def parse_date(cls, value: str | None) -> datetime.datetime | None:
        if value is None:
            return None
        return dateutil.parser.isoparse(value).replace(microsecond=0)

    ### Validation ###

    def validate(self):
        """
        Ensures this object is valid
        """
        self.validate_iri(self.id, noun="id", allow_none=self.allow_null_id)

    @classmethod
    def validate_date(cls, value, noun, allow_none=False):
        """
        Checks if the value is a valid date with a UTC timezone.
        """
        if not isinstance(value, datetime.datetime):
            if value is None and allow_none:
                return
            raise ActivityPubError(f"{noun} is not a datetime")
        if value.tzinfo is None:
            raise ActivityPubError(f"{noun} has no timezone set")
        if value.tzinfo != dateutil.tz.tzutc():
            raise ActivityPubError(f"{noun} has a non-UTC timezone")

    @classmethod
    def validate_iri(cls, value, noun, allow_none=False, allow_as_public=False):
        """
        Checks if the value looks like a valid IRI
        """
        if value is None and allow_none:
            return
        if not isinstance(value, str):
            raise ActivityPubError(f"{noun} is not a string")
        # Yes, I know I can do better
        if "://" not in value:
            if allow_as_public:
                if value != "as:Public":
                    raise ActivityPubError(
                        f"{noun} is not a valid IRI string or 'as:Public'"
                    )
            else:
                raise ActivityPubError(f"{noun} is not a valid IRI string")
