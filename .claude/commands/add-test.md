---
description: Implement a requested test case end-to-end — write it, verify it passes, commit, and push to the right PR/branch
argument-hint: <description of the test case or feature to automate>
---

# Test Automation Agent

## Trigger
Only run this when explicitly asked to automate/add/write a test case —
e.g. "automate the logout test", "can you add a test for X", "/add-test
<description>". Do not run proactively as a side effect of other tasks.

## Workflow

### 1. Clarify scope (ask if ambiguous)
- Confirm exactly what behavior/scenario to test if the request is vague
  (e.g. "automate the checkout" could mean the success path, validation,
  multi-item totals, or all three — ask which)
- Check whether a similar test already exists under `tests/` before
  writing a duplicate — if one's close, ask whether to extend it instead
  of adding a new one
- Confirm which pytest marker(s) apply (`smoke`, `regression`, `login`,
  `cart` — see `pytest.ini`); if the feature doesn't fit any existing
  marker, ask before inventing a new one (new markers must be registered
  in `pytest.ini`, not just used ad hoc)

### 2. Implement, following existing POM conventions
- Selectors and page interactions belong only in the relevant
  `pages/*.py` class — never inline in a test file
- If the target page/feature doesn't have a page object yet (e.g. the
  product-detail page, the burger menu), create one mirroring the
  structure of `pages/base_page.py` and the existing page objects:
  locators as class constants, a `load()` method, action/assertion
  methods, no raw Playwright calls leaking into tests
- Add the test to the matching `tests/test_*.py` file, or create a new
  one (e.g. `tests/test_menu.py`) if the feature doesn't fit an existing
  file — ask first if it's not obvious which file it belongs in
- Use the `logged_in_page` fixture unless the scenario specifically needs
  to exercise login/logout itself

### 3. Verify before touching git
- Run the new test(s) specifically first: `pytest tests/test_x.py::test_name -v`
- Then run the full suite (`pytest`) to confirm nothing else broke
- If a test fails, fix it — never commit a failing test, and never mark
  one `skip`/`xfail` to make the suite pass artificially

### 4. Branch safely — never commit directly to `main`
- Check the current branch: `git branch --show-current`
- If on `main`: create a new branch first. Derive a short kebab-case name
  from the feature (e.g. `add-logout-test`); ask for a name only if
  nothing reasonable can be derived from the request
- If already on a feature branch: reuse it

### 5. Commit and push
- Stage only the files this change actually touched
- Commit with a message describing what test was added and why it was
  needed — not a generic "add test"
- Check whether the current branch already has an open PR:
  `gh pr list --head <branch> --json number,url`
  - **PR exists**: `git push` — this updates the existing PR, nothing
    further to create
  - **No PR exists**: `git push -u origin <branch>`, then
    `gh pr create` with a summary of the test(s) added and confirmation
    that the suite passed locally (test plan section)

### 6. Ask, don't guess
- If test data needed for the scenario isn't in `utils/config.py` and
  isn't obvious (e.g. a new demo user, a specific input value), ask
  rather than inventing it
- If the request could reasonably map to more than one existing
  branch/PR, ask which one to target instead of assuming
- Never force-push, never rewrite history, never merge the PR — this
  command only gets the change onto an open PR for a human to merge

## Output
When done, report: what was added (files touched), local test results
(pass/fail counts), and the PR URL (new or updated).
