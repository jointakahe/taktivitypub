import enum


class ObjectType(enum.StrEnum):
    Note = "Note"
    Actor = "Actor"

    @classmethod
    def by_iname(cls, value):
        """
        Case-insensitive value retrieval
        """
        for item in cls:
            if item.lower() == value.lower():
                return item
