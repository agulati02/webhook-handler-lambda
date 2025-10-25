from enum import Enum


class Event(str, Enum):
    PULL_REQUEST = "pull_request"
    ISSUE_COMMENT = "issue_comment"
    UNKNOWN = "unknown"

class EventStatus(str, Enum):
    IN_QUEUE = "in_queue"
    IN_REVIEW = "in_review"
    COMPLETED = "completed"
    EXCEPTION = "exception" 
