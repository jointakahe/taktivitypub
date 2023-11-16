from typing import Literal

from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType


class Hashtag(APObject):
    """
    A #hashtag.

    These are an extension to ActivityStreams, typed as
    https://www.w3.org/ns/activitystreams#Hashtag, but our context just aliases
    that to Hashtag. I suspect that, like Mentions, they are meant to be Link
    subclasses, which is why there's a href in there.
    """

    type: Literal[ObjectType.Hashtag] = ObjectType.Hashtag

    # The text of the hashtag with the preceding hash, e.g. "#mosstodon"
    # TODO: Support nameMap
    # TODO: Support "tag"/"tagMap" as the attribute, not "name", for kbin
    name: str

    # Link to a timeline of the tag, usually local to the source instance
    # Not very useful to most server implementations.
    href: str | None = None
