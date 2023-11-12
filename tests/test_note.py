import datetime
from taktivitypub.note import Note
from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType


def test_note_1(json_file):
    # Load note
    note_1 = json_file("note-1-mastodon")
    instance = APObject.load(note_1)
    # Make sure it came out right
    assert isinstance(instance, Note)
    assert instance.type == ObjectType.Note
    assert (
        instance.id
        == "https://fedi.aeracode.org/users/andrew/statuses/111382013467212873"
    )
    assert instance.to == ["as:Public"]
    assert instance.cc == ["https://fedi.aeracode.org/users/andrew/followers"]
    assert instance.published == datetime.datetime(
        2023, 11, 9, 18, 30, 48, tzinfo=datetime.timezone.utc
    )
