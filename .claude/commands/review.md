---
description: Review a PR, branch, or the current diff for coding standards and POM compliance
argument-hint: [PR number | branch name] (leave empty to review local changes)
---

# Code Review Agent

## Trigger
Only perform a code review when explicitly asked — e.g. "review this",
"review my changes", "/review". Do not review proactively on file edits,
commits, or as a side effect of other tasks.

## Scope
Invoked as `/review $ARGUMENTS`. Resolve what to diff, in this order:
- **$ARGUMENTS looks like a PR number** (e.g. `12` or `#12`): fetch it with
  `gh pr diff 12` and review that diff. Use `gh pr view 12` first if you
  need the PR's base branch or description for context.
- **$ARGUMENTS looks like a branch name**: diff it against the repo's
  default branch, e.g. `git diff main...<branch>` (use `origin/HEAD` to
  find the default branch if unsure).
- **$ARGUMENTS is empty**:
  - Uncommitted changes (`git diff`) if present
  - Otherwise, the most recent commit (`git diff HEAD~1`)

This command never runs on its own — you always trigger it by hand,
whether that's on your own working tree or on someone else's PR/branch
you're reviewing.

## What to check

### 1. Coding standards
- Naming conventions (methods, variables, classes) consistent with the
  rest of the codebase
- Formatting/linting consistent with existing files (indentation,
  import order, docstrings/comments where the codebase already uses them)
- No hardcoded values that should be config/env-driven (URLs, credentials,
  timeouts, test data)
- Proper error handling — no bare except/catch blocks, no swallowed exceptions
- No dead code, commented-out blocks, or debug print/console.log left in
- Reasonable function/method length and single responsibility — flag
  anything doing too much

### 2. Page Object Model (POM) compliance
- Test files must not contain raw selectors — selectors belong in the
  corresponding page object class only
- Test files should only call page object methods (actions/assertions),
  not interact with the browser/driver directly
- New page objects follow the existing structure/naming pattern used
  elsewhere in the framework (check an existing page object file as the
  reference before flagging deviations)
- No duplicated selectors across multiple page object files — reuse or
  centralize
- Locators use the most stable available strategy consistent with what
  the framework already uses (data-testid / role-based / etc.) — flag
  brittle selectors (deep CSS chains, index-based XPath) as a POM
  hygiene issue, not just a style nitpick

### 3. Ask questions
- Before flagging something as wrong, if intent is ambiguous, ask rather
  than assume — e.g. "This selector is defined directly in the test
  file instead of the page object — was that intentional for a
  one-off check, or should it move into the page object?"
- If a change touches a pattern not seen elsewhere in the codebase, ask
  whether it's a deliberate new convention before treating it as a
  violation
- Don't silently "fix" things — surface the question or suggestion and
  let the user decide

## Output format
For each review, structure the response as:
1. **Summary** — one or two lines on overall state of the change
2. **Coding standards** — bullet list of issues found (file:line), or
   "No issues found"
3. **POM compliance** — bullet list of issues found (file:line), or
   "No issues found"
4. **Questions** — anything ambiguous that needs the user's input, or
   "None"
5. **Suggested fixes** — concrete diff/snippet only for issues you're
   confident about; don't auto-apply changes without confirmation
