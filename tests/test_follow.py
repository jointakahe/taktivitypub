from taktivitypub import Actor, APObject, Follow
from taktivitypub.constants import ObjectType


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
    assert instance.actor_iri == "https://fedi.aeracode.org/users/andrew"
    assert instance.object_iri == "https://takahe.social/@admin@takahe.social/"


def test_make_embedded_follow():
    """
    Tests that we can correctly construct a follow with one ID and one embedded
    object.
    """

    # Build the follow
    follow = Follow.model_construct()
    follow.id = "https://example.com/follow/1"
    follow.actor = Actor.model_construct(id="https://example.com/user/1")
    follow.object = "https://example.org/user/2"
    data = follow.dump()

    # Check the output
    assert data["type"] == "Follow"
    assert data["id"] == "https://example.com/follow/1"
    assert data["actor"]["id"] == "https://example.com/user/1"
    assert data["object"] == "https://example.org/user/2"
    assert "attachment" not in data
