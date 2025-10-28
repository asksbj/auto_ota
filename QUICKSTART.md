# Quick Start Guide - OTA Web Crawler

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Edit Your Search Parameters
Open `config.py` and modify:
```python
DESTINATION = "Your City"
CHECK_IN_DATE = "2025-12-01"
CHECK_OUT_DATE = "2025-12-05"
NUM_ADULTS = 2
NUM_ROOMS = 1
```

### Step 3: Run the Crawler
```bash
python run_search.py
```

That's it! Results will be saved to `search_results.json`

---

## 📝 Alternative: Use Directly in Python

```python
from ota_crawler import OTACrawler

crawler = OTACrawler(headless=False)

results = crawler.search_booking_com(
    destination="Paris",
    check_in="2025-12-15",
    check_out="2025-12-20",
    adults=2,
    rooms=1
)

for hotel in results:
    print(f"{hotel['name']} - {hotel['price']}")

crawler.close()
```

---

## 📁 Files Included

- **ota_crawler.py** - Main crawler class
- **run_search.py** - Simple runner script
- **config.py** - Configuration file
- **requirements.txt** - Python dependencies
- **README.md** - Full documentation

---

## 💡 Tips

1. **First time?** Keep `HEADLESS_MODE = False` to see what's happening
2. **Production?** Set `HEADLESS_MODE = True` for faster execution
3. **Different OTA?** Check README.md for custom OTA instructions
4. **Errors?** Increase `TIMEOUT` value in config.py

---

## ⚙️ System Requirements

- Python 3.7+
- Google Chrome browser
- Internet connection

---

## 🔍 What It Does

✅ Opens OTA website (Booking.com by default)
✅ Enters your destination
✅ Selects check-in and check-out dates
✅ Searches for available rooms
✅ Extracts hotel name, price, rating, location
✅ Saves results to JSON file

---

## 🆘 Need Help?

Check the full README.md for:
- Detailed examples
- Troubleshooting guide
- How to add more OTA websites
- Advanced configurations

Happy crawling! 🕷️
