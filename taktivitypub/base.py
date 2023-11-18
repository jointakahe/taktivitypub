import pydantic
from pydantic import Field, model_validator

from taktivitypub.constants import ObjectType
from taktivitypub.exceptions import ActivityPubError
from taktivitypub.ld import canonicalise, get_map_value
from taktivitypub.types import IRI, IRIOrPublic, ISODatetime, ListOrSingle


class APObject(pydantic.BaseModel):
    """
    A base schema representing a generic ActivityPub object.

    Not all of the base Object properties are on here due to how they
    are generally used, but many are.
    """

    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        validate_default=True,
        validate_return=True,
    )

    type: ObjectType

    # Who the object is to - either Actor IRIs or the special ActivityPub
    # public value, which our context turns into "as:Public".
    # To and cc behave functionally the same for delivery, but they influence
    # whether Mastodon sees posts as "public" (there is an "as:Public" in
    # to) or "unlisted" (there is an "as:Public" in cc)
    to: ListOrSingle[IRIOrPublic] = []
    cc: ListOrSingle[IRIOrPublic] = []

    # Name is a base property, though it's not used by a ton of object types;
    # those that do need it will mostly re-declare this as a non-None string.
    name: str | None = None
    nameMap: dict[str, str] | None = None

    # Content - usually only provided for things like Notes or Pages.
    # This and name can both have language-tagged alternates; generally, most
    # servers will just use and provide one value in one language, though.
    content: str | None = None
    content_map: dict[str, str] | None = Field(None, alias="contentMap")

    # Content summary, but also used as content warnings for Notes
    summary: str | None = None

    # The author of this object, as their Actor IRI
    attributed_to: IRI | None = Field(None, alias="attributedTo")

    # If this is a reply to another Object, the IRI of that object
    in_reply_to: IRI | None = Field(None, alias="inReplyTo")

    # When the object was last considered updated by its source (this could
    # be in the past or in some buggy cases, the near future)
    updated: ISODatetime | None = None

    # Attached images or other items, usually as Document objects.
    attachments: ListOrSingle["APObject"] = Field([], alias="attachment")

    # Hashtags, mentions, emoji, and more.
    tags: ListOrSingle["APObject"] = Field([], alias="tag")

    # The web URL of the object, where it can be viewed.
    # May be different to the ID IRI, but can also be the same.
    url: IRI | None = None

    # The content type of the object, if applicable
    media_type: str | None = None

    # Pull any nameMap/contentMap values out as a default, if they're in there
    @model_validator(mode="before")
    def validate_maps(cls, data):
        if not data.get("name") and data.get("nameMap"):
            data["name"] = get_map_value(data["nameMap"])
        if not data.get("content") and data.get("contentMap"):
            data["content"] = get_map_value(data["contentMap"])
        return data

    @classmethod
    def load(cls, content: dict) -> "APObject":
        """
        Parses an ActivityPub message and returns the specific APObject
        subclass that represents it.
        """
        from taktivitypub import TYPE_MAPPING

        # Run it through the canonicaliser to standardise all the keys
        content = canonicalise(content)

        # Extract type
        if "type" not in content:
            raise ActivityPubError("Type is not present")
        if not isinstance(content["type"], str):
            raise ActivityPubError("Type is not a string")
        type_name = ObjectType.by_iname(content["type"])

        # Work out the class to use based on the type
        object_class = TYPE_MAPPING.get(type_name)
        if object_class is None:
            raise ActivityPubError(f"Unknown type {type_name}")

        return object_class(**content)

    def dump(self):
        """
        Dumps out an ActivityPub message as a JSON-compatible dict
        after making sure it's valid
        """
        self.model_validate(self)
        content = self.model_dump(mode="json", by_alias=True)
        content = canonicalise(content)
        return content


class Tombstone(APObject):
    """
    The shell of a deleted object. Will only contain the deleted object's
    ID, and usually nothing else.
    """

    id: IRI
