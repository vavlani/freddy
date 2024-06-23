# Coding Conventions

## General Guidelines
- Follow PEP 8 for code style.
- Use type hints everywhere possible.
- Add docstrings to all functions, classes, and modules.
- Use f-strings for string formatting.
- Avoid magic numbers; define constants instead.
- Write modular and reusable code.

## Project Structure
- Organize the project with a clear, standard structure:

## Documentation
- Use Markdown for documentation.
- Include a `CHANGELOG.md` for tracking changes.
- Use docstrings for documenting modules, classes, methods, and functions.

## Testing
- Use `pytest` for writing and running tests.
- Write unit tests.
- Name test functions and methods clearly to describe what they are testing.

## Dependencies
- Use  `poetry` for managing dependencies.
- Keep `pyproject.toml` updated.
- Pin dependencies to specific versions.
- Regularly update dependencies to their latest versions.

## Logging and Monitoring
- Use the `logging` module for logging.
- Configure logging levels appropriately.
- Avoid logging sensitive information.

## Exception Handling
- Handle exceptions gracefully.
- Use custom exceptions where appropriate.
- Avoid bare `except` clauses; catch specific exceptions.

## Configuration Management
- Use configuration files for managing settings (e.g.`config.yaml`).
- Separate configuration from code.

## Performance
- Avoid premature optimization; focus on readability and maintainability first.


