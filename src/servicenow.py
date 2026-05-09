import httpx

from models import Incident, IncidentSeverity, IncidentStatus, TimelineEntry
from settings import settings

# ServiceNow severity values: 1=Critical, 2=High, 3=Moderate, 4=Low
SEVERITY_MAP: dict[str, IncidentSeverity] = {
    "1": IncidentSeverity.SEV1,
    "2": IncidentSeverity.SEV2,
    "3": IncidentSeverity.SEV3,
    "4": IncidentSeverity.SEV4,
}

# ServiceNow state values: 1=New, 2=In Progress, 3=On Hold, 6=Resolved, 7=Closed, 8=Cancelled
STATUS_MAP: dict[str, IncidentStatus] = {
    "1": IncidentStatus.OPEN,
    "2": IncidentStatus.INVESTIGATING,
    "3": IncidentStatus.INVESTIGATING,
    "6": IncidentStatus.MITIGATED,
    "7": IncidentStatus.RESOLVED,
    "8": IncidentStatus.RESOLVED,
}

INCIDENT_FIELDS = ",".join([
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

JOURNAL_FIELDS = ",".join([
    "sys_id",
    "sys_created_on",
    "sys_created_by",
    "value",
])


def client() -> httpx.Client:
    return httpx.Client(
        auth=(settings.snow_username, settings.snow_password),
        headers={"Accept": "application/json"},
        timeout=settings.api_timeout,
    )


def map_assignee(raw: object) -> str | None:
    if isinstance(raw, dict):
        return raw.get("display_value") or None
    return raw or None


def map_incident(record: dict, journal: list[dict] | None = None) -> Incident:
    number = record.get("number", record["sys_id"])
    return Incident(
        id=number,
        title=record.get("short_description", ""),
        description=record.get("description") or None,
        severity=SEVERITY_MAP.get(record.get("severity", ""), IncidentSeverity.SEV4),
        status=STATUS_MAP.get(record.get("state", ""), IncidentStatus.OPEN),
        created_at=record.get("sys_created_on", ""),
        updated_at=record.get("sys_updated_on", ""),
        assignee=map_assignee(record.get("assigned_to")),
        timeline=[
            TimelineEntry(
                id=entry["sys_id"],
                incident_id=number,
                timestamp=entry.get("sys_created_on", ""),
                author=entry.get("sys_created_by", ""),
                message=entry.get("value", ""),
            )
            for entry in (journal or [])
        ],
    )
