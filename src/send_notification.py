from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NOTIFICATION_PATH = ROOT / "outputs" / "notifications" / "notification_001.md"


def send_notification(notification_path: Path = DEFAULT_NOTIFICATION_PATH) -> bool:
    load_dotenv()

    if not notification_path.exists():
        print(f"Notification artifact missing: {notification_path.relative_to(ROOT).as_posix()}")
        return False

    notification_text = notification_path.read_text(encoding="utf-8")
    webhook_url = os.getenv("NOTIFICATION_WEBHOOK_URL")

    if not webhook_url:
        print("Webhook delivery skipped: NOTIFICATION_WEBHOOK_URL is not configured.")
        print(f"Notification artifact ready: {notification_path.relative_to(ROOT).as_posix()}")
        return False

    payload = json.dumps({"text": notification_text}).encode("utf-8")
    request = Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=10) as response:
            status_code = response.getcode()

        if 200 <= status_code < 300:
            print("Webhook notification delivered successfully.")
            return True

        print(f"Webhook delivery returned non-success status: {status_code}")
        print(f"Fallback notification artifact: {notification_path.relative_to(ROOT).as_posix()}")
        return False

    except (HTTPError, URLError, TimeoutError, OSError) as error:
        print(f"Webhook delivery failed: {error}")
        print(f"Fallback notification artifact: {notification_path.relative_to(ROOT).as_posix()}")
        return False


if __name__ == "__main__":
    send_notification()