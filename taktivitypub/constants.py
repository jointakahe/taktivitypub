import enum


class ObjectType(enum.StrEnum):
    Accept = "Accept"
    Actor = "Actor"
    Add = "Add"
    Announce = "Announce"
    Block = "Block"
    Collection = "Collection"
    CollectionPage = "CollectionPage"
    Create = "Create"
    Delete = "Delete"
    Document = "Document"
    Emoji = "Emoji"
    Flag = "Flag"
    Follow = "Follow"
    Hashtag = "Hashtag"
    Image = "Image"
    Like = "Like"
    Mention = "Mention"
    Move = "Move"
    Note = "Note"
    Person = "Person"
    Reject = "Reject"
    Remove = "Remove"
    Undo = "Undo"
    Update = "Update"

    @classmethod
    def by_iname(cls, value):
        """
        Case-insensitive value retrieval
        """
        for item in cls:
            if item.lower() == value.lower():
                return item
