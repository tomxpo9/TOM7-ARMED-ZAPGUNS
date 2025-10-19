#!/usr/bin/env python3
# ...existing code...
try:
    import threading
    import random
    import logging
    import string
    import tkinter as tk
    import time
    import os
    import sys
    from concurrent.futures import ThreadPoolExecutor
    from urllib.parse import urlparse
    from tkinter import ttk, messagebox
    from colorama import Back, Style, Fore, init
    from itertools import cycle
except ModuleNotFoundError as e:
    print(f"Requires Modules {e} Not Installed. Please Run: pip3 install -r requirements.txt")
    exit(1)

# ------------------------Modules Initializations------------------------
init(autoreset=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Utility Functions ---
spinner = cycle(['|', '/', '-', '\\'])

def cleargui():
    os.system('cls' if os.name == 'nt' else 'clear')

def dinamicsgui(startgui):
    cleargui()
    for i in range(50):
        print(f"\r {Fore.YELLOW} {startgui} ... {Fore.LIGHTGREEN_EX}[{Fore.CYAN} {next(spinner)} {Fore.LIGHTGREEN_EX}] {Fore.RESET}", end="", flush=True)
        time.sleep(0.03)
        cleargui()
    time.sleep(0.1)

XBANNER = "TOM7 ARMED - SIMULATION MODE"

# ------------------------Files Configurations------------------------
UA_FILE = "UA.txt"
PROXY_FILE = "Proxies.txt"
REFERER_FILE = "Referers.txt"

DEFAULT_UA = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X)",
    "Mozilla/5.0 (X11; Linux x86_64)"
]

DEFAULT_PROXY = ["http://127.0.0.1:9050"]
DEFAULT_REFERER = ["https://www.google.com"]

def docloader(filename, proxy_list=False):
    try:
        loaded_items = []
        config_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(config_dir, filename)
        if not os.path.exists(config_path):
            if filename == UA_FILE:
                print(f'Error {filename} Not Found. Now Using Default Configuration')
                return DEFAULT_UA
            if filename == PROXY_FILE:
                print(f'Error {filename} Not Found. Now Using Default Configuration')
                return DEFAULT_PROXY
            if filename == REFERER_FILE:
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
                return DEFAULT_UA
            if filename == PROXY_FILE:
                return DEFAULT_PROXY
            if filename == REFERER_FILE:
                return DEFAULT_REFERER
        return loaded_items
    except Exception as e:
        print(f'[ERR] Failed To Load {filename}: {e}')
        if filename == UA_FILE:
            return DEFAULT_UA
        if filename == PROXY_FILE:
            return DEFAULT_PROXY
        if filename == REFERER_FILE:
            return DEFAULT_REFERER
        return []

user_agents = docloader(UA_FILE)
proxies = docloader(PROXY_FILE, proxy_list=True)
treferers = docloader(REFERER_FILE)

# ------------------------RPS Monitor (safe)------------------------
request_count_lock = threading.Lock()
_request_count = 0

def increment_request_count(n=1):
    global _request_count
    with request_count_lock:
        _request_count += int(n)

def start_rps_monitor(interval=1):
    def monitor():
        last_total = 0
        while True:
            time.sleep(interval)
            with request_count_lock:
                current_total = _request_count
            rps = current_total - last_total
            last_total = current_total
            logging.info(f"[RPS] {rps} req/s  (total: {current_total})")
    t = threading.Thread(target=monitor, daemon=True)
    t.start()
    return t

# ------------------------Simulation Helpers------------------------
DRY_RUN = True  # enforced simulation mode (no network activity)

def simulate_request(work=0.01):
    """Simulate doing network work — increment counters and sleep briefly."""
    increment_request_count(1)
    time.sleep(work)

def generate_url_path():
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    return "".join(random.sample(msg, 5))

def evade_waf():
    # lightweight simulated headers
    return {"User-Agent": random.choice(user_agents), "Referer": random.choice(treferers)}

# ------------------------GLOBAL ATTACK METHODS (SIMULATED)------------------------
class AttackMethods:
    @staticmethod
    def http_flood(target, duration, threads, proxy=None, use_tor=False):
        end_time = time.time() + duration
        def attack_worker():
            while time.time() < end_time:
                simulate_request(0.02)
                logging.info(f"[SIM] HTTP Flood -> {target}")
        with ThreadPoolExecutor(max_workers=max(1, threads)) as executor:
            for _ in range(threads):
                executor.submit(attack_worker)

    @staticmethod
    def slowloris(target, duration, sockets=50):
        end_time = time.time() + duration
        url_path = generate_url_path()
        sockets_list = []
        # simulate initial sockets
        for _ in range(sockets):
            sockets_list.append(url_path)
            simulate_request(0.01)
        logging.info(f"[SIM] Slowloris setup {len(sockets_list)} sockets -> {target}")
        while time.time() < end_time:
            for _ in list(sockets_list):
                simulate_request(0.01)
            time.sleep(1)

    @staticmethod
    def massive_payload(target, duration, threads, proxy=None):
        end_time = time.time() + duration
        payload_size = 1024 * 1024  # simulated 1MB
        def attack_worker():
            while time.time() < end_time:
                simulate_request(0.05)
                logging.info(f"[SIM] Massive payload ({payload_size}B simulated) -> {target}")
        with ThreadPoolExecutor(max_workers=max(1, threads)) as executor:
            for _ in range(threads):
                executor.submit(attack_worker)

    @staticmethod
    def rudy(target, duration, threads, proxy=None):
        end_time = time.time() + duration
        def attack_worker():
            while time.time() < end_time:
                simulate_request(0.02)
                logging.info(f"[SIM] RUDY simulated POST -> {target}")
                time.sleep(random.uniform(0.05, 0.2))
        with ThreadPoolExecutor(max_workers=max(1, threads)) as executor:
            for _ in range(threads):
                executor.submit(attack_worker)

    @staticmethod
    def xmlrpc_flood(target, duration, threads, proxy=None):
        end_time = time.time() + duration
        def attack_worker():
            while time.time() < end_time:
                simulate_request(0.03)
                logging.info(f"[SIM] XML-RPC simulated POST -> {target}/xmlrpc.php")
        with ThreadPoolExecutor(max_workers=max(1, threads)) as executor:
            for _ in range(threads):
                executor.submit(attack_worker)

# ------------------------GUI (unchanged behavior)------------------------
class TOM7ARMEDGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TOM7 ARMED | ZAP GUNS (SIM)")
        self.target_var = tk.StringVar()
        self.duration_var = tk.StringVar(value="10")
        self.threads_var = tk.StringVar(value="1")
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
        ttk.Checkbutton(root, text="TOR Proxies (simulated)", variable=self.tor_var).grid(row=4, column=0, columnspan=5, pady=8)
        ttk.Button(root, text="Start (SIM)", command=self.start_attack).grid(row=5, column=0, columnspan=5, pady=15)

    def start_attack(self):
        target = self.target_var.get()
        try:
            duration = int(self.duration_var.get())
            threads = int(self.threads_var.get())
        except ValueError:
            messagebox.showerror("Error","Duration and Threads must be integers")
            return
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

        messagebox.showinfo("Started", f"Simulation Launched To {target} Using {method}")

# ------------------------MAIN ROOT------------------------
if __name__ == "__main__":
    cleargui()
    dinamicsgui(f"Loading User Agents")
    dinamicsgui(f"Loading Proxies")
    dinamicsgui(f"Loading Referers")
    time.sleep(0.5)
    cleargui()
    print(f"{Fore.RED}{XBANNER}{Fore.RESET}")
    print(f"USER AGENTS: {len(user_agents)}  PROXIES: {len(proxies)}  REFERERS: {len(treferers)}")
    start_rps_monitor(interval=1)
    root = tk.Tk()
    gui = TOM7ARMEDGUI(root)
    root.mainloop()
    cleargui()
    print("SIMULATION END")
# ...existing code...