import pytest
from unittest.mock import Mock, patch
from src.lambda_function import classify_user_action, handle_review_request, handle_discussion_comment


def test_classify_user_action_review_requested():
    payload = {
        "action": "review_requested",
        "pull_request": {
            "requested_reviewers": [{"login": "tgrafy"}, {"login": "other_user"}]
        },
        "installation": {"id": 12345}
    }
    headers = {"x-github-event": "pull_request"}
    
    action = classify_user_action(payload, headers)
    assert action == "review_requested"

def test_classify_user_action_discussion_comment():
    payload = {
        "action": "created",
        "comment": {"body": "Hello @tgrafy, please review this."},
        "installation": {"id": 12345}
    }
    headers = {"x-github-event": "issue_comment"}
    
    action = classify_user_action(payload, headers)
    assert action == "discussion_comment"

def test_classify_user_action_unknown_event():
    payload = {"action": "some_action"}
    headers = {"x-github-event": "unknown_event"}
    
    action = classify_user_action(payload, headers)
    assert action == "unknown"
