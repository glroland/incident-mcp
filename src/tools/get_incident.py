import httpx

from logger import log_call
from models import Incident, IncidentSeverity, IncidentStatus, TimelineEntry
from settings import settings

# ServiceNow severity values: 1=Critical, 2=High, 3=Moderate, 4=Low
_SEVERITY_MAP: dict[str, IncidentSeverity] = {
    "1": IncidentSeverity.SEV1,
    "2": IncidentSeverity.SEV2,
    "3": IncidentSeverity.SEV3,
    "4": IncidentSeverity.SEV4,
}

# ServiceNow state values: 1=New, 2=In Progress, 3=On Hold, 6=Resolved, 7=Closed, 8=Cancelled
_STATUS_MAP: dict[str, IncidentStatus] = {
    "1": IncidentStatus.OPEN,
    "2": IncidentStatus.INVESTIGATING,
    "3": IncidentStatus.INVESTIGATING,
    "6": IncidentStatus.MITIGATED,
    "7": IncidentStatus.RESOLVED,
    "8": IncidentStatus.RESOLVED,
}

_INCIDENT_FIELDS = ",".join([
    "sys_id",
    "number",
    "short_description",
    "description",
    "severity",
    "state",
    "sys_created_on",
    "sys_updated_on",
    "assigned_to",
])

_JOURNAL_FIELDS = ",".join([
    "sys_id",
    "sys_created_on",
    "sys_created_by",
    "value",
])


def _client() -> httpx.Client:
    return httpx.Client(
        auth=(settings.api_username, settings.api_password),
        headers={"Accept": "application/json"},
        timeout=settings.api_timeout,
    )


def _fetch_incident_record(incident_number: str) -> dict:
    with _client() as client:
        response = client.get(
            f"{settings.api_url}/api/now/table/incident",
            params={
                "sysparm_query": f"number={incident_number}",
                "sysparm_fields": _INCIDENT_FIELDS,
                "sysparm_limit": 1,
            },
        )
        response.raise_for_status()

    records = response.json().get("result", [])
    if not records:
        raise ValueError(f"Incident {incident_number!r} not found")
    return records[0]


def _fetch_journal_entries(sys_id: str) -> list[dict]:
    with _client() as client:
        response = client.get(
            f"{settings.api_url}/api/now/table/sys_journal_field",
            params={
                "sysparm_query": f"element_id={sys_id}^elementINcomments,work_notes",
                "sysparm_fields": _JOURNAL_FIELDS,
                "sysparm_orderby": "sys_created_on",
            },
        )
        response.raise_for_status()

    return response.json().get("result", [])


def _map_assignee(raw: object) -> str | None:
    if isinstance(raw, dict):
        return raw.get("display_value") or None
    return raw or None


def _map_incident(record: dict, journal: list[dict]) -> Incident:
    number = record.get("number", record["sys_id"])
    return Incident(
        id=number,
        title=record.get("short_description", ""),
        description=record.get("description") or None,
        severity=_SEVERITY_MAP.get(record.get("severity", ""), IncidentSeverity.SEV4),
        status=_STATUS_MAP.get(record.get("state", ""), IncidentStatus.OPEN),
        created_at=record.get("sys_created_on", ""),
        updated_at=record.get("sys_updated_on", ""),
        assignee=_map_assignee(record.get("assigned_to")),
        timeline=[
            TimelineEntry(
                id=entry["sys_id"],
                incident_id=number,
                timestamp=entry.get("sys_created_on", ""),
                author=entry.get("sys_created_by", ""),
                message=entry.get("value", ""),
            )
            for entry in journal
        ],
    )


@log_call
def get_incident(incident_id: str) -> Incident:
    """Get details for a specific incident by ID, including its full timeline."""
    record = _fetch_incident_record(incident_id)
    journal = _fetch_journal_entries(record["sys_id"])
    return _map_incident(record, journal)
