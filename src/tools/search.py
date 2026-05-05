from datetime import date

from logger import log_call
from models import Incident


@log_call
def search(
    hostname: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[Incident]:
    """Search incidents. At least one of hostname, start_date, or end_date must be provided."""
    if not any([hostname, start_date, end_date]):
        raise ValueError("At least one search parameter must be specified.")
    raise NotImplementedError
