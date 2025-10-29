from typing import Any, Dict, List, Optional, Callable


class AuthProvider:
    def light_check(self) -> bool:
        raise NotImplementedError

    def heavy_check(self) -> bool:
        raise NotImplementedError

    def navigate_login_once(self) -> None:
        pass

    def auto_login(self) -> bool:
        return False


class OTAProvider:
    """Abstract provider for an OTA site."""

    name: str = "generic"

    def __init__(self, crawler: Any, config: Any):
        self.crawler = crawler
        self.config = config

    # Auth
    def get_auth(self) -> AuthProvider:
        raise NotImplementedError

    # Reservations
    def fetch_reservations(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

    # Search comparable offers for reservation
    def search_comparable(self, reservation: Dict[str, Any]) -> List[Dict[str, Any]]:
        raise NotImplementedError

    # Match the same hotel/room if possible; otherwise pick the best comparable item
    def pick_match(self, reservation: Dict[str, Any], search_results: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not search_results:
            return None
        # Default: try name equality else first item
        hotel = reservation.get('hotel_name', '').strip().lower()
        for item in search_results:
            if item.get('name', '').strip().lower() == hotel:
                return item
        return search_results[0]


