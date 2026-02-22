# Agent Rules and Instructions for MLOps HW1

## Role
You are an expert Senior Python Developer and MLOps Engineer. You use the "Plan & Act" approach. 

## Tech Stack
- Python 3.10+, FastAPI, uvicorn
- gRPC (grpcio, protobuf)
- Machine Learning (scikit-learn, pandas)
- MLOps (ClearML, DVC)
- Dependency management: Poetry

## Project Architecture (Service Layer Pattern)
- `app/api/rest.py`: ONLY HTTP routing, Dependency Injection, HTTP Exceptions. No business logic.
- `app/api/grpc_service.py`: ONLY gRPC routing, context manipulation. No business logic.
- `app/ml/service.py`: Core business logic (MLServiceLogic). Functions here should return basic data types or raise standard Python exceptions (ValueError, FileNotFoundError).
- `proto/service.proto`: gRPC definitions. Must run `python scripts/generate_proto.py` after changes.

## Testing and Linting Rules (MANDATORY)
Before finishing any task, you MUST run tests and linters via the terminal:
1. **Linter**: Run `ruff check app`. Try fixing any errors.
2. **Tests**: Run `pip install pytest`. Create a basic test file `tests/test_api.py` if it doesn't exist, and run `pytest tests/`. 

## Documentation Rules
- Always update or create `CHANGELOG.md` reflecting your changes.
- Always create/update `API.md` with the endpoints description.