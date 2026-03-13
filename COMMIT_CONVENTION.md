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
-- FILE: COMMIT_CONVENTION.md
-- CREATION DATE: 13-03-2026
-- LAST Modified: 10:55:3 13-03-2026
-- DESCRIPTION:
-- A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
-- /STOP
-- COPYRIGHT: (c) Henry Letellier
-- PURPOSE: This is the file that will provide the norm we used when writing our commits in the repository.
-- // AR
-- +==== END polyguard =================+
-->

# Commit convention

This document describes the **commit message conventions** used in this repository.

This project **does not follow Conventional Commits strictly**.  
Instead, commit messages are **action-oriented** and written to clearly
describe *what changed*.

## Commit Message Convention

Each commit message **must** follow the format below:

```plaintext

[UPPERCASE INFINITIVE VERB] <concise description>

```

## Commit Message Rules

* **Prefix**
  * Must be an **uppercase infinitive verb**
  * Must be enclosed in square brackets (`[]`)
* **Description**
  * Short, clear, and written in present tense
  * Avoid past tense and gerunds (`-ing`)
* **Body (Optional)**
  * May be used to explain context, reasoning, or side effects

### Examples

* `[REMOVE] redundant code from the user service`
* `[EDIT] UI to match updated mockups`
* `[RENAME] Readme.md -> README.md`

### Common Commit Verbs

| Verb         | Description                                          | Example                                 |
|--------------|------------------------------------------------------|-----------------------------------------|
| **ADD**      | Introduces new functionality, features, or files     | `[ADD] cron jobs to clean expired tokens` |
| **FIX**      | Corrects bugs or issues in the codebase              | `[FIX] the database connection timeout` |
| **UPDATE**   | Improves or modifies existing functionality          | `[UPDATE] the login flow for better UX` |
| **REMOVE**   | Deletes or removes code, files, or dependencies      | `[REMOVE] outdated npm packages`        |
| **EDIT**     | Adjusts or alters existing code without major change | `[EDIT] the README for better clarity`  |
| **REFACTOR** | Refactors code without changing its behavior         | `[REFACTOR] server-side validation logic`|
| **RENAME**   | Renames files or variables                           | `[RENAME] variables to follow naming convention` |
| **MERGE**    | Merges branches or pull requests                     | `[MERGE] branch 'feature-auth' into dev`|

## Notes

* A single branch may contain **multiple types of commits**
  (e.g. fixes, additions, tests, refactors).
* Commit messages describe **what was done**, not why it was planned.

### Additional Notes

* **Prefixes** should always be in uppercase to clearly identify the action if they are encapsulated by `[]`
* Try to keep descriptions concise and to the point. Use the body for further elaboration if needed.
* If the commit is related to workflows or external dependencies, be explicit in the description.

### Examples from this Repository

* `[FIX] the path to the import of the EntityNode.hpp file`
* `[ADD] a window utility management class`
* `[ADD] a window that can open`
* `[FIX] exception handling issues`
* `[UPDATE] the type of the mainloop function`

## Related Conventions

Branch naming rules and workflow guidelines are defined in:

👉 **[CONTRIBUTING.md — Branch Naming Convention](CONTRIBUTING.md#branch-naming-convention)**

Please ensure your branch name follows those rules before committing.
