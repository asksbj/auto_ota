#!/usr/bin/env python3
"""
Simple runner script for OTA Crawler
Edit config.py to customize your search parameters
"""

from ota_crawler import OTACrawler
import config


def run_search():
    """Run OTA search based on config.py settings"""
    
    print("="*60)
    print("OTA CRAWLER - Starting Search")
    print("="*60)
    print(f"Destination: {config.DESTINATION}")
    print(f"Check-in: {config.CHECK_IN_DATE}")
    print(f"Check-out: {config.CHECK_OUT_DATE}")
    print(f"Adults: {config.NUM_ADULTS}, Rooms: {config.NUM_ROOMS}")
    print(f"Headless mode: {config.HEADLESS_MODE}")
    print("="*60 + "\n")
    
    # Initialize crawler
    crawler = OTACrawler(
        headless=config.HEADLESS_MODE,
        timeout=config.TIMEOUT
    )
    
    results = []
    
    try:
        if config.OTA_SITE.lower() == "booking":
            # Search Booking.com
            results = crawler.search_booking_com(
                destination=config.DESTINATION,
                check_in=config.CHECK_IN_DATE,
                check_out=config.CHECK_OUT_DATE,
                adults=config.NUM_ADULTS,
                rooms=config.NUM_ROOMS
            )
        
        elif config.OTA_SITE.lower() == "custom":
            # Search custom OTA
            results = crawler.search_generic_ota(
                url=config.CUSTOM_OTA_URL,
                selectors=config.CUSTOM_SELECTORS,
                destination=config.DESTINATION,
                check_in=config.CHECK_IN_DATE,
                check_out=config.CHECK_OUT_DATE
            )
        
        else:
            print(f"Unknown OTA site: {config.OTA_SITE}")
            print("Please set OTA_SITE to 'booking' or 'custom' in config.py")
        
        # Display results
        if results:
            print("\n" + "="*60)
            print(f"FOUND {len(results)} RESULTS")
            print("="*60 + "\n")
            
            for idx, hotel in enumerate(results, 1):
                print(f"{idx}. {hotel.get('name', 'N/A')}")
                print(f"   Price: {hotel.get('price', 'N/A')}")
                print(f"   Rating: {hotel.get('rating', 'N/A')}")
                print(f"   Location: {hotel.get('location', 'N/A')}")
                print()
            
            # Save results
            crawler.save_results(results, config.OUTPUT_FILE)
            print(f"\n✓ Results saved to {config.OUTPUT_FILE}")
        else:
            print("\n⚠ No results found. Please check your search parameters.")
        
    except Exception as e:
        print(f"\n✗ Error during search: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        crawler.close()
        print("\n" + "="*60)
        print("Search completed!")
        print("="*60)


if __name__ == "__main__":
    run_search()
