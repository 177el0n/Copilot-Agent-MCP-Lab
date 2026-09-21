# Copilot Agent MCP Lab

A small learning project for understanding:

- AGENTS.md
- Custom agents
- Prompt files
- Instruction files
- Model Context Protocol (MCP)

The sample application is a simple FastAPI Todo API.

## Development Workflow

This project uses a small AI-assisted development workflow to learn how GitHub Copilot custom agents, prompts, instructions, Git, and GitHub CLI work together.

The basic flow is:

```text
User Requirement
      ↓
Issue Setup Agent
      ↓
GitHub Issue
      ↓
Feature Branch
      ↓
Developer Agent
      ↓
Tester Agent
      ↓
Reviewer Agent
      ↓
Commit / Push
      ↓
PR Manager Agent
      ↓
Pull Request
      ↓
main
```

### 1. Prepare the Development Task

Use the `issue-setup` agent to prepare a new development task.

The agent is responsible for:

1. Understanding the requested change.
2. Creating a GitHub Issue using GitHub CLI.
3. Writing clear requirements and acceptance criteria.
4. Obtaining the Issue number.
5. Creating a feature branch associated with the Issue.
6. Switching to the created feature branch.

GitHub operations are performed with:

```bash
gh issue create
```

Feature branches follow this naming convention:

```text
feature/<issue-number>-<short-description>
```

Example:

```text
feature/1-todo-priority
```

The GitHub Issue acts as the development contract for the task.

It should describe:

* Summary
* Requirements
* Acceptance Criteria

The acceptance criteria are used by the Developer, Tester, and Reviewer agents as the common definition of completion.

### 2. Implement the Issue

Use the `developer` agent to implement the Issue.

The Developer:

* Reads the Issue requirements.
* Inspects the existing implementation.
* Follows `AGENTS.md`.
* Follows applicable `*.instructions.md` files.
* Implements the smallest reasonable change.
* Adds or updates tests when necessary.
* Runs relevant tests.

The project architecture follows:

```text
Router
  ↓
Service
  ↓
Repository
```

Routers must not access repositories directly.

### 3. Test the Implementation

Use the `tester` agent to verify the implementation against the Issue acceptance criteria.

The Tester focuses on:

* Normal cases
* Error cases
* Boundary conditions
* Regression risks

Tests are implemented with `pytest`.

The Tester should confirm that the implementation satisfies the expected behavior defined in the Issue.

### 4. Review the Changes

Use the `reviewer` agent to review the current changes.

The Reviewer checks:

* Functional defects
* Architecture violations
* Security issues
* Maintainability problems
* Missing tests
* Unnecessary changes
* Compliance with the Issue acceptance criteria

The Reviewer does not modify the source code.

If problems are found, the findings are returned to the Developer for correction.

The workflow may repeat:

```text
Developer
    ↓
Tester
    ↓
Reviewer
    │
    ├── Findings → Developer
    │                  ↓
    │                Tester
    │                  ↓
    │                Reviewer
    │
    └── No findings → Complete
```

### 5. Confirm Completion

Before creating a Pull Request, confirm that all acceptance criteria in the related Issue have been satisfied.

Example:

```text
[x] API accepts priority values
[x] API returns priority values
[x] Default priority is medium
[x] Invalid priority values are rejected
[x] Normal-case tests pass
[x] Error-case tests pass
```

### 6. Commit and Push

Commit the completed changes.

Example:

```bash
git add .
git commit -m "feat: add todo priority"
```

Push the feature branch:

```bash
git push -u origin feature/1-todo-priority
```

### 7. Create the Pull Request

Use the `pr-manager` agent to create a Pull Request from the completed feature branch to `main`.

GitHub operations are performed with GitHub CLI:

```bash
gh pr create
```

The Pull Request should contain:

* Summary
* Changes
* Testing
* Related Issue

The related Issue should be referenced with:

```text
Closes #<issue-number>
```

Example:

```text
Closes #1
```

This allows the related Issue to be closed automatically when the Pull Request is merged into `main`.

### Agent Responsibilities

| Agent         | Responsibility                                  |
| ------------- | ----------------------------------------------- |
| `issue-setup` | Create the Issue and prepare the feature branch |
| `developer`   | Implement the Issue                             |
| `tester`      | Verify behavior and add tests                   |
| `reviewer`    | Review implementation quality                   |
| `pr-manager`  | Create the Pull Request to `main`               |

### Customization Files

This project uses the following customization files:

| File                | Purpose                                            |
| ------------------- | -------------------------------------------------- |
| `AGENTS.md`         | Project-wide architecture and development policies |
| `*.instructions.md` | File- or technology-specific implementation rules  |
| `*.agent.md`        | Defines the responsibility and tools of each agent |
| `*.prompt.md`       | Defines reusable task-specific workflows           |

The relationship can be summarized as:

```text
AGENTS.md
    = Project-wide rules

*.instructions.md
    = Detailed implementation rules

*.agent.md
    = Who performs the task

*.prompt.md
    = What task is performed

tools
    = What capabilities the agent can use
```

### GitHub and Git Responsibilities

Git and GitHub CLI have separate roles in this workflow.

```text
Git
├── Branch creation
├── Switching branches
├── Commit
├── Diff
└── Push

GitHub CLI (`gh`)
├── Issue creation
├── Issue retrieval
├── Pull Request creation
└── Pull Request retrieval
```

The complete development flow is therefore:

```text
Requirement
    ↓
Issue
    ↓
Feature Branch
    ↓
Implementation
    ↓
Testing
    ↓
Review
    ↓
Commit / Push
    ↓
Pull Request
    ↓
main
```
