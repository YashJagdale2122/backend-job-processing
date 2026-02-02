from enum import Enum

class JobStatus(str, Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"

class JobType(str, Enum):
    GENERIC = "GENERIC"
    EMAIL = "EMAIL"
    VIDEO = "VIDEO"
