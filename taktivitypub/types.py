import datetime
from typing import Annotated, ForwardRef, Literal, TypeVar

from pydantic.functional_serializers import PlainSerializer
from pydantic.functional_validators import AfterValidator, BeforeValidator

T = TypeVar("T")


def validate_iri(value: str) -> str:
    """
    Checks (badly) if a string is a valid IRI
    """
    assert "://" in value, f"{value} is not a valid IRI"
    return value


def validate_list_or_single(value: T | list[T]) -> list[T]:
    """
    Coerces single values into a list
    """
    if not isinstance(value, list):
        return [value]
    return value


def serialize_list_or_single(value):
    """
    Removes empty lists from the output, as they're implicit in JSON-LD
    """
    if not value:
        return None
    return value


def validate_iri_or_object(value):
    """
    If there is an embedded object, loads it so it gains the right class.
    """
    from taktivitypub.base import APObject

    if isinstance(value, dict):
        return APObject.load(value)
    return value


def serialize_iri_or_object(value):
    """
    Dumps embedded objects with validation
    """
    if not (isinstance(value, str) or value is None):
        return value.dump()
    return value


def serialize_iso_datetime(value: datetime.datetime) -> str:
    """
    Ensures datetimes come out as a standard format
    """
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def get_map_value(map: dict[str, T]) -> T | None:
    """
    Retrieves a value from the given nameMap or contentMap
    """
    if len(map) == 1:
        return list(map.values())[0]
    if "und" in map:
        return map["und"]
    if "en" in map:
        return map["en"]
    return None


APObject = ForwardRef("APObject")
IRI = Annotated[str, AfterValidator(validate_iri)]
IRIOrPublic = IRI | Literal["as:Public"]
ListOrSingle = Annotated[
    list[T],
    BeforeValidator(validate_list_or_single),
    PlainSerializer(serialize_list_or_single),
]
ISODatetime = Annotated[datetime.datetime, PlainSerializer(serialize_iso_datetime)]
