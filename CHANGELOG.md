# Changelog

## [Unreleased]

### Added
- New REST endpoint `/predict/batch` for batch predictions from CSV files
- New gRPC method `PredictBatch` for batch predictions
- New service method `MLServiceLogic.predict_batch()` to handle batch predictions
- CSV file parsing functionality in the service layer
- Basic test coverage for batch prediction endpoint
- API documentation for batch prediction feature

### Changed
- Updated `proto/service.proto` to include `BatchPredictRequest` and `BatchPredictResponse` message types
- Regenerated gRPC stubs to include new batch prediction methods

### Fixed
- None

### Technical Details
- Batch prediction accepts CSV files via multipart form upload
- Each row in the CSV is treated as a separate sample
- The service returns an array of predictions (one per row)
- Proper error handling for malformed CSV files and missing models

### Testing
- Added tests for health check endpoint
- Added tests for batch prediction endpoint validation
- All existing tests continue to pass
- Linter (ruff) checks pass for all modified files

### Breaking Changes
- None

## Previous Versions

### [0.1.0]
- Initial implementation of MLOps service
- REST and gRPC endpoints for model training, prediction, and management
- DVC integration for dataset management
- ClearML integration for model tracking and storage
