from taktivitypub.actor import Actor
from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType
from taktivitypub.create import Create
from taktivitypub.document import Document
from taktivitypub.emoji import Emoji
from taktivitypub.follow import Follow
from taktivitypub.hashtag import Hashtag
from taktivitypub.mention import Mention
from taktivitypub.note import Note

__version__ = "0.1"


TYPE_MAPPING: dict[ObjectType, type[APObject]] = {
    ObjectType.Actor: Actor,
    ObjectType.Create: Create,
    ObjectType.Document: Document,
    ObjectType.Emoji: Emoji,
    ObjectType.Follow: Follow,
    ObjectType.Hashtag: Hashtag,
    ObjectType.Mention: Mention,
    ObjectType.Note: Note,
    ObjectType.Person: Actor,
}
