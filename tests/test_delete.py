from taktivitypub import APObject, Delete, ObjectType, Tombstone


def test_delete_tombstone(json_file):
    """
    Tests basic note parsing
    """
    # Load note
    json_data = json_file("delete-tombstone")
    delete = APObject.load(json_data)

    # Check the outer create object
    assert isinstance(delete, Delete)
    assert delete.type == ObjectType.Delete
    assert isinstance(delete.object, Tombstone)
    assert delete.object.type == ObjectType.Tombstone
    assert delete.actor_iri == "https://fedi.aeracode.org/users/testmover"
    assert delete.to == ["as:Public"]
