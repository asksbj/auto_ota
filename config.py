# Configuration file for OTA Crawler
# Edit these values to customize your search

# Search Parameters
DESTINATION = "New York"
CHECK_IN_DATE = "2025-12-01"  # Format: YYYY-MM-DD
CHECK_OUT_DATE = "2025-12-05"  # Format: YYYY-MM-DD
NUM_ADULTS = 2
NUM_ROOMS = 1

# Crawler Settings
HEADLESS_MODE = False  # Set to True to run without browser window
TIMEOUT = 15  # Seconds to wait for elements

# Output Settings
OUTPUT_FILE = "search_results.json"

# OTA Website Selection
OTA_SITE = "booking"  # Options: 'booking', 'custom'

# Custom OTA Selectors (for generic OTA websites)
CUSTOM_SELECTORS = {
    'destination': 'input[name="destination"]',
    'checkin': 'input[name="checkin"]',
    'checkout': 'input[name="checkout"]',
    'search_button': 'button[type="submit"]',
    'result_card': 'div.hotel-card',
    'name': 'h3.hotel-name',
    'price': 'span.price',
    'rating': 'span.rating'
}

CUSTOM_OTA_URL = "https://flight.qunar.com/"
