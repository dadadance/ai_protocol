# Testing Guidelines

> **Template for Testing Strategy**
>
> This document defines the testing strategy, tools, and best practices for the project.
> AI Agents and Developers MUST adhere to these guidelines to ensure code quality and reliability.

---

## 1. Testing Framework & Tools

| Tool | Purpose | Recommended Command |
|------|---------|---------------------|
| **pytest** | Test Runner & Framework | `uv run pytest` |
| **pytest-cov** | Coverage Reporting | `uv run pytest --cov=src` |
| **unittest.mock** | Mocking & Spying | Standard Library |
| **Ruff** | Linting & Formatting | `uv run ruff check .` / `uv run ruff format .` |

---

## 2. Directory Structure

Tests should mirror the source code structure within a top-level `tests/` directory.

```text
project/
├── src/
│   ├── auth/
│   │   ├── login.py
│   │   └── utils.py
│   └── main.py
└── tests/
    ├── conftest.py          # Shared fixtures
    ├── auth/
    │   ├── test_login.py    # Tests for login.py
    │   └── test_utils.py    # Tests for utils.py
    └── test_main.py
```

---

## 3. Test Types & Scope

### 3.1. Unit Tests (Fast & Isolated)
*   **Scope:** Individual functions, classes, or methods.
*   **Dependencies:** All external dependencies (DB, API, File System) **MUST** be mocked.
*   **Location:** `tests/unit/` (optional split) or co-located in `tests/`.
*   **Goal:** Verify logic correctness, edge cases, and error handling.

### 3.2. Integration Tests (Slower & Connected)
*   **Scope:** Interaction between modules or interaction with external systems (DB, API).
*   **Dependencies:** Use real (containerized) databases or file systems where possible; mock expensive 3rd party APIs.
*   **Marker:** Use `@pytest.mark.integration` to allow separate execution.
*   **Goal:** Verify data flow and component wiring.

---

## 4. Best Practices

### 4.1. Arrange-Act-Assert (AAA)
Every test function must follow this structure clearly.

```python
def test_calculate_total_with_discount():
    # Arrange
    price = 100.0
    discount = 0.2
    expected = 80.0

    # Act
    result = calculate_total(price, discount)

    # Assert
    assert result == expected
```

### 4.2. Fixtures over `setUp/tearDown`
Use `pytest` fixtures for setup and teardown logic. They are modular, reusable, and explicit.

```python
@pytest.fixture
def mock_db():
    db = create_test_db()
    yield db
    db.teardown()

def test_user_creation(mock_db):
    ...
```

### 4.3. One Assertion per Concept
Try to verify one logical outcome per test. Multiple assertions are okay if they check different aspects of the *same* state change.

### 4.4. Mocking Guidelines
*   **Mock at boundaries:** Only mock external calls or slow dependencies.
*   **Do not mock internal logic:** If you have to mock half the function to test it, the function is likely too complex (refactor it).

---

## 5. Coverage Requirements

*   **Pure Functions:** 100% Coverage.
*   **Business Logic:** >90% Coverage.
*   **Overall Project Goal:** >80% Coverage.

Run coverage check:
```bash
uv run pytest --cov=src --cov-report=term-missing
```

---

## 6. Continuous Integration (CI)

Tests are automatically run on every Pull Request.
*   **Blocker:** If tests fail, the PR cannot be merged.
*   **Linting:** Ruff (lint + format) is run alongside tests. Command: `uv run ruff check . && uv run ruff format --check .`
