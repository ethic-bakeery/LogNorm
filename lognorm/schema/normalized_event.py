from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class LogType(str, Enum):
    AUTH = "auth"
    SYSLOG = "syslog"
    SSH = "ssh"
    UNKNOWN = "unknown"

class AuthResult(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    UNKNOWN = "unknown"

class NormalizedEvent(BaseModel):
    # Core
    event_id: str
    timestamp: Optional[datetime] = None
    host: Optional[str] = None
    log_type: LogType = LogType.UNKNOWN
    severity: Severity = Severity.INFO
    message: Optional[str] = None
    raw: str

    # Actor
    user: Optional[str] = None
    ip_address: Optional[str] = None
    port: Optional[int] = None

    # Process
    process_name: Optional[str] = None
    process_id: Optional[int] = None

    # Auth
    auth_result: Optional[AuthResult] = None
    auth_method: Optional[str] = None

    # Detection
    is_suspicious: bool = False
    detection_reason: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    # Meta
    schema_version: str = "1.0.0"
    source_file: Optional[str] = None
