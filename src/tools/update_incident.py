from logger import log_call
from models import Incident, IncidentSeverity, IncidentStatus


@log_call
def update_incident(
    incident_id: str,
    status: IncidentStatus | None = None,
    severity: IncidentSeverity | None = None,
    assignee: str | None = None,
) -> Incident:
    """Update the status, severity, or assignee of an incident."""
    raise NotImplementedError
