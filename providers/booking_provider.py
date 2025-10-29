from typing import Any, Dict, List, Optional
from providers.base_provider import OTAProvider, AuthProvider


class BookingAuth(AuthProvider):
    def __init__(self, crawler: Any, config: Any):
        self.crawler = crawler
        self.config = config

    def light_check(self) -> bool:
        return self.crawler.is_booking_logged_in_light(self.config.BOOKING_SELECTORS)

    def heavy_check(self) -> bool:
        return self.crawler.is_booking_logged_in(self.config.BOOKING_SELECTORS)

    def navigate_login_once(self) -> None:
        try:
            current_url = self.crawler.driver.current_url or ""
            if current_url.startswith('data:') or 'about:blank' in current_url:
                self.crawler.driver.get(self.config.BOOKING_SELECTORS.get('login_page_url', 'https://account.booking.com/sign-in'))
        except Exception:
            pass

    def auto_login(self) -> bool:
        if not (self.config.BOOKING_EMAIL and self.config.BOOKING_PASSWORD):
            return False
        return self.crawler.login_booking(self.config.BOOKING_EMAIL, self.config.BOOKING_PASSWORD, self.config.BOOKING_SELECTORS)


class BookingProvider(OTAProvider):
    name = "booking"

    def get_auth(self) -> AuthProvider:
        return BookingAuth(self.crawler, self.config)

    def fetch_reservations(self) -> List[Dict[str, Any]]:
        return self.crawler.fetch_booking_reservations(self.config.BOOKING_SELECTORS)

    def search_comparable(self, reservation: Dict[str, Any]) -> List[Dict[str, Any]]:
        hotel_name = reservation.get('hotel_name', '')
        check_in = reservation.get('check_in', '') or self.config.CHECK_IN_DATE
        check_out = reservation.get('check_out', '') or self.config.CHECK_OUT_DATE
        return self.crawler.search_booking_com(
            destination=hotel_name,
            check_in=check_in,
            check_out=check_out,
            adults=self.config.NUM_ADULTS,
            rooms=self.config.NUM_ROOMS,
        )


