import datetime

from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType
from taktivitypub.note import Note


def test_note_mastodon_basic(json_file):
    # Load note
    json_data = json_file("note-mastodon-basic")
    instance = APObject.load(json_data)

    # Make sure it came out right on the Python side
    assert isinstance(instance, Note)
    assert instance.type == ObjectType.Note
    assert (
        instance.id
        == "https://fedi.aeracode.org/users/andrew/statuses/111354066078688049"
    )
    assert instance.to == ["as:Public"]
    assert instance.cc == ["https://fedi.aeracode.org/users/andrew/followers"]
    assert instance.published == datetime.datetime(
        2023, 11, 4, 20, 3, 25, tzinfo=datetime.UTC
    )

    # Re-serialize it and check it looks right
    json_data = instance.dump()
    assert json_data["published"] == "2023-11-04T20:03:25Z"
    assert json_data["to"] == "as:Public"
