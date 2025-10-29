from typing import Any, Dict, List, Optional
from providers.base_provider import OTAProvider, AuthProvider


class AgodaAuth(AuthProvider):
    def __init__(self, crawler: Any, config: Any):
        self.crawler = crawler
        self.config = config

    def light_check(self) -> bool:
        try:
            url = (self.crawler.driver.current_url or "").lower()
            if any(k in url for k in ["agoda.com/account", "/mybookings", "/account/booking"]):
                return True
            # Simple header/account icon heuristic if present
            sel = (getattr(self.config, 'AGODA_SELECTORS', {}) or {}).get('account_menu', '[data-element-name="header-account-menu"]')
            if self.crawler.driver.find_elements_by_css_selector(sel):
                return True
        except Exception:
            pass
        return False

    def heavy_check(self) -> bool:
        try:
            url = (getattr(self.config, 'AGODA_SELECTORS', {}) or {}).get('reservations_page_url', 'https://www.agoda.com/account/booking')
            self.crawler.driver.get(url)
            self.crawler._handle_popups()
            # Presence of any reservation list container would indicate login
            sel = (getattr(self.config, 'AGODA_SELECTORS', {}) or {}).get('reservation_card', '.BookingCard')
            cards = self.crawler.driver.find_elements_by_css_selector(sel)
            return len(cards) >= 0  # if page loads without redirecting to login, treat as logged in
        except Exception:
            return False

    def navigate_login_once(self) -> None:
        try:
            current_url = self.crawler.driver.current_url or ""
            if current_url.startswith('data:') or 'about:blank' in current_url:
                login_url = (getattr(self.config, 'AGODA_SELECTORS', {}) or {}).get('login_page_url', 'https://www.agoda.com/account/signin')
                self.crawler.driver.get(login_url)
        except Exception:
            pass

    def auto_login(self) -> bool:
        # Not implemented for Agoda; manual login expected
        return False


class AgodaProvider(OTAProvider):
    name = "agoda"

    def get_auth(self) -> AuthProvider:
        return AgodaAuth(self.crawler, self.config)

    def fetch_reservations(self) -> List[Dict[str, Any]]:
        # Skeleton: Not implemented. Return empty list to allow script to proceed gracefully.
        print("AgodaProvider.fetch_reservations: not implemented yet.")
        return []

    def search_comparable(self, reservation: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Skeleton: Not implemented. You can implement via crawler.search_generic_ota with proper selectors.
        print("AgodaProvider.search_comparable: not implemented yet.")
        return []


