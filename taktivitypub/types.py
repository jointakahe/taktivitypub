from typing import Annotated
from pydantic.functional_validators import AfterValidator

IRI = Annotated[str, AfterValidator(validate_iri)]
