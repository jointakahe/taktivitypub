# taktivitypub

*Note: This is still under early development and is not fully usable yet!*

This is an ActivityPub (and ActivityStreams) object parsing and
generation library, designed to make it easier to both accept the wide
variety of ActivityPub object messages and to make it easier to create messages
accepted by other servers.

To parse objects, hand the Python dict you got from the JSON to `APObject.load`:

```
from taktivitypub import APObject

my_note_data = {"type": "Note", "id": "https://...", ...}
note = APObject.load(my_note_data)
# Now we can use the object fields as normal Python objects
print(note.published.strptime("%Y-%m-%d"))
```

It will return the appopriate `APObject` subclass for the type of object you passed - so if you have an object of type `Note`, you will get a `taktivitypub.Note` class back.

To create messages, construct the objects and then call `dump`:

```
note = Note(
    id="https://example.com/1",
    content="Hi",
    attributed_to="https://example.com/andrew",
)
json = note.dump()
```
