<!-- 
-- +==== BEGIN polyguard =================+
-- LOGO:
--       input
-- 
--    @#$%!  hello
--      |     |
--      +--+--+
--         |
--         v
--   +------------+
--   | POLY GUARD |
--   +------------+
--     |        |
--     v        v
--  BLOCKED  PASSED
--    KO       OK
-- /STOP
-- PROJECT: polyguard
-- FILE: CONTRIBUTING.md
-- CREATION DATE: 13-03-2026
-- LAST Modified: 10:56:27 13-03-2026
-- DESCRIPTION:
-- A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
-- /STOP
-- COPYRIGHT: (c) Henry Letellier
-- PURPOSE: These are the guidelines about how one can contribute to the module.
-- // AR
-- +==== END polyguard =================+
-->

# Contributing to Polyguard module

Thank you for considering contributing to Polyguard module!
This document outlines the guidelines and processes for making contributions
to the project

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
    - [Reporting Issues](#reporting-issues)
    - [Feature Requests](#feature-requests)
    - [Submitting Changes](#submitting-changes)
3. [Coding Guidelines](#coding-guidelines)
4. [Commit Message Convention](#commit-message-convention)
5. [Branch Naming Convention](#branch-naming-convention)
6. [Pull Request Process](#pull-request-process)
7. [Setting Up the Development Environment](#setting-up-the-development-environment)

---

## Code of Conduct

We adhere to a [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming
and inclusive environment for all contributors

---

## How to Contribute

### Reporting Issues

If you encounter a bug or have a question:

1. Check if the issue has already been reported in the [Issues section](https://github.com/Hanra-s-work/polyguard/issues).
2. If not, create a new issue using the **Bug Report** or **Question** template.
3. Include detailed steps to reproduce the bug or context about your question.

### Feature Requests

To propose a new feature:

1. Check if the feature has already been requested.
2. Open a new issue using the **Feature Request** template.
3. Clearly describe the problem the feature solves and, if possible, provide examples of how it would be used.

### Submitting Changes

1. Fork the repository.
2. Create a new branch following the **Branch Naming Convention**.
3. Make your changes following the coding and commit guidelines.
4. Test your changes thoroughly before submitting a pull request.

---

## Coding Guidelines

- Follow the repository’s style and best practices.
- Ensure code is **documented and readable**.
- Add tests where applicable.
- Ensure CI checks pass before submitting a PR.

---

## Commit Message Convention

All commit messages **must** follow the rules defined in **[COMMIT_CONVENTION.md](COMMIT_CONVENTION.md)**

Commits describe **individual actions** taken during development.

---

## Branch Naming Convention

Branches represent a **work context**, not a single type of change.
A single branch may include fixes, additions, tests, refactors,
and documentation updates.

### Important Git Limitation

Git branch names are stored as filesystem paths.

As a result, **a branch name cannot be both a prefix and a leaf**.

If a branch named:

```plaintext
backend/endpoints
```

exists, then branches such as:

```plaintext
backend/endpoints/user_id
```

**cannot exist** (and vice versa).

### General Rules

- Slash-separated names are used for logical grouping.
- Top-level names are **namespaces only** and must not exist as standalone branches.
- Every branch must represent a **concrete unit of work**.
- Avoid category-only branches such as:
  `backend`, `docker`, `documentation`.

### Naming Structure

```plaintext
<component>/<section>/<work-item>
```

The **last segment** must always be the actual branch.

### Component Prefixes

| Component        | Prefix Example          |
|------------------|-------------------------|
| Backend code     | `backend/...`           |
| Backend tests    | `backend/tests/...`     |
| Docker / CI      | `docker/...`            |
| Documentation    | `documentation/...`     |
| Automation       | `automation/...`        |
| Miscellaneous    | `etc/...`               |

### Examples

#### Valid

- backend/endpoints/user_id
- backend/tests/unit/auth
- docker/ci
- documentation/deployment
- automation/release

#### Invalid

- backend
- backend/endpoints
- backend/endpoints + backend/endpoints/user_id

---

## Pull Request Process

1. Ensure your branch is up to date with the `main` branch.
2. Create a pull request with a clear title and description of your changes.
3. Link any relevant issues in the pull request description.
4. Ensure the following checks pass:
   - Code adheres to the guidelines.
   - All tests pass.
   - There are no conflicts with the `prod` branch.

5. A reviewer will assess your pull request. Please address their feedback promptly.

---

## Setting Up the Development Environment

In order to use the project locally, please, make sure you have docker installed and running, then run the following command for your system command:

You can see the [Getting started](./README.md#getting-started) in the readme server.
