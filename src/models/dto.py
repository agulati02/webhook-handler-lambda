from enum import Enum


class Event(str, Enum):
    PULL_REQUEST = "pull_request"
    ISSUE_COMMENT = "issue_comment"
    UNKNOWN = "unknown"

class UserAction(str, Enum):
    REVIEW_REQUESTED = "review_requested"
    DISCUSSION_COMMENT = "discussion_comment"
    UNKNOWN = "unknown"    
