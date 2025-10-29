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

# Optional: persist Chrome session to keep login state
CHROME_USER_DATA_DIR = ""  # e.g. "/Users/asks/Library/Application Support/Google/Chrome/Profile 1"

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

# Reservation Monitoring Settings
RESERVATION_SITE = "booking"  # Currently supported: 'booking'

# Booking.com account credentials (required for reservation monitoring)
BOOKING_EMAIL = "asksbj@outlook.com"
BOOKING_PASSWORD = ""

# Notification settings
ENABLE_EMAIL = False
ENABLE_SMS = False

# Email (SMTP) configuration
SMTP_HOST = ""
SMTP_PORT = 587
SMTP_USERNAME = ""
SMTP_PASSWORD = ""
EMAIL_FROM = ""
EMAIL_TO = [
    # "your@email.com"
]

# Twilio SMS configuration
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_FROM_NUMBER = ""
TWILIO_TO_NUMBERS = [
    # "+11234567890"
]

# Booking.com selectors for login and reservations page
BOOKING_SELECTORS = {
    'login_page_url': 'https://account.booking.com/sign-in',
    'email_input': 'input[type="email"]',
    'continue_button': 'button[type="submit"]',
    'password_input': 'input[type="password"]',
    'reservations_page_url': 'https://secure.booking.com/myreservations.html',
    'trips_page_url': 'https://secure.booking.com/mytrips.html',
    'reservation_card': '[data-testid="booking-card"]',
    'reservation_card_alt': '[data-testid*="booking"]',
    'hotel_name': '[data-testid="property-name"]',
    'room_type': '[data-testid="room-type"]',
    'date_range': '[data-testid="stay-dates"]',
    'price_total': '[data-testid="total-price"]',
    'cancellation_policy': '[data-testid="cancellation-policy"]',
    'reservation_status': '[data-testid="reservation-status"]',
}

# Monitoring behavior
ONLY_CHECK_CANCELLABLE = True
LOOKAHEAD_DAYS = 365  # Only consider reservations within this many days
PRICE_DROP_THRESHOLD = 1.0  # Notify if new total is lower by at least this amount (in same currency units)

# Agoda placeholders (for future provider implementation)
AGODA_SELECTORS = {
    'login_page_url': 'https://www.agoda.com/account/signin',
    'reservations_page_url': 'https://www.agoda.com/account/booking',
    'account_menu': '[data-element-name="header-account-menu"]',
    'reservation_card': '.BookingCard',
}

# Manual login wait (seconds) when not logged in and no credentials are provided
MONITOR_LOGIN_WAIT_SECONDS = 300
MONITOR_LOGIN_POLL_SECONDS = 5  # Check login status every N seconds while waiting
MONITOR_LIGHT_LOGIN_CHECK = True  # During manual login wait, do not navigate; check DOM/URL only
