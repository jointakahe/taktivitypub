import datetime
from taktivitypub.base import APObject
from taktivitypub.ld import get_list, parse_ld_date
from taktivitypub.constants import ObjectType
from taktivitypub.exceptions import ActivityPubError


class Note(APObject):
    """
    A note, commonly actually used as a microblogging post/status
    """

    type = ObjectType.Note

    to: list[str] = []
    cc: list[str] = []
    url: str | None = None
    in_reply_to: str | None = None
    published: datetime.datetime | None = None
    sensitive: bool = False
    attributed_to: str | None

    ### Parsing ###

    def parse(self, content: dict):
        super().parse(content)
        # Addressing
        self.to = self.parse_list(content, "to")
        self.cc = self.parse_list(content, "cc")
        # Dates
        self.published = self.parse_date(content.get("published"))
        # Content
        self.sensitive = content.get("sensitive", False)

    ### Validation ###

    def validate(self):
        super().validate()
        # Handle addressing
        self.to = self.validate_to_value(self.to, noun="to")
        self.cc = self.validate_to_value(self.cc, noun="to")
        # Handle dates
        self.validate_date(self.published, noun="published", allow_none=True)

    def validate_to_value(self, value, noun) -> list[str]:
        """
        Ensures a value is a list and that it contains only IRIs or as:Public
        """
        if value is None:
            return []
        if isinstance(value, str):
            value = [value]
        if not isinstance(value, list):
            raise ActivityPubError(f"{noun} values must be a list or single string")
        for item in value:
            self.validate_iri(item, f"{noun} value", allow_as_public=True)
        return value

    ### Dumping ###
