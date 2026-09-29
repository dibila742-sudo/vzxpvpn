import base64
import re
import urllib.request
from urllib.parse import quote

BASE = "https://github.com/Au1rxx/free-vpn-subscriptions/raw/main/output/by-country/v2ray-base64-{}.txt"

COUNTRIES = [
    ("US", "🇺🇸 США"),
    ("CA", "🇨🇦 Канада"),
    ("DE", "🇩🇪 Германия"),
    ("FR", "🇫🇷 Франция"),
    ("HK", "🇭🇰 Гонконг"),
]

HEADER = (
    "#profile-title: VzxVpn\n"
    "#profile-update-interval: 1\n"
    "#announce: VzxVpn - США, Канада, Германия, Франция, Гонконг. Если не подключается, нажмите обновить подписку.\n"
)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore").strip()
    if "://" not in raw[:20]:
        raw += "=" * (-len(raw) % 4)
        raw = base64.b64decode(raw).decode("utf-8", "ignore")
    return raw.splitlines()


def main():
    out = []
    for code, name in COUNTRIES:
        try:
            lines = fetch(BASE.format(code))
        except Exception as e:
            print(code, "error", e)
            continue
        vless = [l.strip() for l in lines if l.strip().startswith("vless://")]
        if not vless:
            print(code, "no vless")
            continue
        link = re.sub(r"#.*$", "", vless[0]) + "#" + quote(name)
        out.append(link)
        print(code, "ok")
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(HEADER + "\n".join(out) + "\n")


main()
