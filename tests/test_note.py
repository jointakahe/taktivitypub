import datetime

from taktivitypub import APObject, Document, Emoji, Hashtag, Mention, Note, ObjectType


def test_note_mastodon_basic(json_file):
    """
    Tests basic note parsing
    """
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

    # It should have one attachment with a known URL
    assert len(instance.attachments) == 1
    attachment = instance.attachments[0]
    assert isinstance(attachment, Document)
    assert (
        attachment.url
        == "https://cdn.masto.host/fediaeracodeorg/media_attachments/files/111/"
        "354/062/557/131/802/original/cdc8d0e5a12e4994.jpg"
    )
    assert attachment.width == 2922
    assert attachment.height == 2839
    assert (
        attachment.name
        == "A 2U rackmount server with its top cover off. Various electronics "
        "are visible inside, and the front drive bays have two caddies and ten empty spaces."
    )
    assert attachment.blurhash == "UPFFZ}kCaxxt01j[WBWB9ZaeofWB_2WUNGbH"
    assert attachment.media_type == "image/jpeg"
    assert attachment.focal_point is None


def test_note_mastodon_tag_photo(json_file):
    """
    Tests that a more complex post with lots of attachments and photos works
    """
    # Load note
    json_data = json_file("note-mastodon-tag-photo")
    instance = APObject.load(json_data)
    assert isinstance(instance, Note)

    # It should have two attachments
    assert len(instance.attachments) == 2

    # Sort them by URL so we get a predictable one first
    instance.attachments.sort(key=lambda a: a.url)
    assert (
        instance.attachments[0].url
        == "https://cdn.masto.host/fediaeracodeorg/media_attachments/files/111/"
        "416/866/159/228/600/original/e0e1fede28d4b4a4.jpg"
    )
    assert instance.attachments[0].focal_point == (0, 0)

    # There should be four tags (two hashtags, one emoji and one mention)
    assert len(instance.tags) == 4

    # Get the mention
    mention = [x for x in instance.tags if x.type == ObjectType.Mention][0]
    assert isinstance(mention, Mention)
    assert mention.name == "@takahe@jointakahe.org"
    assert mention.href == "https://jointakahe.takahe.social/@takahe@jointakahe.org/"

    # Get the emoji
    emoji = [x for x in instance.tags if x.type == ObjectType.Emoji][0]
    assert isinstance(emoji, Emoji)
    assert emoji.name == ":Takahe:"
    assert (
        emoji.icon.url
        == "https://cdn.masto.host/fediaeracodeorg/custom_emojis/images/000/007/858/original/2cb223f1f317848b.png"
    )

    # Get the alphabetically first hashtag
    hashtag = [
        x
        for x in sorted(instance.tags, key=lambda i: i.name)
        if x.type == ObjectType.Hashtag
    ][0]
    assert isinstance(hashtag, Hashtag)
    assert hashtag.name == "#hashtags"


def test_note_firefish(json_file):
    """
    Tests a Firefish (Calckey) note
    """
    json_data = json_file("note-firefish")
    note = APObject.load(json_data)
    assert note.attributed_to == "https://firefish.social/users/9aprgabaeb"


def test_note_python_everything():
    """
    Creates a new Note from Python and ensures it looks correct
    """
    note = Note.model_construct(
        id="https://example.com/notes/1/",
        attributed_to="https://fedi.aeracode.org/users/andrew",
    )
    note.content = "<p>This is my test note.</p>"
    note.tags = [
        Hashtag.model_construct(name="#hashtag"),
        Mention.model_construct(
            name="@takahe@jointakahe.org",
            href="https://jointakahe.takahe.social/@takahe@jointakahe.org/",
        ),
    ]
    json_data = note.dump()

    # Validate content
    assert json_data["content"] == "<p>This is my test note.</p>"
    assert json_data["attributedTo"] == "https://fedi.aeracode.org/users/andrew"
