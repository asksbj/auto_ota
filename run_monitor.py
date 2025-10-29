#!/usr/bin/env python3
from datetime import datetime
import time
from ota_crawler import OTACrawler
import config
from notifier import send_email, send_sms
import re
from auth_flow import wait_for_login
from providers.booking_provider import BookingProvider
from providers.base_provider import OTAProvider
from providers.agoda_provider import AgodaProvider


def normalize_price(price_text: str) -> float:
    if not price_text:
        return 0.0
    nums = re.findall(r"[\d,.]+", price_text.replace("\u00a0", " "))
    if not nums:
        return 0.0
    value = nums[-1].replace(",", "")
    try:
        return float(value)
    except Exception:
        return 0.0


def is_future(check_in_text: str) -> bool:
    try:
        # Try several common formats; Booking varies by locale
        for fmt in ("%d %B %Y", "%Y-%m-%d", "%d %b %Y"):
            try:
                dt = datetime.strptime(check_in_text, fmt)
                return dt.date() >= datetime.today().date()
            except Exception:
                continue
    except Exception:
        pass
    return True


def main():
    crawler = OTACrawler(headless=config.HEADLESS_MODE, timeout=config.TIMEOUT)
    try:
        site = config.RESERVATION_SITE.lower()
        provider: OTAProvider
        if site == 'booking':
            provider = BookingProvider(crawler, config)
        elif site == 'agoda':
            provider = AgodaProvider(crawler, config)
        else:
            print(f"Site '{site}' not yet implemented. Supported: booking, agoda (skeleton)")
            return

        light_mode = bool(getattr(config, 'MONITOR_LIGHT_LOGIN_CHECK', True))
        auth = provider.get_auth()

        def light_check():
            return auth.light_check()

        def heavy_check():
            return auth.heavy_check()

        def navigate_login_once():
            return auth.navigate_login_once()

        def try_auto_login():
            return auth.auto_login()

        def on_progress(remaining: int):
            print(f"Waiting for manual login... ~{remaining}s left")

        logged_in = wait_for_login(
            light_check=light_check,
            heavy_check=heavy_check,
            navigate_login_once=navigate_login_once,
            auto_login=try_auto_login,
            wait_seconds=getattr(config, 'MONITOR_LOGIN_WAIT_SECONDS', 300),
            poll_seconds=getattr(config, 'MONITOR_LOGIN_POLL_SECONDS', 5),
            use_light_mode=light_mode,
            on_progress=on_progress,
        )

        if not logged_in:
            print("Login not completed within the allowed time.")
            return

        reservations = provider.fetch_reservations()
        if not reservations:
            print("No reservations found.")
            return

        notifications = []

        for res in reservations:
            if config.ONLY_CHECK_CANCELLABLE and not res.get('is_cancellable'):
                continue
            if not is_future(res.get('check_in', '')):
                continue

            hotel_name = res.get('hotel_name', '')
            room_type = res.get('room_type', '')
            check_in = res.get('check_in', '')
            check_out = res.get('check_out', '')
            original_price = normalize_price(res.get('price_total', ''))

            if not hotel_name or not check_in or not check_out:
                continue

            # Provider search for comparable offers
            search_results = provider.search_comparable(res)

            # Pick the best match per provider strategy
            matched = provider.pick_match(res, search_results)

            new_price = normalize_price((matched or {}).get('price', ''))
            if new_price > 0 and original_price > 0 and new_price + 1e-6 < original_price - max(0.0, config.PRICE_DROP_THRESHOLD):
                delta = original_price - new_price
                notifications.append({
                    'hotel_name': hotel_name,
                    'room_type': room_type,
                    'check_in': check_in,
                    'check_out': check_out,
                    'old_price': original_price,
                    'new_price': new_price,
                    'delta': delta,
                })

        if not notifications:
            print("No price drops found. Current reservations:")
            for idx, r in enumerate(reservations, 1):
                print(f"{idx}. {r.get('hotel_name','N/A')} | {r.get('check_in','?')} → {r.get('check_out','?')} | cancellable={bool(r.get('is_cancellable'))} | total={r.get('price_total','N/A')}")
            return

        # Prepare notification content
        subject = f"{site.capitalize()} price drop alerts ({len(notifications)})"
        html_lines = ["<h3>Price Drop Found</h3>"]
        text_sms_lines = []
        for n in notifications:
            html_lines.append(
                f"<p><b>{n['hotel_name']}</b> ({n['room_type']})<br/>"
                f"{n['check_in']} → {n['check_out']}<br/>"
                f"Old: {n['old_price']} | New: {n['new_price']} | ↓ {n['delta']:.2f}</p>"
            )
            text_sms_lines.append(
                f"{n['hotel_name']} {n['check_in']}→{n['check_out']} drop {n['old_price']}→{n['new_price']} (-{n['delta']:.2f})"
            )
        html_body = "\n".join(html_lines)
        sms_body = ("; ".join(text_sms_lines))[:1300]

        if config.ENABLE_EMAIL and config.EMAIL_TO and config.EMAIL_FROM and config.SMTP_HOST:
            try:
                send_email(
                    smtp_host=config.SMTP_HOST,
                    smtp_port=config.SMTP_PORT,
                    username=config.SMTP_USERNAME,
                    password=config.SMTP_PASSWORD,
                    sender=config.EMAIL_FROM,
                    recipients=config.EMAIL_TO,
                    subject=subject,
                    html_body=html_body,
                )
                print("Email sent.")
            except Exception as e:
                print(f"Failed to send email: {str(e)}")

        if config.ENABLE_SMS and config.TWILIO_ACCOUNT_SID and config.TWILIO_AUTH_TOKEN and config.TWILIO_FROM_NUMBER and config.TWILIO_TO_NUMBERS:
            try:
                send_sms(
                    account_sid=config.TWILIO_ACCOUNT_SID,
                    auth_token=config.TWILIO_AUTH_TOKEN,
                    from_number=config.TWILIO_FROM_NUMBER,
                    to_numbers=config.TWILIO_TO_NUMBERS,
                    body=sms_body,
                )
                print("SMS sent.")
            except Exception as e:
                print(f"Failed to send SMS: {str(e)}")

    finally:
        crawler.close()


if __name__ == "__main__":
    main()


