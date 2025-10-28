# OTA Web Crawler

A Python Selenium-based web crawler for searching available rooms on Online Travel Agency (OTA) websites.

## Features

- 🔍 Search for hotel rooms by destination and dates
- 🏨 Built-in support for Booking.com
- 🔧 Extensible architecture for other OTA websites
- 💾 Save results to JSON format
- 📸 Screenshot capability for debugging
- 🎯 Handles popups and cookie banners automatically

## Prerequisites

- Python 3.7+
- Google Chrome browser
- ChromeDriver (will be managed automatically with webdriver-manager)

## Installation

1. **Clone or download the project files**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install ChromeDriver** (if not using webdriver-manager):
   - Download from: https://chromedriver.chromium.org/
   - Make sure it matches your Chrome version
   - Add to PATH or place in project directory

## Quick Start

### Basic Usage

```python
from ota_crawler import OTACrawler

# Initialize the crawler
crawler = OTACrawler(headless=False, timeout=15)

# Search for hotels
results = crawler.search_booking_com(
    destination="Paris",
    check_in="2025-12-15",
    check_out="2025-12-20",
    adults=2,
    rooms=1
)

# Display results
for hotel in results:
    print(f"{hotel['name']} - {hotel['price']}")

# Save to file
crawler.save_results(results, "paris_hotels.json")

# Close browser
crawler.close()
```

### Running the Example

Simply run the main script:
```bash
python ota_crawler.py
```

This will search for hotels in New York for December 1-5, 2025.

## Usage Examples

### Example 1: Weekend Getaway Search

```python
from ota_crawler import OTACrawler
from datetime import datetime, timedelta

crawler = OTACrawler(headless=False)

# Search for this weekend
today = datetime.now()
weekend_start = today + timedelta(days=(4 - today.weekday()) % 7)
weekend_end = weekend_start + timedelta(days=2)

results = crawler.search_booking_com(
    destination="Los Angeles",
    check_in=weekend_start.strftime("%Y-%m-%d"),
    check_out=weekend_end.strftime("%Y-%m-%d"),
    adults=2,
    rooms=1
)

crawler.save_results(results, "weekend_getaway.json")
crawler.close()
```

### Example 2: Headless Mode (No Browser Window)

```python
from ota_crawler import OTACrawler

# Run in headless mode (no GUI)
crawler = OTACrawler(headless=True, timeout=20)

results = crawler.search_booking_com(
    destination="Tokyo",
    check_in="2026-03-10",
    check_out="2026-03-15",
    adults=1,
    rooms=1
)

print(f"Found {len(results)} hotels")
crawler.close()
```

### Example 3: Custom OTA Website

```python
from ota_crawler import OTACrawler

crawler = OTACrawler()

# Define custom selectors for a different OTA
custom_selectors = {
    'destination': 'input#destination',
    'checkin': 'input#checkin',
    'checkout': 'input#checkout',
    'search_button': 'button.search-btn',
    'result_card': 'div.hotel-card',
    'name': 'h3.hotel-name',
    'price': 'span.price'
}

results = crawler.search_generic_ota(
    url="https://example-ota.com",
    selectors=custom_selectors,
    destination="London",
    check_in="2025-11-01",
    check_out="2025-11-05"
)

crawler.close()
```

## Configuration Options

### OTACrawler Parameters

- `headless` (bool): Run browser without GUI (default: False)
- `timeout` (int): Wait timeout in seconds (default: 10)

### search_booking_com Parameters

- `destination` (str): City, hotel name, or location to search
- `check_in` (str): Check-in date in 'YYYY-MM-DD' format
- `check_out` (str): Check-out date in 'YYYY-MM-DD' format
- `adults` (int): Number of adults (default: 2)
- `rooms` (int): Number of rooms (default: 1)

## Result Format

Results are returned as a list of dictionaries with the following structure:

```json
[
  {
    "name": "Hotel Name",
    "price": "$150 per night",
    "rating": "8.5",
    "location": "City Center"
  }
]
```

## Troubleshooting

### Common Issues

1. **ChromeDriver version mismatch**
   - Solution: Update Chrome browser or use webdriver-manager

2. **Element not found errors**
   - Website structure may have changed
   - Try increasing timeout value
   - Check if popups are blocking elements

3. **Slow performance**
   - Increase timeout values
   - Use headless mode
   - Check internet connection

4. **Popup/Cookie banner blocking**
   - The crawler has built-in popup handling
   - Add custom selectors to `_handle_popups()` if needed

### Debugging

Enable screenshots on errors:
```python
crawler._take_screenshot("debug_screen")
```

Check console output for detailed error messages.

## Extending the Crawler

### Adding Support for Another OTA

1. Create a new method in the `OTACrawler` class:

```python
def search_expedia(self, destination, check_in, check_out):
    self.driver.get("https://www.expedia.com")
    # Implement search logic
    # Use similar pattern to search_booking_com
    return results
```

2. Study the target website's HTML structure
3. Use browser DevTools to identify element selectors
4. Test with small modifications first

## Best Practices

1. **Respect robots.txt** - Check if crawling is allowed
2. **Add delays** - Use time.sleep() to avoid overwhelming servers
3. **Handle errors gracefully** - Wrap code in try-except blocks
4. **Rotate user agents** - If making many requests
5. **Use headless mode** - For production/scheduled tasks
6. **Save results incrementally** - For long-running searches

## Limitations

- Requires Chrome browser and ChromeDriver
- Website structure changes may break selectors
- Some OTAs may have anti-bot measures
- Results limited to first page (can be extended)
- Date selection logic specific to Booking.com calendar

## Future Enhancements

- [ ] Support for more OTA websites (Expedia, Hotels.com, Agoda)
- [ ] Multi-page result scraping
- [ ] Parallel processing for multiple searches
- [ ] Proxy support for distributed crawling
- [ ] Database integration
- [ ] Email notifications for price drops
- [ ] GUI interface

## Legal Notice

This tool is for educational purposes. Ensure compliance with:
- Website Terms of Service
- robots.txt policies
- Local laws regarding web scraping
- Data protection regulations

Always use responsibly and ethically.

## License

MIT License - Feel free to modify and distribute.

## Contributing

Contributions welcome! Please test thoroughly before submitting pull requests.

## Support

For issues or questions, please check:
1. Selenium documentation: https://selenium-python.readthedocs.io/
2. ChromeDriver releases: https://chromedriver.chromium.org/downloads
