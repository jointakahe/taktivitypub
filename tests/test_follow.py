from taktivitypub.base import APObject
from taktivitypub.constants import ObjectType
from taktivitypub.follow import Follow


def test_follow_mastodon(json_file):
    """
    Tests a Mastodon-style follow with no embedded objects
    """

    # Load JSON
    json_data = json_file("follow-mastodon")
    instance = APObject.load(json_data)

    # Make sure it came out right on the Python side
    assert isinstance(instance, Follow)
    assert instance.type == ObjectType.Follow
    assert (
        instance.id == "https://fedi.aeracode.org/0f479df8-02bc-4314-94c9-400004944282"
    )
    assert instance.actor == "https://fedi.aeracode.org/users/andrew"
    assert instance.object == "https://takahe.social/@admin@takahe.social/"

    # Re-serialize it and check it looks right
    json_data = instance.dump()
    assert json_data["type"] == "Follow"
    assert (
        json_data["id"]
        == "https://fedi.aeracode.org/0f479df8-02bc-4314-94c9-400004944282"
    )
    assert json_data["actor"] == "https://fedi.aeracode.org/users/andrew"
    assert json_data["object"] == "https://takahe.social/@admin@takahe.social/"


def test_follow_with_embed(json_file):
    """
    Tests a follow where one of the Actors is embedded
    """

    # Load JSON
    json_data = json_file("follow-with-embed")
    instance = APObject.load(json_data)

    # Make sure it came out right on the Python side
    assert isinstance(instance, Follow)
    assert instance.type == ObjectType.Follow
    assert instance.actor == "https://fedi.aeracode.org/users/andrew"
    assert instance.object == "https://takahe.social/@admin@takahe.social/"
