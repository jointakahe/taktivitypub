from typing import Literal

from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType


class Mention(APObject):
    """
    Mentioning another user.

    This is a built-in ActivityPub object type that extends Link; most
    server implementations just send "name" and "href", though.
    """

    type: Literal[ObjectType.Mention] = ObjectType.Mention

    # The handle of the user - e.g. "@takahe@jointakahe.org"
    # This may not match the actual text of the mention in the Note; you should
    # instead look for links to the "href" value here. Don't rely on this.
    name: str | None = None

    # The Actor ID (IRI) of the other profile
    href: str
