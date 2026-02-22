# Feature Plan: Batch Prediction Implementation

## Overview
Add a new batch prediction feature that allows users to upload CSV files containing multiple feature vectors and receive predictions for all of them. This includes both REST and gRPC endpoints.

## Implementation Steps

### 1. Update Protocol Buffers Definition
- **File**: 
- **Changes**:
  - Add new message type  with fields:
    -  - ID of the model to use for prediction
    -  - CSV file content with features
  - Add new message type  with fields:
    -  - Array of predictions (one per row)
  - Add new RPC method 
- **Validation**: Ensure the proto definition follows existing patterns

### 2. Implement Batch Prediction Logic in Service Layer
- **File**: 
- **Changes**:
  - Add new method 
  - Method should:
    - Load the model from ClearML using 
    - Parse CSV content into pandas DataFrame
    - Extract features (all columns except possibly the last)
    - Use loaded model to predict on all rows
    - Return predictions as list of floats
  - Handle edge cases:
    - Empty CSV files
    - Malformed CSV data
    - Missing model
    - Different feature dimensions than model expects

### 3. Add REST Endpoint
- **File**: 
- **Changes**:
  - Add new Pydantic model  with:
    - 
    -  (CSV file)
  - Add new endpoint  that:
    - Accepts multipart form data with CSV file
    - Reads file content
    - Calls 
    - Returns predictions as JSON array
  - Add proper error handling for:
    - File upload issues
    - Model not found
    - Prediction errors

### 4. Add gRPC Method Implementation
- **File**: 
- **Changes**:
  - Implement  method in  class
  - Method should:
    - Extract model_id and csv_content from request
    - Call 
    - Return predictions in 
  - Add error handling with appropriate gRPC status codes

### 5. Generate gRPC Code
- **Command**: Proto files generated.
- **Purpose**: Regenerate Python gRPC stubs from updated proto file

### 6. Create Tests
- **File**:  (create if doesn't exist)
- **Tests to implement**:
  - Test batch prediction with valid CSV data
  - Test batch prediction with invalid model_id
  - Test batch prediction with malformed CSV
  - Test batch prediction endpoint availability
  - Test gRPC batch prediction method
  - Test error responses for various edge cases

### 7. Update Documentation
- **File**:  (create if doesn't exist)
- **Changes**:
  - Add section for  REST endpoint
  - Document:
    - Request format (multipart form with CSV file)
    - Response format (array of predictions)
    - Example request/response
    - Error cases

- **File**:  (create if doesn't exist)
- **Changes**:
  - Add entry for batch prediction feature
  - List all changes made

### 8. Run Linters and Tests
- **Commands**:
  - All checks passed! - Run linter and fix any issues
  - ============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-8.3.5, pluggy-1.5.0
rootdir: D:\HSE\mlops\hw1
configfile: pyproject.toml
plugins: anyio-4.9.0, docker-3.1.2
collected 0 items

============================ no tests ran in 0.03s ============================ - Run tests (ensure pytest is installed)
  - Fix any linting or test failures

## Dependencies
- No new dependencies required (pandas and joblib already in use)

## Validation Plan
1. Code quality: Run ruff linter
2. Unit tests: Test all new functionality
3. Integration: Verify REST and gRPC endpoints work
4. Error handling: Test edge cases and error scenarios

## Risk Assessment
- **Medium risk**: CSV parsing may fail with malformed data
- **Medium risk**: Feature dimension mismatch between model and input
- **Low risk**: ClearML model loading (already tested in single prediction)

## Follow-up Tasks
- Consider adding input validation for CSV schema
- Add support for different file formats (JSON, parquet)
- Implement batch prediction rate limiting if needed
