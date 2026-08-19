# Playwright UI Automation Framework (Python + pytest + POM)

A UI test automation framework for [saucedemo.com](https://www.saucedemo.com), built with
**Playwright**, **pytest**, and the **Page Object Model (POM)** design pattern.

## Project Overview

- **Language/tools**: Python, Playwright (sync API), pytest
- **Pattern**: Page Object Model — page locators and actions live in `pages/`, test logic
  and assertions live in `tests/`
- **Target site**: https://www.saucedemo.com (a public demo e-commerce site made for
  automation practice)
- **Coverage**: login (valid/invalid/locked-out user), product listing (sorting, add/remove),
  cart management, and the full checkout flow

```
playwright-ui-framework/
├── pages/                  # Page Object classes
│   ├── base_page.py        # Common reusable actions (click, fill, wait, screenshot, ...)
│   ├── login_page.py       # Login page locators + actions
│   ├── inventory_page.py   # Products/inventory page locators + actions
│   └── cart_page.py        # Cart + checkout locators + actions
├── tests/                  # Test files
│   ├── conftest.py         # Fixtures: browser/context/page lifecycle, failure screenshots, logged_in_page
│   ├── test_login.py       # Login tests
│   ├── test_inventory.py   # Product listing tests
│   └── test_cart.py        # Cart + checkout tests
├── utils/
│   └── config.py           # BASE_URL, credentials, timeouts, browser settings
├── reports/                 # Generated HTML test reports
├── screenshots/             # Auto-captured screenshots for failed tests
├── pytest.ini
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10+
- pip

## Installation

From the project root:

```bash
# 1. (Recommended) create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Playwright's browser binaries
playwright install
```

## Running the Tests

Run the full suite:

```bash
pytest
```

Run a specific test file:

```bash
pytest tests/test_login.py
```

Run in headed mode (see the browser), by editing `utils/config.py` and setting
`HEADLESS: bool = False`, or temporarily overriding it:

```bash
python -c "import utils.config as c; c.config.HEADLESS=False" # not persistent — prefer editing config.py directly
```

### Run by marker

Registered markers: `smoke`, `regression`, `login`, `cart`.

```bash
# Only smoke tests
pytest -m smoke

# Only regression tests
pytest -m regression

# Only login-related tests
pytest -m login

# Only cart/checkout tests
pytest -m cart

# Combine markers
pytest -m "smoke and cart"
```

### Viewing the HTML report

Every run generates a self-contained HTML report at `reports/report.html`
(configured via `pytest.ini`). After a run, open it directly:

```bash
open reports/report.html          # macOS
xdg-open reports/report.html      # Linux
start reports/report.html         # Windows
```

### Screenshots on failure

The `page` fixture in `tests/conftest.py` automatically captures a full-page
screenshot into `screenshots/` whenever a test fails, named after the test's
node ID for easy correlation with the failure.

## Notes

- All waits rely on Playwright's built-in auto-waiting (`locator.click()`,
  `locator.fill()`, `locator.wait_for()`); no explicit `sleep()` calls are used.
- Credentials and environment settings are centralized in `utils/config.py` —
  update `BASE_URL`, `STANDARD_USER`, `PASSWORD`, or `TIMEOUT` there rather than
  hardcoding values in tests.
- The `logged_in_page` fixture (in `conftest.py`) logs in as the standard user
  once per test and hands back an authenticated `Page`, so inventory/cart tests
  don't need to repeat login steps.
