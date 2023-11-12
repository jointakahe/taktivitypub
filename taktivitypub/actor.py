from taktivitypub.base import APObject


class Actor(APObject):
    inbox: str
    outbox: str

    @classmethod
    def make_test(cls):
        return cls(id="a", type="b", inbox="x", outbox="y")
