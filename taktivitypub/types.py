import datetime
from typing import Annotated, Literal, TypeVar

from pydantic.functional_serializers import PlainSerializer
from pydantic.functional_validators import AfterValidator, BeforeValidator

T = TypeVar("T")


def validate_iri(value: str):
    assert "://" in value, f"{value} is not a valid IRI"
    return value


def validate_list_or_single(value):
    if not isinstance(value, list):
        return [value]
    return value


def serialize_datetime(value: datetime.datetime) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


IRI = Annotated[str, AfterValidator(validate_iri)]
IRIOrPublic = IRI | Literal["as:Public"]
ListOrSingle = Annotated[list[T], BeforeValidator(validate_list_or_single)]
ISODatetime = Annotated[datetime.datetime, PlainSerializer(serialize_datetime)]
