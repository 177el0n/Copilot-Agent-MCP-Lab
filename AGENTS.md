# Project Guidance

## Project

This project is a small FastAPI Todo API used to learn AI-assisted development.

## Architecture

Use the following dependency direction:

Router
→ Service
→ Repository

- Routers handle HTTP concerns.
- Services contain business logic.
- Repositories handle data access.
- Routers must not access repositories directly.

## Development Policy

- Keep changes small and focused.
- Preserve existing API behavior unless explicitly requested.
- Add tests for new behavior.
- Do not delete tests to make implementation pass.

## Security

- Do not hard-code credentials.
- Do not commit `.env` files.
- Do not log secrets or tokens.
