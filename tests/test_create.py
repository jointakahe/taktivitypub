import datetime

from taktivitypub import APObject, Create, Note, ObjectType


def test_create_note_mastodon_followersonly(json_file):
    """
    Tests basic note parsing
    """
    # Load note
    json_data = json_file("create-note-mastodon-followeronly")
    create = APObject.load(json_data)

    # Check the outer create object
    assert isinstance(create, Create)
    assert create.type == ObjectType.Create
    assert (
        create.id
        == "https://fedi.aeracode.org/users/testmover/statuses/110758610463118408/activity"
    )
    assert create.to == ["https://fedi.aeracode.org/users/testmover/followers"]
    assert create.cc == []
    assert create.published == datetime.datetime(
        2023, 7, 22, 16, 11, 13, tzinfo=datetime.UTC
    )

    # It should have an embedded Note object
    assert isinstance(create.object, Note)
    assert create.object.content == "<p>This is a followers-only post!</p>"
