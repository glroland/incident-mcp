from logger import log_call
from models import Incident


@log_call
def get_incident(incident_id: str) -> Incident:
    """Get details for a specific incident by ID, including its full timeline."""
    raise NotImplementedError
