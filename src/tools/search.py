from datetime import date

from logger import log_call
from models import Incident
from servicenow import INCIDENT_FIELDS, client, map_incident
from settings import settings


def _build_query(
    hostname: str | None,
    start_date: date | None,
    end_date: date | None,
) -> str:
    clauses = []
    if hostname:
        clauses.append(f"cmdb_ci.nameCONTAINS{hostname}")
    if start_date:
        clauses.append(f"sys_created_on>={start_date} 00:00:00")
    if end_date:
        clauses.append(f"sys_created_on<={end_date} 23:59:59")
    return "^".join(clauses)


@log_call
def search(
    hostname: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[Incident]:
    """Search incidents. At least one of hostname, start_date, or end_date must be provided."""
    if not any([hostname, start_date, end_date]):
        raise ValueError("At least one search parameter must be specified.")

    with client() as c:
        response = c.get(
            f"{settings.api_url}/api/now/table/incident",
            params={
                "sysparm_query": _build_query(hostname, start_date, end_date),
                "sysparm_fields": INCIDENT_FIELDS,
                "sysparm_orderby": "sys_created_on",
            },
        )
        response.raise_for_status()

    return [map_incident(record) for record in response.json().get("result", [])]
