from __future__ import annotations

from enum import Enum
from typing import Optional
from pydantic import BaseModel


class IncidentSeverity(str, Enum):
    SEV1 = "sev1"
    SEV2 = "sev2"
    SEV3 = "sev3"
    SEV4 = "sev4"


class IncidentStatus(str, Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    MITIGATED = "mitigated"
    RESOLVED = "resolved"


class TimelineEntry(BaseModel):
    id: str
    incident_id: str
    timestamp: str
    author: str
    message: str


class Incident(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    severity: IncidentSeverity
    status: IncidentStatus
    created_at: str
    updated_at: str
    assignee: Optional[str] = None
    timeline: list[TimelineEntry] = []
