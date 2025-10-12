# AI Agent Instructions for Code Review Assistant

## Project Overview
This is a GitHub App that automates code reviews. It's implemented as an AWS Lambda function that responds to GitHub webhook events, specifically for pull request reviews and discussion comments.

## Key Architecture Components

### Event Flow
1. GitHub webhook → `lambda_function.py` (entrypoint)
2. Event classification → SQS queue for processing
3. GitHub API interaction through `repo_handler.py`

### Core Components
- `lambda_function.py`: Main webhook handler and event router
- `repo_handler.py`: GitHub API interaction layer
- `token_manager.py`: GitHub App authentication using JWT and installation tokens
- `clients.py`: AWS service client factories (SQS, SSM)
- `dto.py`: Event type definitions and user action enums

## Development Patterns

### Authentication Flow
```python
# Example from repo_handler.py
jwt_token = TokenManager.get_jwt_token()
access_token = TokenManager.get_installation_access_token(jwt_token, installation_id)
```

### AWS Integration
- Uses boto3 with cached clients (see `@lru_cache` in `clients.py`)
- SSM for secrets in prod, local files for development
- SQS for async processing queue

### Testing
- Pytest for unit testing
- Mock fixtures in `conftest.py`
- HTTP client mocking pattern for GitHub API calls

## Environment Setup
1. Python dependencies: `pip install -r requirements.txt`
2. Local environment needs:
   - GitHub App private key at specified path
   - AWS credentials for SQS/SSM access
   - Environment variables defined in config.py

## Common Operations

### Adding New Event Types
1. Add enum to `dto.py`
2. Update `classify_user_action()` in `lambda_function.py`
3. Create handler function following existing patterns

### Integration Testing
- Set ENV=local for local file-based secrets
- Use httpx AsyncClient for GitHub API calls
- Mock AWS services using pytest fixtures

## Key Files to Review
- `src/lambda_function.py`: Entry point and event routing
- `src/repo_handler.py`: GitHub interaction patterns
- `src/token_manager.py`: Authentication flow
- `tests/test_token_manager.py`: Testing patterns