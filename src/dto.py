from enum import Enum


class UserAction(str, Enum):
    REVIEW_REQUESTED = "review_requested"
    UNKNOWN = "unknown"    
