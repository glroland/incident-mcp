from logger import log_call
from models import TimelineEntry
from servicenow import JOURNAL_FIELDS, client
from settings import settings


def _lookup_sys_id(incident_number: str) -> str:
    with client() as c:
        response = c.get(
            f"{settings.api_url}/api/now/table/incident",
            params={
                "sysparm_query": f"number={incident_number}",
                "sysparm_fields": "sys_id",
                "sysparm_limit": 1,
            },
        )
        response.raise_for_status()

    records = response.json().get("result", [])
    if not records:
        raise ValueError(f"Incident {incident_number!r} not found")
    return records[0]["sys_id"]


def _add_work_note(sys_id: str, message: str) -> None:
    with client() as c:
        response = c.patch(
            f"{settings.api_url}/api/now/table/incident/{sys_id}",
            json={"work_notes": message},
        )
        response.raise_for_status()


def _fetch_latest_journal_entry(sys_id: str) -> dict:
    with client() as c:
        response = c.get(
            f"{settings.api_url}/api/now/table/sys_journal_field",
            params={
                "sysparm_query": f"element_id={sys_id}^elementINcomments,work_notes",
                "sysparm_fields": JOURNAL_FIELDS,
                "sysparm_orderbyDesc": "sys_created_on",
                "sysparm_limit": 1,
            },
        )
        response.raise_for_status()

    entries = response.json().get("result", [])
    if not entries:
        raise RuntimeError(f"Could not retrieve created journal entry for sys_id {sys_id!r}")
    return entries[0]


@log_call
def add_timeline_entry(incident_id: str, message: str, author: str) -> TimelineEntry:
    """Add a timeline entry to an incident."""
    sys_id = _lookup_sys_id(incident_id)
    _add_work_note(sys_id, message)
    entry = _fetch_latest_journal_entry(sys_id)
    return TimelineEntry(
        id=entry["sys_id"],
        incident_id=incident_id,
        timestamp=entry.get("sys_created_on", ""),
        author=author,
        message=message,
    )
