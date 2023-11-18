import pytest
from pydantic import ValidationError

from taktivitypub import APObject, Emoji


def test_validate_str_or_map():
    """
    Tests that the StrOrMap type validator works correctly
    """
    # Normal value with name
    emoji = APObject.load(
        {
            "icon": {
                "mediaType": "image/png",
                "type": "Image",
                "url": "https://cdn.masto.host/fediaeracodeorg/custom_emojis/images/"
                "000/007/858/original/2cb223f1f317848b.png",
            },
            "id": "https://fedi.aeracode.org/emojis/7858",
            "name": ":Takahe:",
            "type": "Emoji",
        }
    )
    assert isinstance(emoji, Emoji)
    assert emoji.name == ":Takahe:"

    # NameMap with und
    emoji = APObject.load(
        {
            "icon": {
                "mediaType": "image/png",
                "type": "Image",
                "url": "https://cdn.masto.host/fediaeracodeorg/custom_emojis/images/"
                "000/007/858/original/2cb223f1f317848b.png",
            },
            "id": "https://fedi.aeracode.org/emojis/7858",
            "nameMap": {"und": ":Takahe:"},
            "type": "Emoji",
        }
    )
    assert isinstance(emoji, Emoji)
    assert emoji.name == ":Takahe:"

    # Both missing should be an error
    with pytest.raises(ValidationError):
        APObject.load(
            {
                "icon": {
                    "mediaType": "image/png",
                    "type": "Image",
                    "url": "https://cdn.masto.host/fediaeracodeorg/custom_emojis/images/"
                    "000/007/858/original/2cb223f1f317848b.png",
                },
                "id": "https://fedi.aeracode.org/emojis/7858",
                "type": "Emoji",
            }
        )
