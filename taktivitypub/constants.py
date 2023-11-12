import enum


class ObjectType(enum.StrEnum):
    Accept = "Accept"
    Actor = "Actor"
    Add = "Add"
    Announce = "Announce"
    Block = "Block"
    Create = "Create"
    Delete = "Delete"
    Flag = "Flag"
    Follow = "Follow"
    Like = "Like"
    Move = "Move"
    Note = "Note"
    Reject = "Reject"
    Remove = "Remove"
    Person = "Person"
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
