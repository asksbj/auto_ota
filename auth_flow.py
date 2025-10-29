import time
from typing import Callable, Optional


def wait_for_login(
    light_check: Callable[[], bool],
    heavy_check: Callable[[], bool],
    navigate_login_once: Optional[Callable[[], None]] = None,
    auto_login: Optional[Callable[[], bool]] = None,
    wait_seconds: int = 300,
    poll_seconds: int = 5,
    use_light_mode: bool = True,
    on_progress: Optional[Callable[[int], None]] = None,
) -> bool:
    """
    Generic login flow helper.

    - First, run light/normal check (depending on use_light_mode). If logged in, return True.
    - If auto_login is provided, try it once. If still not logged in, proceed to manual wait.
    - Optionally call navigate_login_once() a single time before waiting (e.g., to open sign-in page from blank tab).
    - During waiting, poll using light_check (if use_light_mode) or heavy_check (if not) until timeout.
    - After success via light check, confirm once with heavy_check.
    """

    poll = max(1, int(poll_seconds))

    def report(remaining: int):
        if on_progress:
            try:
                on_progress(remaining)
            except Exception:
                pass

    # Initial check
    is_logged = light_check() if use_light_mode else heavy_check()
    if is_logged:
        if use_light_mode:
            return heavy_check()
        return True

    # Try auto login once
    if auto_login is not None:
        try:
            if auto_login():
                # Validate after auto login
                return heavy_check()
        except Exception:
            # Ignore and fall back to manual wait
            pass

    # Navigate to login page once if requested (non-intrusive helper)
    if navigate_login_once is not None:
        try:
            navigate_login_once()
        except Exception:
            pass

    # Manual wait loop
    deadline = time.time() + int(wait_seconds)
    while time.time() < deadline:
        remaining = int(deadline - time.time())
        report(max(0, remaining))
        time.sleep(min(poll, max(1, remaining)))
        if use_light_mode:
            if light_check():
                # confirm once
                return heavy_check()
        else:
            if heavy_check():
                return True

    return False


