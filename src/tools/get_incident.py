import logging

from models import Incident
from servicenow import INCIDENT_FIELDS, JOURNAL_FIELDS, client, map_incident
from settings import settings

logger = logging.getLogger(__name__)


def _fetch_incident_record(incident_number: str) -> dict:
    with client() as c:
        response = c.get(
            f"{settings.api_url}/api/now/table/incident",
            params={
                "sysparm_query": f"number={incident_number}",
                "sysparm_fields": INCIDENT_FIELDS,
                "sysparm_limit": 1,
            },
        )
        response.raise_for_status()

    records = response.json().get("result", [])
    if not records:
        raise ValueError(f"Incident {incident_number!r} not found")
    return records[0]


def _fetch_journal_entries(sys_id: str) -> list[dict]:
    with client() as c:
        response = c.get(
            f"{settings.api_url}/api/now/table/sys_journal_field",
            params={
                "sysparm_query": f"element_id={sys_id}^elementINcomments,work_notes",
                "sysparm_fields": JOURNAL_FIELDS,
                "sysparm_orderby": "sys_created_on",
            },
        )
        response.raise_for_status()

    return response.json().get("result", [])


def get_incident(incident_id: str) -> Incident:
    """Get details for a specific incident by ID, including its full timeline."""
    logger.info("get_incident(incident_id=%r)", incident_id)
    record = _fetch_incident_record(incident_id)
    journal = _fetch_journal_entries(record["sys_id"])
    result = map_incident(record, journal)
    logger.info("get_incident returned %r", result)
    return result
