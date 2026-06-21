import httpx
import re
import os
from datetime import datetime, timezone

MIRRORS = [
    "v2tetotech.onrender.com",
]

README_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'README.md')

def is_sleep_time() -> bool:
    hour_utc = datetime.now(timezone.utc).hour
    return hour_utc >= 23 or hour_utc < 3

def check_server(url: str) -> str:
    try:
        response = httpx.get(f"https://{url}/svinfo", timeout=60.0)
        if response.status_code == 200:
            return "🟢"
        else:
            return "🔴"
    except Exception as e:
        print(f"⚠️ Error pinging {url}: {e}")
        return "🔴"

def update_readme():
    if not os.path.exists(README_PATH):
        print(f"❌ README.md not found at {README_PATH}")
        return

    with open(README_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    sleep = is_sleep_time()

    for mirror in MIRRORS:
        if sleep:
            status = "💤"
            print(f"💤 {mirror} is sleeping (23:00-03:00 UTC)...")
        else:
            status = check_server(mirror)
            print(f"{status} {mirror} status updated")

        pattern = re.compile(rf'({re.escape(mirror)}.*?)\s*[🟢🔴💤]\s*$', re.MULTILINE)

        if pattern.search(content):
            content = pattern.sub(rf'\1 {status}', content)
        else:
            print(f"⚠️ Line for {mirror} not found in README.md. Please add it manually.")

    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ README.md updated successfully!")

if __name__ == "__main__":
    update_readme()
