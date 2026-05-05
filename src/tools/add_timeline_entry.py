from logger import log_call
from models import TimelineEntry


@log_call
def add_timeline_entry(incident_id: str, message: str, author: str) -> TimelineEntry:
    """Add a timeline entry to an incident."""
    raise NotImplementedError
