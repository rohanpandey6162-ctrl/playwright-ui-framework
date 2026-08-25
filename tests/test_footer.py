"""Footer tests: social media links present on the authenticated app shell."""
import pytest

from pages.footer_component import FooterComponent


@pytest.mark.regression
def test_social_media_links_have_valid_hrefs(logged_in_page):
    """The footer's Twitter, Facebook, and LinkedIn links should point to real Sauce Labs URLs."""
    footer = FooterComponent(logged_in_page)

    assert footer.get_twitter_href() == "https://twitter.com/saucelabs"
    assert footer.get_facebook_href() == "https://www.facebook.com/saucelabs"
    assert footer.get_linkedin_href() == "https://www.linkedin.com/company/sauce-labs/"
