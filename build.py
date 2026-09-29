import base64
import re
import socket
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote, urlparse

BASE = "https://github.com/Au1rxx/free-vpn-subscriptions/raw/main/output/by-country/v2ray-base64-{}.txt"

COUNTRIES = [
    ("US", "🇺🇸 США"),
    ("CA", "🇨🇦 Канада"),
    ("DE", "🇩🇪 Германия"),
    ("FR", "🇫🇷 Франция"),
    ("HK", "🇭🇰 Гонконг"),
    ("JP", "🇯🇵 Япония"),
    ("NL", "🇳🇱 Нидерланды"),
    ("SG", "🇸🇬 Сингапур"),
    ("KR", "🇰🇷 Корея"),
    ("TW", "🇹🇼 Тайвань"),
    ("PL", "🇵🇱 Польша"),
    ("GB", "🇬🇧 Британия"),
    ("FI", "🇫🇮 Финляндия"),
    ("EE", "🇪🇪 Эстония"),
    ("IN", "🇮🇳 Индия"),
    ("AT", "🇦🇹 Австрия"),
    ("ES", "🇪🇸 Испания"),
    ("AU", "🇦🇺 Австралия"),
    ("LV", "🇱🇻 Латвия"),
    ("RO", "🇷🇴 Румыния"),
]

PER_COUNTRY = 1
MAX_CHECK = 300

HEADER = (
    "#profile-title: VzxVpn\n"
    "#profile-update-interval: 1\n"
    "#announce: VzxVpn - 20 стран, первый сервер с самым низким пингом. Если не подключается, нажмите обновить подписку.\n"
)


def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore").strip()
        if "://" not in raw[:20]:
            raw += "=" * (-len(raw) % 4)
            raw = base64.b64decode(raw).decode("utf-8", "ignore")
        return raw.splitlines()
    except Exception as e:
        print("error", url, e)
        return []


def vless_links(url):
    res = []
    for l in fetch(url):
        l = l.strip()
        if l.startswith("vless://"):
            res.append(re.sub(r"#.*$", "", l))
    return res[:MAX_CHECK]


def ping(link):
    try:
        u = urlparse(link)
        t = time.time()
        s = socket.create_connection((u.hostname, u.port), timeout=3)
        s.close()
        return int((time.time() - t) * 1000)
    except Exception:
        return None


def check(links):
    with ThreadPoolExecutor(100) as ex:
        pings = list(ex.map(ping, links))
    alive = [(p, l) for p, l in zip(pings, links) if p is not None]
    alive.sort()
    return alive


def main():
    groups = []
    for code, name in COUNTRIES:
        best = check(vless_links(BASE.format(code)))[:PER_COUNTRY]
        print(name, len(best))
        groups.append((name, best))

    everything = sorted(x for _, g in groups for x in g)
    out = []
    if everything:
        p, l = everything[0]
        out.append(l + "#" + quote(f"🚀 Мин. пинг ({p} мс)"))
    for name, g in groups:
        for p, l in g:
            out.append(l + "#" + quote(f"{name} ({p} мс)"))

    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(HEADER + "\n".join(out) + "\n")


main()
