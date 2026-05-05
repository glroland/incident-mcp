from unittest.mock import MagicMock, patch

import pytest

from src.models import IncidentSeverity, IncidentStatus
from src.tools.get_incident import get_incident

INCIDENT_RECORD = {
    "sys_id": "a1b2c3d4e5f67890",
    "number": "INC0011318",
    "short_description": "Production web server unreachable",
    "description": "Users are unable to connect to the main production web server.",
    "severity": "1",
    "state": "2",
    "sys_created_on": "2025-01-15 08:00:00",
    "sys_updated_on": "2025-01-15 09:30:00",
    "assigned_to": {"display_value": "Jane Smith", "value": "usr_jane"},
}

JOURNAL_ENTRY_1 = {
    "sys_id": "j001",
    "sys_created_on": "2025-01-15 08:15:00",
    "sys_created_by": "jsmith",
    "value": "Started investigating connectivity issues",
}

JOURNAL_ENTRY_2 = {
    "sys_id": "j002",
    "sys_created_on": "2025-01-15 09:00:00",
    "sys_created_by": "jsmith",
    "value": "Identified network misconfiguration as root cause",
}


def _mock_client(data: dict) -> MagicMock:
    """Return a mock httpx context manager whose .get() yields the given JSON."""
    response = MagicMock()
    response.raise_for_status.return_value = None
    response.json.return_value = data

    c = MagicMock()
    c.__enter__ = MagicMock(return_value=c)
    c.__exit__ = MagicMock(return_value=False)
    c.get.return_value = response
    return c


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

def test_get_incident_returns_correct_incident():
    with patch("src.tools.get_incident.client") as mock_factory:
        mock_factory.side_effect = [
            _mock_client({"result": [INCIDENT_RECORD]}),
            _mock_client({"result": []}),
        ]
        result = get_incident("INC0011318")

    assert result.id == "INC0011318"
    assert result.title == "Production web server unreachable"
    assert result.description == "Users are unable to connect to the main production web server."
    assert result.severity == IncidentSeverity.SEV1
    assert result.status == IncidentStatus.INVESTIGATING
    assert result.assignee == "Jane Smith"
    assert result.created_at == "2025-01-15 08:00:00"
    assert result.updated_at == "2025-01-15 09:30:00"


def test_get_incident_includes_timeline():
    with patch("src.tools.get_incident.client") as mock_factory:
        mock_factory.side_effect = [
            _mock_client({"result": [INCIDENT_RECORD]}),
            _mock_client({"result": [JOURNAL_ENTRY_1]}),
        ]
        result = get_incident("INC0011318")

    assert len(result.timeline) == 1
    entry = result.timeline[0]
    assert entry.id == "j001"
    assert entry.incident_id == "INC0011318"
    assert entry.author == "jsmith"
    assert entry.message == "Started investigating connectivity issues"
    assert entry.timestamp == "2025-01-15 08:15:00"


def test_get_incident_timeline_is_empty_for_new_incident():
    with patch("src.tools.get_incident.client") as mock_factory:
        mock_factory.side_effect = [
            _mock_client({"result": [INCIDENT_RECORD]}),
            _mock_client({"result": []}),
        ]
        result = get_incident("INC0011318")

    assert result.timeline == []


def test_get_incident_timeline_entries_ordered_chronologically():
    with patch("src.tools.get_incident.client") as mock_factory:
        mock_factory.side_effect = [
            _mock_client({"result": [INCIDENT_RECORD]}),
            _mock_client({"result": [JOURNAL_ENTRY_1, JOURNAL_ENTRY_2]}),
        ]
        result = get_incident("INC0011318")

    assert len(result.timeline) == 2
    assert result.timeline[0].timestamp == "2025-01-15 08:15:00"
    assert result.timeline[1].timestamp == "2025-01-15 09:00:00"
    assert result.timeline[0].timestamp < result.timeline[1].timestamp


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

def test_get_incident_raises_when_not_found():
    with patch("src.tools.get_incident.client") as mock_factory:
        mock_factory.return_value = _mock_client({"result": []})

        with pytest.raises(ValueError, match="HIIDONTEXIST"):
            get_incident("HIIDONTEXIST")


def test_get_incident_raises_when_id_is_null():
    with patch("src.tools.get_incident.client") as mock_factory:
        mock_factory.return_value = _mock_client({"result": []})

        with pytest.raises(ValueError, match="not found"):
            get_incident(None)
