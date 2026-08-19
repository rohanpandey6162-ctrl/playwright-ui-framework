"""Central configuration for the framework: URLs, credentials, timeouts, browser settings."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """Holds all environment-level settings used across pages and tests."""

    BASE_URL: str = "https://www.saucedemo.com"

    # Standard demo credentials for saucedemo.com
    STANDARD_USER: str = "standard_user"
    LOCKED_OUT_USER: str = "locked_out_user"
    PROBLEM_USER: str = "problem_user"
    PERFORMANCE_GLITCH_USER: str = "performance_glitch_user"
    PASSWORD: str = "secret_sauce"

    # Timeouts (milliseconds) - used with Playwright's expect/wait_for_* APIs
    TIMEOUT: int = 10_000
    NAVIGATION_TIMEOUT: int = 15_000

    # Browser settings
    BROWSER: str = "chromium"  # chromium | firefox | webkit
    HEADLESS: bool = True
    SLOW_MO: int = 0
    VIEWPORT_WIDTH: int = 1280
    VIEWPORT_HEIGHT: int = 800

    # Paths
    SCREENSHOT_DIR: str = "screenshots"
    REPORT_DIR: str = "reports"


config = Config()
