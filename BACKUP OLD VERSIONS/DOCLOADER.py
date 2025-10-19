import os, sys

UA_FILE = "UA.txt"
PROXY_FILE = "Proxie.txt"
REFERER_FILE = "Referers.txt"

DEFAULT_UA = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/15.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/117.0"
]

DEFAULT_PROXY = [
    "http://127.0.0.1:9050",
    "socks4://127.0.0.1:9050",
    "socks5://127.0.0.1:9050"
]

DEFAULT_REFERER = [
    "https://www.google.com",
    "https://www.bing.com",
    "https://duckduckgo.com",
    "https://search.yahoo.com",
    "https://www.baidu.com",
    "https://yandex.com",
    "https://www.startpage.com",
    "https://www.ecosia.org",
    "https://www.qwant.com",
    "https://search.brave.com",
    "https://www.mojeek.com",
    "https://searx.org",
    "https://www.dogpile.com",
    "https://www.webcrawler.com",
    "https://www.ixquick.com",
    "https://www.gigablast.com",
    "https://swisscows.com",
    "https://metager.org",
    "https://www.youtube.com",
    "https://www.google.com",
    "https://news.google.com",
    "https://scholar.google.com",
    "https://www.reddit.com",
    "https://twitter.com",
    "https://x.com",
    "https://github.com",
    "https://stackoverflow.com",
    "https://www.amazon.com",
    "https://web.archive.org",
    "https://search.crossref.org",
    "https://ahmia.fi",
    "https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion",
    "https://brave.com"
]


def docloader(filename, proxy_list=False):
    try:
        loaded_items = []

        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, filename)

        if not os.path.exists(path):
            if filename == UA_FILE:
                print(f'Error {filename} Not Found. Now Using Default Configuration')
                return DEFAULT_UA
            elif filename == PROXY_FILE:
                print(f'Error {filename} Not Found. Now Using Default Configuration')
                return DEFAULT_PROXY
            elif filename == REFERER_FILE:
                print(f'Error {filename} Not Found. Now Using Default Configuration')
                return DEFAULT_REFERER
            return []

        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                item = line.strip()
                if item and not item.startswith("#"):
                    if proxy_list:
                        if "://" in item:
                            loaded_items.append(item)
                    else:
                        loaded_items.append(item)

        if not loaded_items:
            if filename == UA_FILE:
                print(f'Error {filename} Is Not Configuration Files / Malformed. Now Using Default Configuration')
                return DEFAULT_UA
            elif filename == PROXY_FILE:
                print(f'Error {filename} Is Not Configuration Files / Malformed. Now Using Default Configuration')
                return DEFAULT_PROXY
            elif filename == REFERER_FILE:
                print(f'Error {filename} Is Not Configuration Files / Malformed. Now Using Default Configuration')
                return DEFAULT_REFERER
        return loaded_items

    except Exception as e:
        print(f'[ERR] Failed To Load {filename}: {e}')
        if filename in [UA_FILE, PROXY_FILE, REFERER_FILE]:
            if filename == UA_FILE:
                print(f'Error {filename} Not Found. Now Using Default Configuration')
                return DEFAULT_UA
            elif filename == PROXY_FILE:
                print(f'Error {filename} Not Found. Now Using Default Configuration')
                return DEFAULT_PROXY
            elif filename == REFERER_FILE:
                print(f'Error {filename} Not Found. Now Using Default Configuration')
                return DEFAULT_REFERER
        return []


ua = docloader(UA_FILE)
pr = docloader(PROXY_FILE, proxy_list=True)
re = docloader(REFERER_FILE)

if __name__ == "__main__":
    print(f"USER AGENTS {len(ua)}")
    print(f"PROXIES {len(pr)}")
    print(f"REFERERS {len(re)}")
