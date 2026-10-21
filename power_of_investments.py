import tkinter as tk
from tkinter import ttk
import json
import os
import queue
import random
import re
import threading
import urllib.error
import urllib.request

API_URL = "https://power-of-investments.minecraftmobileexplorer.workers.dev"
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".power_of_investments.json")
SAVE_PATH = os.path.join(os.path.expanduser("~"), ".power_of_investments_save.json")
AUTOSAVE_SEC = 5
LOGO_B64 = (
    "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"
)
USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,16}$")

GOAL = 1_000_000
TURN_MS = 3000
TICK_MS = 50
HISTORY = 60
MIN_INTERVAL = 0.2
SPEEDUP = 0.9
COMP_QTYS = ("1", "10", "100", "Max")

NEWS = [
    ("Market rally! Investors are bullish.", 4.0),
    ("Strong earnings reports lift prices.", 3.0),
    ("Tech boom drives the market up.", 5.0),
    ("Rumors of a recession shake confidence.", -4.0),
    ("Supply chain trouble hits stocks.", -3.0),
    ("Flash crash! Prices tumble.", -6.0),
]


class InvestmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Power of Investments")
        try:
            self.logo_img = tk.PhotoImage(data=LOGO_B64)
            self.root.iconphoto(True, self.logo_img)
        except tk.TclError:
            pass
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.toggle_fullscreen)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<space>", self.toggle_pause)

        self.bg = "#f4ecd8"
        self.fg = "#3b2e2a"
        self.accent = "#d9c3a9"
        self.bar = "#8b5a2b"
        self.up = "#2e7d32"
        self.down = "#b23a2e"
        self.font = "Courier New"
        self.root.configure(bg=self.bg)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Horizontal.TProgressbar", background=self.bar,
                             troughcolor=self.accent, bordercolor=self.fg)

        self.container = tk.Frame(root, bg=self.bg)
        self.container.pack(fill="both", expand=True)

        self.timer_id = None
        self.in_game = False
        self.paused = False
        self.won = False
        self.view_id = 0
        self.save_timer = 0.0
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.api_queue = queue.Queue()
        self.cfg = self.load_cfg()
        self.root.after(100, self.poll_api)
        self.show_main_menu()

    def toggle_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def clear(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.in_game = False
        self.view_id += 1
        for w in self.container.winfo_children():
            w.destroy()

    def button(self, parent, text, command, width=20, size=12):
        b = tk.Button(parent, text=text, command=command, bg=self.accent, fg=self.fg,
                      activebackground=self.bar, activeforeground=self.bg,
                      font=(self.font, size, "bold"), relief="groove", width=width, cursor="hand2")
        return b

    def label(self, parent, text="", size=12, bold=True, **kw):
        kw.setdefault("fg", self.fg)
        return tk.Label(parent, text=text, bg=self.bg,
                        font=(self.font, size, "bold" if bold else "normal"), **kw)

    def centered(self):
        outer = tk.Frame(self.container, bg=self.bg)
        outer.pack(fill="both", expand=True)
        inner = tk.Frame(outer, bg=self.bg)
        inner.place(relx=0.5, rely=0.5, anchor="center")
        return inner

    def show_main_menu(self):
        if not self.cfg.get("username"):
            self.show_username_screen()
            return
        self.clear()
        f = self.centered()
        self.label(f, "POWER OF INVESTMENTS", 26).pack(pady=(0, 6))
        self.label(f, f"Reach ${GOAL:,} net worth to win", 11, False).pack(pady=(0, 4))
        self.label(f, f"Playing as: {self.cfg['username']}", 11, False).pack(pady=(0, 20))
        self.label(f, "Select Difficulty:", 12).pack(pady=6)

        if not hasattr(self, "difficulty_var"):
            self.difficulty_var = tk.StringVar(value="Normal")
        row = tk.Frame(f, bg=self.bg)
        row.pack(pady=6)
        for d in ("Easy", "Normal", "Hard"):
            tk.Radiobutton(row, text=d, variable=self.difficulty_var, value=d, bg=self.bg,
                           fg=self.fg, selectcolor=self.accent, activebackground=self.bg,
                           font=(self.font, 11, "bold")).pack(side="left", padx=15)

        bf = tk.Frame(f, bg=self.bg)
        bf.pack(pady=24)
        saved = self.load_save()
        if saved:
            self.button(bf, f"CONTINUE ({saved['difficulty']}, turn {saved['turn']})",
                        self.continue_game, width=28).pack(pady=7, ipady=5)
        self.button(bf, "NEW GAME", lambda: self.start_game(self.difficulty_var.get())).pack(pady=7, ipady=5)
        self.button(bf, "LEADERBOARD", lambda: self.show_leaderboard(self.difficulty_var.get())).pack(pady=7, ipady=5)
        self.button(bf, "HOW TO PLAY", self.show_help).pack(pady=7, ipady=5)
        self.button(bf, "CREDITS", self.show_credits).pack(pady=7, ipady=5)
        self.button(bf, "QUIT", self.quit_app).pack(pady=7, ipady=5)
        self.label(f, "ESC / F11: fullscreen   SPACE: pause", 9, False).pack(pady=10)

    def show_text_page(self, title, body):
        self.clear()
        f = self.centered()
        self.label(f, title, 22).pack(pady=20)
        tk.Label(f, text=body, bg=self.bg, fg=self.fg, font=(self.font, 12),
                 justify="left").pack(pady=10)
        self.button(f, "BACK", self.show_main_menu).pack(pady=20, ipady=4)

    def load_cfg(self):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError):
            return {}

    def save_cfg(self):
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as fh:
                json.dump(self.cfg, fh)
        except OSError:
            pass

    def api(self, method, path, body, callback):
        if not API_URL:
            callback(False, {"error": "Online leaderboard is not set up (API_URL is empty)."})
            return
        view = self.view_id

        def work():
            try:
                data = json.dumps(body).encode() if body is not None else None
                req = urllib.request.Request(API_URL + path, data=data, method=method,
                                             headers={"Content-Type": "application/json",
                                                      "User-Agent": "PowerOfInvestments/1.0"})
                with urllib.request.urlopen(req, timeout=10) as r:
                    res = (True, json.loads(r.read().decode()))
            except urllib.error.HTTPError as e:
                try:
                    res = (False, json.loads(e.read().decode()))
                except ValueError:
                    res = (False, {"error": f"Server error {e.code}"})
            except Exception:
                res = (False, {"error": "Could not reach the server. Check your internet."})
            self.api_queue.put((view, callback, res))

        threading.Thread(target=work, daemon=True).start()

    def poll_api(self):
        try:
            while True:
                view, callback, (ok, data) = self.api_queue.get_nowait()
                if callback and (view == self.view_id or getattr(callback, "always", False)):
                    callback(ok, data)
        except queue.Empty:
            pass
        self.root.after(100, self.poll_api)

    def show_username_screen(self, message=""):
        self.clear()
        f = self.centered()
        self.label(f, "CHOOSE A USERNAME", 22).pack(pady=(0, 10))
        self.label(f, "3-16 letters, numbers or underscores.\nThis is your name on the leaderboard.", 11, False).pack(pady=6)
        var = tk.StringVar()
        entry = tk.Entry(f, textvariable=var, font=(self.font, 14, "bold"), justify="center",
                         bg=self.accent, fg=self.fg, insertbackground=self.fg, relief="groove", width=22)
        entry.pack(pady=14, ipady=4)
        entry.focus_set()
        msg = self.label(f, message, 10, fg=self.down)
        msg.pack(pady=4)

        def submit(event=None):
            name = var.get().strip()
            if not USERNAME_RE.match(name):
                msg.config(text="Use 3-16 letters, numbers or underscores.")
                return
            if not API_URL:
                self.cfg["username"] = name
                self.save_cfg()
                self.show_main_menu()
                return
            msg.config(text="Checking name...", fg=self.fg)
            btn.config(state="disabled")

            def done(ok, data):
                if ok:
                    self.cfg["username"] = name
                    self.cfg["token"] = data.get("token", "")
                    self.save_cfg()
                    self.show_main_menu()
                else:
                    btn.config(state="normal")
                    msg.config(text=data.get("error", "Could not register."), fg=self.down)
            self.api("POST", "/register", {"username": name}, done)

        btn = self.button(f, "CONTINUE", submit)
        btn.pack(pady=10, ipady=4)
        entry.bind("<Return>", submit)

    def show_leaderboard(self, difficulty="Normal"):
        self.clear()
        f = self.centered()
        self.label(f, "LEADERBOARD", 22).pack(pady=(0, 4))
        self.label(f, "Fastest wins (fewest turns to reach the goal)", 10, False).pack(pady=(0, 10))
        row = tk.Frame(f, bg=self.bg)
        row.pack(pady=6)
        for d in ("Easy", "Normal", "Hard"):
            b = self.button(row, d.upper(), lambda dd=d: self.show_leaderboard(dd), width=10, size=10)
            if d == difficulty:
                b.config(bg=self.bar, fg=self.bg)
            b.pack(side="left", padx=4)
        body = tk.Label(f, text="Loading...", bg=self.bg, fg=self.fg, font=(self.font, 12), justify="left")
        body.pack(pady=12)
        self.button(f, "BACK", self.show_main_menu).pack(pady=10, ipady=4)

        def done(ok, data):
            if not ok:
                body.config(text=data.get("error", "Could not load leaderboard."))
                return
            rows = data.get("scores", [])
            if not rows:
                body.config(text=f"No {difficulty} scores yet. Be the first!")
                return
            me = (self.cfg.get("username") or "").lower()
            lines = [f"{'#':>3}  {'PLAYER':<16}  {'TURNS':>6}"]
            for i, r in enumerate(rows, 1):
                mark = " <" if r["username"].lower() == me else ""
                lines.append(f"{i:>3}  {r['username']:<16}  {r['turns']:>6}{mark}")
            body.config(text="\n".join(lines))
        self.api("GET", f"/leaderboard?difficulty={difficulty}", None, done)

    def submit_score(self, status_label):
        status_label.config(text="Submitting score...")

        def done(ok, data):
            if ok:
                status_label.config(text="Score submitted to the leaderboard!")
            else:
                status_label.config(text=data.get("error", "Could not submit score."))
        done.always = False
        self.api("POST", "/score", {"username": self.cfg.get("username", ""),
                                    "token": self.cfg.get("token", ""),
                                    "difficulty": self.difficulty,
                                    "turns": self.turn}, done)

    def show_credits(self):
        self.show_text_page("CREDITS",
                            "Power of Investments\n\nLead Developer: You!\n"
                            "Theme: Vintage Retro Terminal\n\nThanks for playing!")

    def show_help(self):
        self.show_text_page("HOW TO PLAY",
                            "- Prices change every few seconds.\n"
                            "- Buy low, sell high in the STOCKS tab.\n"
                            "- Each company in the COMPANIES tab has its\n"
                            "  own timer and payout. Upgrades raise income\n"
                            "  and shorten the timer until MAX SPEED.\n"
                            "- Upgrade 1x / 10x / 100x / Max at a time.\n"
                            "- The bottom bar is the stock market timer.\n"
                            "- News events can move the market.\n"
                            f"- Reach ${GOAL:,} net worth to win!\n\n"
                            "Keys: SPACE pause, ESC/F11 fullscreen")

    def _save_key(self):
        return (self.cfg.get("username") or "player").lower()

    def _read_saves(self):
        try:
            with open(SAVE_PATH, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            return data if isinstance(data, dict) else {}
        except (OSError, ValueError):
            return {}

    def load_save(self):
        s = self._read_saves().get(self._save_key())
        needed = ("difficulty", "cash", "stock", "shares", "total_cost", "turn", "history", "levels")
        if isinstance(s, dict) and all(k in s for k in needed):
            return s
        return None

    def save_game(self, announce=False):
        if not self.in_game or self.won:
            return
        state = {
            "difficulty": self.difficulty, "cash": self.cash, "stock": self.stock,
            "shares": self.shares, "total_cost": self.total_cost, "turn": self.turn,
            "history": self.history, "news_text": self.news_text, "news_bias": self.news_bias,
            "news_turns": self.news_turns, "elapsed": self.elapsed,
            "levels": [c[3] for c in self.companies], "comp_elapsed": self.comp_elapsed,
        }
        saves = self._read_saves()
        saves[self._save_key()] = state
        try:
            with open(SAVE_PATH, "w", encoding="utf-8") as fh:
                json.dump(saves, fh)
            if announce:
                self.say("Game saved.")
        except OSError:
            if announce:
                self.say("Could not write the save file.")

    def delete_save(self):
        saves = self._read_saves()
        if saves.pop(self._save_key(), None) is not None:
            try:
                with open(SAVE_PATH, "w", encoding="utf-8") as fh:
                    json.dump(saves, fh)
            except OSError:
                pass

    def continue_game(self):
        s = self.load_save()
        if s:
            self.start_game(s["difficulty"], state=s)

    def apply_state(self, s):
        self.cash, self.stock = float(s["cash"]), float(s["stock"])
        self.shares, self.total_cost, self.turn = int(s["shares"]), float(s["total_cost"]), int(s["turn"])
        self.history = [float(x) for x in s["history"]][-HISTORY:] or [self.stock]
        self.news_text = s.get("news_text", "Welcome back!")
        self.news_bias = float(s.get("news_bias", 0.0))
        self.news_turns = int(s.get("news_turns", 0))
        self.elapsed = int(s.get("elapsed", 0))
        for c, lvl in zip(self.companies, s["levels"]):
            c[3] = int(lvl)
        for i, e in enumerate(s.get("comp_elapsed", [])[:len(self.companies)]):
            self.comp_elapsed[i] = float(e)

    def quit_app(self):
        self.save_game()
        self.root.destroy()

    def start_game(self, difficulty, state=None):
        self.clear()
        self.in_game = True
        self.paused = False
        self.won = False
        self.difficulty = difficulty
        settings = {"Easy": (2000.0, 5.0), "Normal": (1000.0, 8.0), "Hard": (500.0, 15.0)}
        self.cash, self.volatility = settings[difficulty]
        self.stock = 100.0
        self.shares = 0
        self.total_cost = 0.0
        self.income = 0
        self.turn = 0
        self.history = [100.0]
        self.qty_var = tk.StringVar(value="1")
        self.news_text = "Welcome to the market!"
        self.news_bias = 0.0
        self.news_turns = 0

        self.companies = [
            ["Lemonade Stand", 100, 10, 0, 2],
            ["Paper Route", 300, 35, 0, 3],
            ["Car Wash", 750, 90, 0, 4],
            ["Coffee Shop", 1500, 200, 0, 5],
            ["Bookstore", 3500, 500, 0, 6],
            ["Fitness Gym", 8000, 1200, 0, 8],
            ["Tech Startup", 20000, 3200, 0, 10],
            ["Real Estate Firm", 50000, 8500, 0, 12],
            ["Crypto Miner", 120000, 22000, 0, 15],
            ["Global Conglomerate", 300000, 60000, 0, 20],
        ]
        self.comp_elapsed = [0.0] * len(self.companies)
        self.comp_qty_var = tk.StringVar(value="1")

        root_f = tk.Frame(self.container, bg=self.bg)
        root_f.pack(fill="both", expand=True)
        root_f.rowconfigure(1, weight=1)
        root_f.columnconfigure(0, weight=1)

        top = tk.Frame(root_f, bg=self.fg)
        top.grid(row=0, column=0, sticky="ew")
        self.top_lbl = tk.Label(top, bg=self.fg, fg=self.bg, font=(self.font, 12, "bold"), anchor="w")
        self.top_lbl.pack(side="left", padx=12, pady=6)
        self.button(top, "PAUSE", self.toggle_pause, width=9, size=10).pack(side="right", padx=6, pady=4)
        self.button(top, "MENU", self.confirm_menu, width=9, size=10).pack(side="right", padx=6, pady=4)
        self.button(top, "SAVE", lambda: self.save_game(announce=True), width=9, size=10).pack(side="right", padx=6, pady=4)

        nb = ttk.Notebook(root_f)
        nb.grid(row=1, column=0, sticky="nsew", padx=10, pady=8)
        self.tab_stocks = tk.Frame(nb, bg=self.bg)
        self.tab_comp = tk.Frame(nb, bg=self.bg)
        nb.add(self.tab_stocks, text="[ STOCKS ]")
        nb.add(self.tab_comp, text="[ COMPANIES ]")

        self.build_stocks_tab()
        self.build_companies_tab()

        bottom = tk.Frame(root_f, bg=self.bg)
        bottom.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 10))
        bottom.columnconfigure(0, weight=1)
        self.status_lbl = self.label(bottom, "", 10, anchor="w")
        self.status_lbl.grid(row=0, column=0, sticky="ew")
        self.news_lbl = self.label(bottom, "", 10, False, anchor="w")
        self.news_lbl.grid(row=1, column=0, sticky="ew")
        self.progress = ttk.Progressbar(bottom, orient="horizontal", mode="determinate", maximum=100)
        self.progress.grid(row=2, column=0, sticky="ew", pady=(6, 0))
        self.elapsed = 0
        self.save_timer = 0.0
        if state:
            self.apply_state(state)
            self.say("Save loaded. Welcome back!")

        self.update_display()
        self.timer_id = self.root.after(TICK_MS, self.tick)

    def build_stocks_tab(self):
        t = self.tab_stocks
        t.rowconfigure(0, weight=1)
        t.columnconfigure(0, weight=1)

        chart_wrap = tk.Frame(t, bg=self.fg, bd=2)
        chart_wrap.grid(row=0, column=0, sticky="nsew", padx=(12, 12), pady=12)
        self.chart = tk.Canvas(chart_wrap, bg=self.bg, highlightthickness=0)
        self.chart.pack(fill="both", expand=True, padx=2, pady=2)
        self.chart.bind("<Configure>", lambda e: self.draw_chart())

        side = tk.Frame(t, bg=self.bg)
        side.grid(row=0, column=1, sticky="ns", padx=(0, 12), pady=12)
        self.stats_lbl = tk.Label(side, bg=self.bg, fg=self.fg, font=(self.font, 12, "bold"), justify="left")
        self.stats_lbl.pack(anchor="nw", pady=(0, 12))

        self.label(side, "Quantity:", 11).pack(anchor="w")
        qrow = tk.Frame(side, bg=self.bg)
        qrow.pack(anchor="w", pady=4)
        for q in ("1", "10", "100", "Max"):
            tk.Radiobutton(qrow, text=q, variable=self.qty_var, value=q, indicatoron=False,
                           bg=self.accent, fg=self.fg, selectcolor=self.bar, width=5,
                           font=(self.font, 10, "bold"), relief="groove").pack(side="left", padx=2)

        self.button(side, "BUY", self.buy, width=18, size=11).pack(anchor="w", pady=(14, 6), ipady=3)
        self.button(side, "SELL", self.sell, width=18, size=11).pack(anchor="w", pady=6, ipady=3)
        self.button(side, "SELL ALL", self.sell_all, width=18, size=11).pack(anchor="w", pady=6, ipady=3)

    def build_companies_tab(self):
        qbar = tk.Frame(self.tab_comp, bg=self.bg)
        qbar.pack(fill="x", padx=15, pady=(10, 0))
        self.label(qbar, "Upgrade amount:", 11).pack(side="left", padx=(0, 8))
        for q in COMP_QTYS:
            tk.Radiobutton(qbar, text=f"{q}x" if q != "Max" else "Max", variable=self.comp_qty_var,
                           value=q, indicatoron=False, bg=self.accent, fg=self.fg,
                           selectcolor=self.bar, width=6, font=(self.font, 10, "bold"),
                           relief="groove", command=self.update_display).pack(side="left", padx=2)
        wrap = tk.Frame(self.tab_comp, bg=self.bg)
        wrap.pack(fill="both", expand=True)
        canvas = tk.Canvas(wrap, bg=self.bg, highlightthickness=0)
        sb = ttk.Scrollbar(wrap, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg=self.bg, padx=15, pady=15)
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        win = canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        def on_wheel(e):
            canvas.yview_scroll(-1 if (e.num == 4 or e.delta > 0) else 1, "units")
        canvas.bind_all("<MouseWheel>", on_wheel)
        canvas.bind_all("<Button-4>", on_wheel)
        canvas.bind_all("<Button-5>", on_wheel)

        self.comp_btns = []
        self.comp_bars = []
        self.comp_info = []
        for i in range(len(self.companies)):
            row = tk.Frame(frame, bg=self.bg, highlightbackground=self.fg, highlightthickness=1)
            row.pack(pady=5, fill="x")
            row.columnconfigure(1, weight=1)
            b = tk.Button(row, command=lambda idx=i: self.upgrade(idx), bg=self.accent,
                          fg=self.fg, font=(self.font, 10, "bold"), relief="groove",
                          justify="left", anchor="w", cursor="hand2", width=34)
            b.grid(row=0, column=0, sticky="ns", padx=6, pady=6, ipady=4)
            right = tk.Frame(row, bg=self.bg)
            right.grid(row=0, column=1, sticky="ew", padx=10, pady=6)
            right.columnconfigure(0, weight=1)
            info = tk.Label(right, bg=self.bg, fg=self.fg, font=(self.font, 10, "bold"),
                            justify="left", anchor="w")
            info.grid(row=0, column=0, sticky="ew")
            bar = ttk.Progressbar(right, orient="horizontal", mode="determinate", maximum=100)
            bar.grid(row=1, column=0, sticky="ew", pady=(4, 0))
            self.comp_btns.append(b)
            self.comp_info.append(info)
            self.comp_bars.append(bar)

    def say(self, msg):
        self.status_lbl.config(text=msg)

    def qty(self):
        q = self.qty_var.get()
        if q == "Max":
            return int(self.cash // self.stock)
        return int(q)

    def buy(self):
        if self.paused or self.won:
            return
        n = self.qty()
        if n <= 0 or self.cash < self.stock * n:
            n = int(self.cash // self.stock) if self.qty_var.get() != "Max" else n
            if n <= 0:
                self.say("Not enough cash to buy.")
                return
            self.say(f"Not enough cash for requested amount; bought {n} instead.")
        cost = self.stock * n
        self.cash -= cost
        self.total_cost += cost
        self.shares += n
        if self.status_lbl.cget("text").startswith("Not enough cash for"):
            pass
        else:
            self.say(f"Bought {n} share(s) at ${self.stock:,.2f}.")
        self.update_display()

    def sell(self):
        if self.paused or self.won:
            return
        n = self.shares if self.qty_var.get() == "Max" else min(self.qty(), self.shares)
        self.do_sell(n)

    def sell_all(self):
        if self.paused or self.won:
            return
        self.do_sell(self.shares)

    def do_sell(self, n):
        if n <= 0:
            self.say("No shares to sell.")
            return
        avg = self.total_cost / self.shares
        proceeds = self.stock * n
        profit = proceeds - avg * n
        self.cash += proceeds
        self.shares -= n
        self.total_cost = 0.0 if self.shares == 0 else self.total_cost - avg * n
        self.say(f"Sold {n} share(s) for ${proceeds:,.2f} ({'+' if profit >= 0 else '-'}${abs(profit):,.2f}).")
        self.update_display()

    def upgrade(self, i):
        if self.paused or self.won:
            return
        name, base, boost, lvl, _ = self.companies[i]
        n = self.comp_upgrade_count(i)
        if n <= 0:
            need = self.comp_cost(i, 1)
            self.say(f"Need ${need - self.cash:,.0f} more for {name}.")
            return
        cost = self.comp_cost(i, n)
        if self.cash < cost:
            self.say(f"Need ${cost - self.cash:,.0f} more for {n} level(s) of {name}.")
            return
        self.cash -= cost
        if lvl == 0:
            self.comp_elapsed[i] = 0.0
        self.companies[i][3] += n
        self.say(f"Upgraded {name} by {n} to level {lvl + n}.")
        self.update_display(redraw_chart=False)

    def comp_cost(self, i, n):
        base, lvl = self.companies[i][1], self.companies[i][3]
        return int(base * (1.5 ** lvl) * ((1.5 ** n) - 1) / 0.5)

    def comp_upgrade_count(self, i):
        q = self.comp_qty_var.get()
        if q == "Max":
            n = 0
            while n < 1000 and self.comp_cost(i, n + 1) <= self.cash:
                n += 1
            return n
        n = int(q)
        return n if self.comp_cost(i, n) <= self.cash else 0

    def comp_interval_for(self, i, lvl=None):
        base = self.companies[i][4]
        lvl = self.companies[i][3] if lvl is None else lvl
        if lvl <= 0:
            return None
        return max(MIN_INTERVAL, base * (SPEEDUP ** (lvl - 1)))

    def income_per_sec(self):
        total = 0.0
        for i, c in enumerate(self.companies):
            iv = self.comp_interval_for(i)
            if iv:
                total += c[2] * c[3] / iv
        return total

    def toggle_pause(self, event=None):
        if not self.in_game or self.won:
            return
        self.paused = not self.paused
        self.say("PAUSED - press SPACE to resume." if self.paused else "Resumed.")

    def confirm_menu(self):
        self.save_game()
        self.show_main_menu()

    def net_worth(self):
        return self.cash + self.shares * self.stock

    def update_display(self, redraw_chart=True):
        avg = self.total_cost / self.shares if self.shares else 0.0
        nw = self.net_worth()
        ips = self.income_per_sec()
        self.top_lbl.config(text=f"[{self.difficulty}]  Turn {self.turn}   Cash ${self.cash:,.2f}   "
                                 f"Income ${ips:,.2f}/sec   Net Worth ${nw:,.2f} / ${GOAL:,}")
        pl = (self.stock - avg) * self.shares if self.shares else 0.0
        self.stats_lbl.config(
            text=f"=== PORTFOLIO ===\nCash:    ${self.cash:,.2f}\nIncome:  ${ips:,.2f}/sec\n"
                 f"Net:     ${nw:,.2f}\n\n=== MARKET ===\nPrice:   ${self.stock:,.2f}\n"
                 f"Owned:   {self.shares}\nAvg buy: ${avg:,.2f}\n"
                 f"P/L:     {'+' if pl >= 0 else '-'}${abs(pl):,.2f}")
        self.news_lbl.config(text=f"NEWS: {self.news_text}")
        for i, (name, base, boost, lvl, _) in enumerate(self.companies):
            n = self.comp_upgrade_count(i)
            shown = max(1, n) if self.comp_qty_var.get() == "Max" else int(self.comp_qty_var.get())
            cost = self.comp_cost(i, shown)
            self.comp_btns[i].config(
                text=f"{name}  (Lvl {lvl})\nUpgrade x{shown}: ${cost:,}",
                fg=self.fg if n > 0 else "#8a7a70")

            iv = self.comp_interval_for(i)
            next_iv = self.comp_interval_for(i, lvl + shown)
            next_inc = boost * (lvl + shown)
            if iv is None:
                info = (f"Not owned yet\n"
                        f"After upgrade: ${next_inc:,}/payout every {next_iv:.2f}s")
            else:
                speed = "MAX SPEED" if iv <= MIN_INTERVAL else f"{iv:.2f}s"
                nspeed = "MAX SPEED" if next_iv <= MIN_INTERVAL else f"{next_iv:.2f}s"
                info = (f"Income: ${boost * lvl:,}/payout   Timer: {speed}   "
                        f"= ${boost * lvl / iv:,.2f}/sec\n"
                        f"After upgrade: ${next_inc:,}/payout, timer {nspeed}")
            self.comp_info[i].config(text=info)
        if redraw_chart:
            self.draw_chart()

    def draw_chart(self):
        if not self.in_game or not hasattr(self, "chart"):
            return
        c = self.chart
        c.delete("all")
        w, h = c.winfo_width(), c.winfo_height()
        if w < 50 or h < 50:
            return
        pl, pr, pt, pb = 60, 100, 20, 25
        data = self.history
        lo, hi = min(data), max(data)
        pad = max((hi - lo) * 0.1, 1.0)
        lo, hi = max(0, lo - pad), hi + pad
        span = hi - lo

        for k in range(5):
            y = pt + (h - pt - pb) * k / 4
            c.create_line(pl, y, w - pr, y, fill=self.accent)
            c.create_text(pl - 6, y, text=f"${hi - span * k / 4:,.0f}", anchor="e",
                          fill=self.fg, font=(self.font, 8))

        slots = max(10, len(data) - 1)

        def px(i):
            return pl + (w - pl - pr) * (i / slots)

        def py(v):
            return pt + (h - pt - pb) * (1 - (v - lo) / span)

        pts = []
        for i, v in enumerate(data):
            pts += [px(i), py(v)]
        color = self.up if len(data) < 2 or data[-1] >= data[-2] else self.down
        if len(pts) >= 4:
            c.create_line(*pts, fill=color, width=3, smooth=False)
        for i in range(0, len(pts), 2):
            c.create_oval(pts[i] - 3, pts[i + 1] - 3, pts[i] + 3, pts[i + 1] + 3,
                          fill=self.bar, outline=self.fg)
        c.create_text(pts[-2] + 8, max(pt + 8, pts[-1] - 16), text=f"${data[-1]:,.2f}", anchor="w",
                      fill=color, font=(self.font, 10, "bold"))

    def tick(self):
        if not self.in_game:
            return
        if not self.paused and not self.won:
            self.elapsed += TICK_MS
            if self.elapsed >= TURN_MS:
                self.elapsed = 0
                self.next_turn()
            self.progress["value"] = self.elapsed / TURN_MS * 100
            if not self.won:
                self.tick_companies()
            self.save_timer += TICK_MS / 1000.0
            if self.save_timer >= AUTOSAVE_SEC and not self.won:
                self.save_timer = 0.0
                self.save_game()
        self.timer_id = self.root.after(TICK_MS, self.tick)

    def tick_companies(self):
        paid = False
        for i, c in enumerate(self.companies):
            iv = self.comp_interval_for(i)
            if iv is None:
                self.comp_bars[i]["value"] = 0
                continue
            self.comp_elapsed[i] += TICK_MS / 1000.0
            if self.comp_elapsed[i] >= iv:
                payouts = int(self.comp_elapsed[i] // iv)
                self.comp_elapsed[i] -= payouts * iv
                self.cash += c[2] * c[3] * payouts
                paid = True
            self.comp_bars[i]["value"] = min(100, self.comp_elapsed[i] / iv * 100)
        if paid:
            if self.net_worth() >= GOAL:
                self.win()
                return
            self.update_display(redraw_chart=False)

    def next_turn(self):
        self.turn += 1

        if self.news_turns > 0:
            self.news_turns -= 1
            if self.news_turns == 0:
                self.news_bias = 0.0
                self.news_text = "Markets are calm."
        elif random.random() < 0.12:
            self.news_text, self.news_bias = random.choice(NEWS)
            self.news_turns = 3

        change = random.uniform(-self.volatility, self.volatility) + self.news_bias
        self.stock = max(1.0, self.stock + change)
        self.history.append(self.stock)
        if len(self.history) > HISTORY:
            self.history.pop(0)

        if self.net_worth() >= GOAL:
            self.win()
            return
        self.update_display()

    def win(self):
        self.won = True
        self.delete_save()
        self.update_display()
        overlay = tk.Frame(self.container, bg=self.bg, highlightbackground=self.fg, highlightthickness=3)
        overlay.place(relx=0.5, rely=0.5, anchor="center")
        inner = tk.Frame(overlay, bg=self.bg, padx=40, pady=30)
        inner.pack()
        self.label(inner, "YOU WIN!", 28, fg=self.up).pack(pady=8)
        self.label(inner, f"Net worth ${self.net_worth():,.2f}\nTurns: {self.turn}", 13).pack(pady=8)
        status = self.label(inner, "", 10)
        status.pack(pady=4)
        self.submit_score(status)
        self.button(inner, "LEADERBOARD", lambda: self.show_leaderboard(self.difficulty)).pack(pady=6, ipady=4)
        self.button(inner, "PLAY AGAIN", lambda: self.start_game(self.difficulty)).pack(pady=6, ipady=4)
        self.button(inner, "MAIN MENU", self.show_main_menu).pack(pady=6, ipady=4)


if __name__ == "__main__":
    root = tk.Tk()
    app = InvestmentApp(root)
    root.mainloop()
