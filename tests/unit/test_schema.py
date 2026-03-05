from lognorm.schema.normalized_event import NormalizedEvent, Severity, LogType
import uuid

def test_minimal_event_creation():
    event = NormalizedEvent(
        event_id=str(uuid.uuid4()),
        raw="Feb 28 10:00:00 server sshd[1234]: Failed password for root"
    )
    assert event.severity == Severity.INFO
    assert event.is_suspicious == False
    assert event.schema_version == "1.0.0"

def test_full_event_creation():
    event = NormalizedEvent(
        event_id=str(uuid.uuid4()),
        raw="Feb 28 10:00:00 server sshd[1234]: Failed password for root from 192.168.1.1",
        user="root",
        ip_address="192.168.1.1",
        severity=Severity.HIGH,
        log_type=LogType.SSH,
        is_suspicious=True,
        detection_reason="Failed login attempt for root account"
    )
    assert event.user == "root"
    assert event.is_suspicious == True

def test_tags_default_empty():
    event = NormalizedEvent(
        event_id=str(uuid.uuid4()),
        raw="some log line"
    )
    assert event.tags == []
