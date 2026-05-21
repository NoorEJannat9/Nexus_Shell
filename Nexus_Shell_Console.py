import subprocess
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox, filedialog
import requests
import time
import webbrowser
import threading
import os
import json
import platform
import psutil
from datetime import datetime


from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = os.getenv("CITY", "Dhaka")
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

HISTORY_FILE = os.path.expanduser("~/.shell_console_history.json")


BG_DEEP    = "#0a0a0f"
BG_PANEL   = "#0f0f1a"
BG_CARD    = "#13131f"
BG_INPUT   = "#1a1a2e"
ACCENT1    = "#00d4ff"   
ACCENT2    = "#7b2fff"   
ACCENT3    = "#ff2d78"   
SUCCESS    = "#00ff9d"
WARNING    = "#ffb700"
ERROR      = "#ff4757"
TEXT_PRI   = "#e8e8f0"
TEXT_SEC   = "#7a7a9d"
BORDER     = "#2a2a3e"

FONT_MONO  = ("Consolas", 10)
FONT_MONO_SM = ("Consolas", 9)
FONT_HEAD  = ("Segoe UI", 11, "bold")
FONT_LABEL = ("Segoe UI", 9)
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_SMALL = ("Segoe UI", 8)


command_explanations = {
    "File Management": {
        "ls":    {"explanation": "Lists files and directories in the current directory.", "example": "ls -la", "flags": "-l (long), -a (hidden), -h (human sizes)"},
        "pwd":   {"explanation": "Prints the current working directory path.", "example": "pwd", "flags": ""},
        "cd":    {"explanation": "Changes the current directory.", "example": "cd /home/user", "flags": ""},
        "mkdir": {"explanation": "Creates a new directory.", "example": "mkdir -p path/to/dir", "flags": "-p (parents), -v (verbose)"},
        "rmdir": {"explanation": "Removes an empty directory.", "example": "rmdir mydir", "flags": ""},
        "rm":    {"explanation": "Removes files or directories.", "example": "rm -rf mydir", "flags": "-r (recursive), -f (force), -i (interactive)"},
        "cp":    {"explanation": "Copies files or directories.", "example": "cp -r src/ dest/", "flags": "-r (recursive), -p (preserve), -v (verbose)"},
        "mv":    {"explanation": "Moves or renames files or directories.", "example": "mv old.txt new.txt", "flags": "-i (interactive), -v (verbose)"},
        "touch": {"explanation": "Creates an empty file or updates timestamps.", "example": "touch newfile.txt", "flags": ""},
        "cat":   {"explanation": "Concatenates and displays file content.", "example": "cat file.txt", "flags": "-n (line numbers), -A (show all)"},
        "echo":  {"explanation": "Displays a line of text or variable value.", "example": "echo $HOME", "flags": "-n (no newline), -e (interpret escapes)"},
        "find":  {"explanation": "Searches for files in a directory hierarchy.", "example": "find . -name '*.py'", "flags": "-name, -type, -mtime, -size"},
        "ln":    {"explanation": "Creates hard or symbolic links.", "example": "ln -s target link", "flags": "-s (symbolic), -f (force)"},
        "stat":  {"explanation": "Display file or filesystem status.", "example": "stat file.txt", "flags": ""},
        "file":  {"explanation": "Determine file type.", "example": "file unknown.bin", "flags": ""},
        "wc":    {"explanation": "Counts lines, words, and characters in a file.", "example": "wc -l file.txt", "flags": "-l (lines), -w (words), -c (bytes)"},
    },
    "Text Processing": {
        "grep":  {"explanation": "Searches for patterns in files.", "example": "grep -rn 'error' logs/", "flags": "-r (recursive), -n (line numbers), -i (case insensitive)"},
        "sed":   {"explanation": "Stream editor for filtering and transforming text.", "example": "sed 's/old/new/g' file.txt", "flags": "-i (in-place), -n (quiet)"},
        "awk":   {"explanation": "Pattern scanning and text processing language.", "example": "awk '{print $1}' file.txt", "flags": "-F (field separator)"},
        "sort":  {"explanation": "Sorts lines in text files.", "example": "sort -n numbers.txt", "flags": "-n (numeric), -r (reverse), -u (unique)"},
        "uniq":  {"explanation": "Reports or filters out repeated lines.", "example": "sort file | uniq -c", "flags": "-c (count), -d (duplicates only)"},
        "cut":   {"explanation": "Removes sections from each line of files.", "example": "cut -d',' -f1 file.csv", "flags": "-d (delimiter), -f (fields)"},
        "tr":    {"explanation": "Translates or deletes characters.", "example": "echo 'hello' | tr 'a-z' 'A-Z'", "flags": "-d (delete), -s (squeeze)"},
        "diff":  {"explanation": "Compares files line by line.", "example": "diff file1.txt file2.txt", "flags": "-u (unified), -r (recursive)"},
        "head":  {"explanation": "Outputs the first part of files.", "example": "head -n 20 file.txt", "flags": "-n (lines), -c (bytes)"},
        "tail":  {"explanation": "Outputs the last part of files.", "example": "tail -f logfile", "flags": "-n (lines), -f (follow)"},
    },
    "Permissions": {
        "chmod": {"explanation": "Changes file or directory permissions.", "example": "chmod 755 script.sh", "flags": "-R (recursive), +x (add execute)"},
        "chown": {"explanation": "Changes file owner and group.", "example": "chown user:group file", "flags": "-R (recursive)"},
        "chgrp": {"explanation": "Changes group ownership.", "example": "chgrp developers file", "flags": "-R (recursive)"},
        "umask": {"explanation": "Sets default permissions for new files.", "example": "umask 022", "flags": ""},
        "sudo":  {"explanation": "Executes a command as superuser.", "example": "sudo apt update", "flags": "-u (user), -i (login shell)"},
        "su":    {"explanation": "Switches to another user account.", "example": "su - root", "flags": "-l (login), -c (command)"},
    },
    "System Info": {
        "ps":       {"explanation": "Shows running processes.", "example": "ps aux | grep python", "flags": "aux (all), -ef (full format)"},
        "top":      {"explanation": "Real-time system resource viewer.", "example": "top -bn1", "flags": "-b (batch), -n (iterations)"},
        "htop":     {"explanation": "Interactive process viewer (enhanced top).", "example": "htop", "flags": ""},
        "free":     {"explanation": "Displays memory usage.", "example": "free -h", "flags": "-h (human), -m (megabytes)"},
        "uptime":   {"explanation": "Shows system uptime and load averages.", "example": "uptime", "flags": ""},
        "df":       {"explanation": "Reports filesystem disk usage.", "example": "df -h", "flags": "-h (human), -T (type)"},
        "du":       {"explanation": "Estimates file space usage.", "example": "du -sh *", "flags": "-s (summary), -h (human)"},
        "hostname": {"explanation": "Shows or sets the system hostname.", "example": "hostname -I", "flags": "-I (all IPs), -f (FQDN)"},
        "date":     {"explanation": "Displays or sets the system date/time.", "example": "date '+%Y-%m-%d'", "flags": "+FORMAT"},
        "whoami":   {"explanation": "Prints effective user name.", "example": "whoami", "flags": ""},
        "uname":    {"explanation": "Prints system information.", "example": "uname -a", "flags": "-a (all), -r (kernel)"},
        "lscpu":    {"explanation": "Displays CPU architecture info.", "example": "lscpu", "flags": ""},
        "lsblk":    {"explanation": "Lists block devices.", "example": "lsblk", "flags": "-f (filesystem info)"},
        "dmesg":    {"explanation": "Prints kernel ring buffer messages.", "example": "dmesg | tail -20", "flags": ""},
    },
    "Networking": {
        "ping":       {"explanation": "Tests connectivity to a host.", "example": "ping -c 4 google.com", "flags": "-c (count), -i (interval)"},
        "curl":       {"explanation": "Transfers data from or to a server.", "example": "curl -s https://api.github.com", "flags": "-s (silent), -o (output), -I (headers)"},
        "wget":       {"explanation": "Downloads files from the web.", "example": "wget -q https://example.com/file.zip", "flags": "-q (quiet), -r (recursive)"},
        "ssh":        {"explanation": "Secure Shell remote login.", "example": "ssh user@192.168.1.1", "flags": "-i (identity), -p (port)"},
        "scp":        {"explanation": "Secure copy over SSH.", "example": "scp file.txt user@host:~/", "flags": "-r (recursive), -P (port)"},
        "netstat":    {"explanation": "Network statistics and connections.", "example": "netstat -tuln", "flags": "-t (TCP), -u (UDP), -l (listen)"},
        "ss":         {"explanation": "Socket statistics (modern netstat).", "example": "ss -tuln", "flags": "-t (TCP), -u (UDP), -l (listen)"},
        "ip":         {"explanation": "Show/manipulate routing and network devices.", "example": "ip addr show", "flags": "addr, route, link"},
        "ifconfig":   {"explanation": "Configure network interfaces.", "example": "ifconfig eth0", "flags": ""},
        "traceroute": {"explanation": "Traces packet route to a host.", "example": "traceroute google.com", "flags": "-n (no DNS), -m (max hops)"},
        "nmap":       {"explanation": "Network exploration and port scanner.", "example": "nmap -sV 192.168.1.0/24", "flags": "-sV (version), -p (ports)"},
        "dig":        {"explanation": "DNS lookup utility.", "example": "dig google.com A", "flags": "+short, @server"},
    },
    "Package Management": {
        "apt":      {"explanation": "Debian/Ubuntu package manager.", "example": "apt install neovim", "flags": "install, remove, update, upgrade"},
        "apt-get":  {"explanation": "Older Debian/Ubuntu package manager.", "example": "apt-get install -y curl", "flags": "-y (yes), --no-install-recommends"},
        "dpkg":     {"explanation": "Low-level Debian package manager.", "example": "dpkg -i package.deb", "flags": "-i (install), -l (list), -r (remove)"},
        "snap":     {"explanation": "Snap package manager.", "example": "snap install code --classic", "flags": "--classic, --channel"},
        "pip":      {"explanation": "Python package installer.", "example": "pip install requests", "flags": "--upgrade, --user, -r (requirements)"},
        "pip3":     {"explanation": "Python 3 package installer.", "example": "pip3 install flask", "flags": "--upgrade, -r, --user"},
        "npm":      {"explanation": "Node.js package manager.", "example": "npm install express", "flags": "-g (global), --save-dev"},
        "cargo":    {"explanation": "Rust package manager.", "example": "cargo install ripgrep", "flags": "build, run, test"},
        "brew":     {"explanation": "macOS/Linux package manager.", "example": "brew install bat", "flags": "install, uninstall, update"},
    },
    "Archiving": {
        "tar":    {"explanation": "Archive utility.", "example": "tar -czf archive.tar.gz dir/", "flags": "-c (create), -x (extract), -z (gzip), -v (verbose)"},
        "zip":    {"explanation": "Creates ZIP archives.", "example": "zip -r archive.zip folder/", "flags": "-r (recursive), -e (encrypt)"},
        "unzip":  {"explanation": "Extracts ZIP archives.", "example": "unzip -o archive.zip", "flags": "-o (overwrite), -d (directory)"},
        "gzip":   {"explanation": "Compress/decompress files with gzip.", "example": "gzip -k file.txt", "flags": "-k (keep), -d (decompress), -9 (max compression)"},
        "7z":     {"explanation": "7-Zip archiver.", "example": "7z a archive.7z folder/", "flags": "a (add), e (extract), l (list)"},
        "rsync":  {"explanation": "Fast, versatile file copying tool.", "example": "rsync -avz src/ user@host:dest/", "flags": "-a (archive), -v (verbose), -z (compress)"},
    },
    "Process Management": {
        "kill":    {"explanation": "Sends a signal to a process.", "example": "kill -9 1234", "flags": "-9 (SIGKILL), -15 (SIGTERM), -l (list)"},
        "killall": {"explanation": "Kills processes by name.", "example": "killall python3", "flags": "-9 (force), -i (interactive)"},
        "pkill":   {"explanation": "Signal processes by name pattern.", "example": "pkill -f 'python.*script'", "flags": "-f (full command), -u (user)"},
        "pgrep":   {"explanation": "Lists PIDs matching a pattern.", "example": "pgrep -u root sshd", "flags": "-u (user), -l (list names)"},
        "nice":    {"explanation": "Runs a command with modified scheduling priority.", "example": "nice -n 10 make", "flags": "-n (niceness value)"},
        "renice":  {"explanation": "Alters priority of running processes.", "example": "renice -n 5 -p 1234", "flags": "-n (priority), -p (PID)"},
        "nohup":   {"explanation": "Runs command immune to hangups.", "example": "nohup server.py &", "flags": ""},
        "jobs":    {"explanation": "Lists active jobs in current shell.", "example": "jobs -l", "flags": "-l (PID), -r (running), -s (stopped)"},
        "bg":      {"explanation": "Resumes suspended job in background.", "example": "bg %1", "flags": ""},
        "fg":      {"explanation": "Brings job to foreground.", "example": "fg %1", "flags": ""},
        "watch":   {"explanation": "Executes a program periodically.", "example": "watch -n 1 'df -h'", "flags": "-n (interval), -d (highlight changes)"},
    },
    "Git": {
        "git init":   {"explanation": "Initializes a new Git repository.", "example": "git init", "flags": "--bare, --initial-branch"},
        "git clone":  {"explanation": "Clones a repository.", "example": "git clone https://github.com/user/repo.git", "flags": "--depth (shallow), -b (branch)"},
        "git add":    {"explanation": "Stages changes for commit.", "example": "git add -A", "flags": "-A (all), -p (patch), . (current dir)"},
        "git commit": {"explanation": "Records staged changes.", "example": "git commit -m 'feat: add feature'", "flags": "-m (message), --amend, -a (stage all)"},
        "git push":   {"explanation": "Pushes commits to remote.", "example": "git push origin main", "flags": "-u (set upstream), --force-with-lease"},
        "git pull":   {"explanation": "Fetches and merges from remote.", "example": "git pull --rebase", "flags": "--rebase, --ff-only"},
        "git status": {"explanation": "Shows working tree status.", "example": "git status -s", "flags": "-s (short), -b (branch)"},
        "git log":    {"explanation": "Shows commit history.", "example": "git log --oneline --graph", "flags": "--oneline, --graph, -n (limit)"},
        "git branch": {"explanation": "Lists, creates, or deletes branches.", "example": "git branch -a", "flags": "-a (all), -d (delete), -m (rename)"},
        "git stash":  {"explanation": "Stashes the working directory changes.", "example": "git stash pop", "flags": "push, pop, list, drop"},
    },
    "Docker": {
        "docker ps":      {"explanation": "Lists running containers.", "example": "docker ps -a", "flags": "-a (all), -q (IDs only)"},
        "docker run":     {"explanation": "Creates and starts a container.", "example": "docker run -d -p 80:80 nginx", "flags": "-d (detach), -p (port), -v (volume), -e (env)"},
        "docker build":   {"explanation": "Builds an image from a Dockerfile.", "example": "docker build -t myapp:1.0 .", "flags": "-t (tag), --no-cache, -f (file)"},
        "docker exec":    {"explanation": "Executes a command in a running container.", "example": "docker exec -it mycontainer bash", "flags": "-it (interactive tty)"},
        "docker logs":    {"explanation": "Fetches logs of a container.", "example": "docker logs -f mycontainer", "flags": "-f (follow), --tail (lines)"},
        "docker pull":    {"explanation": "Pulls an image from a registry.", "example": "docker pull ubuntu:22.04", "flags": ""},
        "docker stop":    {"explanation": "Stops running containers.", "example": "docker stop mycontainer", "flags": ""},
        "docker rm":      {"explanation": "Removes containers.", "example": "docker rm -f mycontainer", "flags": "-f (force), -v (volumes)"},
        "docker images":  {"explanation": "Lists local images.", "example": "docker images -a", "flags": "-a (all), -q (IDs only)"},
        "docker-compose": {"explanation": "Manages multi-container applications.", "example": "docker-compose up -d", "flags": "up, down, ps, logs"},
    },
}

QUICK_SNIPPETS = {
    "Find large files (>100MB)": "find / -type f -size +100M 2>/dev/null",
    "Show listening ports":       "ss -tuln | grep LISTEN",
    "Monitor live logs":          "tail -f /var/log/syslog",
    "CPU usage by process":       "ps aux --sort=-%cpu | head -15",
    "Memory usage by process":    "ps aux --sort=-%mem | head -15",
    "Disk usage top dirs":        "du -sh /* 2>/dev/null | sort -rh | head -10",
    "Check open file handles":    "lsof | wc -l",
    "Network connections count":  "ss -s",
    "Last 10 logins":             "last -n 10",
    "Scheduled cron jobs":        "crontab -l",
    "Active systemd services":    "systemctl list-units --state=active --type=service",
    "Environment variables":      "env | sort",
    "Running Docker containers":  "docker ps --format 'table {{.Names}}\\t{{.Status}}\\t{{.Ports}}'",
    "Git log one-line graph":     "git log --oneline --graph --all --decorate",
    "Python HTTP server":         "python3 -m http.server 8080",
}


def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return []

def save_history(history):
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history[-500:], f)
    except Exception:
        pass

class ShellConsole2026:
    def __init__(self):
        self.history = load_history()
        self.history_index = -1
        self.current_process = None
        self.auto_scroll = True

        self._build_login()

    def _build_login(self):
        self.login_win = tk.Tk()
        self.login_win.title("SYS//ACCESS")
        self.login_win.geometry("460x520")
        self.login_win.resizable(False, False)
        self.login_win.configure(bg=BG_DEEP)
        self._center(self.login_win, 460, 520)

        canvas = tk.Canvas(self.login_win, bg=BG_DEEP, highlightthickness=0, width=460, height=520)
        canvas.pack(fill="both", expand=True)

        for i in range(0, 460, 30):
            canvas.create_line(i, 0, i, 520, fill="#111122", width=1)
        for i in range(0, 520, 30):
            canvas.create_line(0, i, 460, i, fill="#111122", width=1)

        canvas.create_oval(155, 50, 305, 200, outline=ACCENT1, width=2)
        canvas.create_oval(165, 60, 295, 190, outline=ACCENT2, width=1)
        canvas.create_text(230, 125, text="⚡", font=("Segoe UI Emoji", 40), fill=ACCENT1)

        canvas.create_text(230, 220, text="SYS//ACCESS", font=("Consolas", 22, "bold"), fill=TEXT_PRI)
        canvas.create_text(230, 248, text="Authorized Personnel Only", font=("Consolas", 9), fill=TEXT_SEC)


        canvas.create_text(80, 285, text="USER_ID", font=FONT_MONO_SM, fill=ACCENT1, anchor="w")
        self.l_user = tk.Entry(self.login_win, font=FONT_MONO, bg=BG_INPUT, fg=TEXT_PRI,
                               insertbackground=ACCENT1, relief="flat", bd=0,
                               highlightthickness=1, highlightcolor=ACCENT1, highlightbackground=BORDER)
        self.l_user.place(x=80, y=298, width=300, height=32)

  

        canvas.create_text(80, 348, text="AUTH_KEY", font=FONT_MONO_SM, fill=ACCENT1, anchor="w")
        self.l_pass = tk.Entry(self.login_win, font=FONT_MONO, bg=BG_INPUT, fg=TEXT_PRI,
                               insertbackground=ACCENT1, relief="flat", bd=0, show="●",
                               highlightthickness=1, highlightcolor=ACCENT1, highlightbackground=BORDER)
        self.l_pass.place(x=80, y=360, width=300, height=32)

        self.l_err = canvas.create_text(230, 410, text="", font=FONT_MONO_SM, fill=ERROR)

        btn_frame = tk.Frame(self.login_win, bg=BG_DEEP)
        btn_frame.place(x=80, y=425, width=300, height=40)
        self._styled_btn(btn_frame, "AUTHENTICATE →", self._do_login, ACCENT1).pack(fill="x")

        canvas.create_text(230, 490, text="v2.6.0 · NEXUS SHELL · © 2026", font=FONT_SMALL, fill=TEXT_SEC)

        self.l_pass.bind("<Return>", lambda e: self._do_login())
        self.l_user.bind("<Return>", lambda e: self.l_pass.focus())
        self.login_win.mainloop()

    def _do_login(self):
        u = self.l_user.get()
        p = self.l_pass.get()
        if u == "neha" and p == "neha":
            self.login_win.destroy()
            self._build_console()
        else:
            self.login_win.nametowidget(self.login_win.children.get(
                list(self.login_win.children.keys())[0], self.login_win
            ))
           

            for widget in self.login_win.winfo_children():
                if isinstance(widget, tk.Canvas):
                    widget.itemconfig(self.l_err, text="⛔  INVALID CREDENTIALS — ACCESS DENIED")
                    break


    def _build_console(self):
        self.root = tk.Tk()
        self.root.title("NEXUS SHELL · 2026")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG_DEEP)
        self._center(self.root, 1200, 800)

        self._apply_ttk_styles()
        self._build_titlebar()
        self._build_main()
        self._start_live_metrics()
        self._fetch_weather_async()
        self.root.mainloop()

    def _apply_ttk_styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TCombobox", fieldbackground=BG_INPUT, background=BG_INPUT,
                    foreground=TEXT_PRI, bordercolor=BORDER, arrowcolor=ACCENT1,
                    selectbackground=ACCENT2, selectforeground=TEXT_PRI)
        s.map("TCombobox", fieldbackground=[("readonly", BG_INPUT)],
              foreground=[("readonly", TEXT_PRI)], background=[("readonly", BG_INPUT)])
        s.configure("TNotebook", background=BG_PANEL, bordercolor=BORDER)
        s.configure("TNotebook.Tab", background=BG_CARD, foreground=TEXT_SEC,
                    padding=[14, 6], font=FONT_MONO_SM, bordercolor=BORDER)
        s.map("TNotebook.Tab", background=[("selected", BG_INPUT)],
              foreground=[("selected", ACCENT1)])
        s.configure("Vertical.TScrollbar", background=BG_CARD, troughcolor=BG_DEEP,
                    bordercolor=BORDER, arrowcolor=ACCENT1, width=6)
        s.configure("Horizontal.TScrollbar", background=BG_CARD, troughcolor=BG_DEEP,
                    bordercolor=BORDER, arrowcolor=ACCENT1, width=6)

    def _build_titlebar(self):
        tb = tk.Frame(self.root, bg=BG_PANEL, height=52)
        tb.pack(fill="x", side="top")
        tb.pack_propagate(False)

    
        tk.Label(tb, text=" ⚡ NEXUS", font=("Consolas", 14, "bold"),
                 bg=BG_PANEL, fg=ACCENT1).pack(side="left", padx=14)
        tk.Label(tb, text="SHELL v2.6", font=("Consolas", 9),
                 bg=BG_PANEL, fg=TEXT_SEC).pack(side="left")

  
        self.chip_user = self._chip(tb, f"USER: NEHA", ACCENT2)
        self.chip_user.pack(side="right", padx=(4, 14))

        self.chip_time = self._chip(tb, "00:00:00", ACCENT1)
        self.chip_time.pack(side="right", padx=4)

        self.chip_weather = self._chip(tb, "WEATHER …", SUCCESS)
        self.chip_weather.pack(side="right", padx=4)

        self.chip_os = self._chip(tb, platform.system().upper(), WARNING)
        self.chip_os.pack(side="right", padx=4)

        self._update_clock()

    def _chip(self, parent, text, color):
        f = tk.Frame(parent, bg=color, padx=6, pady=2)
        lbl = tk.Label(f, text=text, font=("Consolas", 8, "bold"), bg=color, fg=BG_DEEP)
        lbl.pack()
        f._lbl = lbl
        return f

    def _build_main(self):

        paned = tk.PanedWindow(self.root, orient="horizontal",
                               bg=BG_DEEP, sashwidth=4, sashrelief="flat",
                               sashpad=0)
        paned.pack(fill="both", expand=True, padx=0, pady=0)


        sidebar = tk.Frame(paned, bg=BG_PANEL, width=260)
        sidebar.pack_propagate(False)
        paned.add(sidebar, minsize=220)

        self._build_sidebar(sidebar)


        content = tk.Frame(paned, bg=BG_DEEP)
        paned.add(content, minsize=500)

        self._build_content(content)

    def _build_sidebar(self, parent):
        tk.Label(parent, text="COMMAND REFERENCE", font=("Consolas", 8, "bold"),
                 bg=BG_PANEL, fg=TEXT_SEC).pack(anchor="w", padx=12, pady=(12, 4))


        self.cat_var = tk.StringVar()
        cat_combo = ttk.Combobox(parent, textvariable=self.cat_var,
                                 values=list(command_explanations.keys()),
                                 state="readonly", font=FONT_MONO_SM)
        cat_combo.pack(fill="x", padx=10, pady=(0, 6))
        cat_combo.set(list(command_explanations.keys())[0])
        cat_combo.bind("<<ComboboxSelected>>", self._on_category_change)


        tk.Label(parent, text="COMMANDS", font=("Consolas", 8),
                 bg=BG_PANEL, fg=TEXT_SEC).pack(anchor="w", padx=12)

        cmd_frame = tk.Frame(parent, bg=BG_PANEL)
        cmd_frame.pack(fill="x", padx=10, pady=(2, 6))

        sb = tk.Scrollbar(cmd_frame, bg=BG_CARD, troughcolor=BG_DEEP,
                          activebackground=ACCENT1, width=6, relief="flat")
        self.cmd_listbox = tk.Listbox(cmd_frame, bg=BG_CARD, fg=TEXT_PRI,
                                      selectbackground=ACCENT2, selectforeground=TEXT_PRI,
                                      font=FONT_MONO_SM, relief="flat", bd=0,
                                      activestyle="none", height=10, yscrollcommand=sb.set)
        sb.config(command=self.cmd_listbox.yview)
        sb.pack(side="right", fill="y")
        self.cmd_listbox.pack(side="left", fill="both", expand=True)
        self.cmd_listbox.bind("<<ListboxSelect>>", self._on_cmd_select)
        self.cmd_listbox.bind("<Double-Button-1>", self._inject_command)
        self._on_category_change(None)

        sep = tk.Frame(parent, bg=BORDER, height=1)
        sep.pack(fill="x", padx=10, pady=4)

        tk.Label(parent, text="DESCRIPTION", font=("Consolas", 8),
                 bg=BG_PANEL, fg=TEXT_SEC).pack(anchor="w", padx=12)

        self.explain_text = tk.Text(parent, bg=BG_CARD, fg=TEXT_PRI,
                                    font=FONT_MONO_SM, relief="flat", bd=0,
                                    wrap="word", height=5, padx=8, pady=6,
                                    state="disabled")
        self.explain_text.pack(fill="x", padx=10, pady=(2, 4))
        self.explain_text.tag_config("key", foreground=ACCENT1, font=("Consolas", 9, "bold"))
        self.explain_text.tag_config("val", foreground=TEXT_PRI, font=FONT_MONO_SM)
        self.explain_text.tag_config("ex",  foreground=SUCCESS,  font=FONT_MONO_SM)
        self.explain_text.tag_config("flag",foreground=WARNING,  font=FONT_MONO_SM)

        sep2 = tk.Frame(parent, bg=BORDER, height=1)
        sep2.pack(fill="x", padx=10, pady=4)


        tk.Label(parent, text="QUICK SNIPPETS", font=("Consolas", 8),
                 bg=BG_PANEL, fg=TEXT_SEC).pack(anchor="w", padx=12)

        snip_outer = tk.Frame(parent, bg=BG_PANEL)
        snip_outer.pack(fill="both", expand=True, padx=10, pady=(2, 10))

        snip_sb = tk.Scrollbar(snip_outer, bg=BG_CARD, troughcolor=BG_DEEP,
                               activebackground=ACCENT1, width=6, relief="flat")
        self.snip_listbox = tk.Listbox(snip_outer, bg=BG_CARD, fg=ACCENT3,
                                       selectbackground=ACCENT2, selectforeground=TEXT_PRI,
                                       font=("Consolas", 8), relief="flat", bd=0,
                                       activestyle="none", yscrollcommand=snip_sb.set)
        snip_sb.config(command=self.snip_listbox.yview)
        snip_sb.pack(side="right", fill="y")
        self.snip_listbox.pack(side="left", fill="both", expand=True)

        for name in QUICK_SNIPPETS:
            self.snip_listbox.insert(tk.END, f"  {name}")
        self.snip_listbox.bind("<Double-Button-1>", self._inject_snippet)

    def _build_content(self, parent):
        nb = ttk.Notebook(parent)
        nb.pack(fill="both", expand=True, padx=0, pady=0)

        term_tab = tk.Frame(nb, bg=BG_DEEP)
        nb.add(term_tab, text="  ⟩_ TERMINAL  ")
        self._build_terminal_tab(term_tab)

   
        mon_tab = tk.Frame(nb, bg=BG_DEEP)
        nb.add(mon_tab, text="  ◎ MONITOR  ")
        self._build_monitor_tab(mon_tab)

        notes_tab = tk.Frame(nb, bg=BG_DEEP)
        nb.add(notes_tab, text="  ✎ NOTES  ")
        self._build_notes_tab(notes_tab)


        shortcuts_tab = tk.Frame(nb, bg=BG_DEEP)
        nb.add(shortcuts_tab, text="  ⌨ SHORTCUTS  ")
        self._build_shortcuts_tab(shortcuts_tab)


    def _build_terminal_tab(self, parent):
        
        toolbar = tk.Frame(parent, bg=BG_PANEL, height=40)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)

        def tb_btn(txt, cmd, color=ACCENT1):
            b = tk.Button(toolbar, text=txt, font=("Consolas", 8, "bold"),
                          bg=BG_CARD, fg=color, activebackground=BG_INPUT,
                          activeforeground=color, relief="flat", bd=0,
                          padx=10, pady=4, cursor="hand2", command=cmd)
            b.pack(side="left", padx=(4, 0), pady=4)
            return b

        tb_btn("▶  RUN", self._run_command, SUCCESS)
        tb_btn("✕  CLEAR", self._clear_output, ERROR)
        tb_btn("⌛  HISTORY", self._show_history, WARNING)
        tb_btn("⬆  EXPORT LOG", self._export_log, ACCENT2)
        tb_btn("⏹  KILL", self._kill_process, ACCENT3)

        self.autoscroll_var = tk.BooleanVar(value=True)
        chk = tk.Checkbutton(toolbar, text="AUTO-SCROLL", variable=self.autoscroll_var,
                             bg=BG_PANEL, fg=TEXT_SEC, selectcolor=BG_CARD,
                             activebackground=BG_PANEL, font=("Consolas", 8))
        chk.pack(side="right", padx=10)

    
        input_row = tk.Frame(parent, bg=BG_DEEP, pady=6)
        input_row.pack(fill="x", padx=12)

        tk.Label(input_row, text="⟩", font=("Consolas", 14, "bold"),
                 bg=BG_DEEP, fg=SUCCESS).pack(side="left")

        self.cmd_entry = tk.Entry(input_row, font=("Consolas", 11),
                                  bg=BG_INPUT, fg=TEXT_PRI, insertbackground=ACCENT1,
                                  relief="flat", bd=0,
                                  highlightthickness=1, highlightcolor=ACCENT1,
                                  highlightbackground=BORDER)
        self.cmd_entry.pack(side="left", fill="x", expand=True, padx=(8, 8), ipady=5)
        self.cmd_entry.bind("<Return>",    lambda e: self._run_command())
        self.cmd_entry.bind("<Up>",        self._history_up)
        self.cmd_entry.bind("<Down>",      self._history_down)
        self.cmd_entry.bind("<Tab>",       self._tab_complete)
        self.cmd_entry.focus()

        tk.Label(input_row, text="[ TAB=complete ↑↓=history ]",
                 font=("Consolas", 7), bg=BG_DEEP, fg=TEXT_SEC).pack(side="right")

     
        out_frame = tk.Frame(parent, bg=BG_DEEP)
        out_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        out_sb = tk.Scrollbar(out_frame, bg=BG_CARD, troughcolor=BG_DEEP,
                              activebackground=ACCENT1, width=6, relief="flat")
        self.output_box = tk.Text(out_frame, bg=BG_DEEP, fg=TEXT_PRI,
                                  font=FONT_MONO, relief="flat", bd=0,
                                  wrap="word", padx=8, pady=8, state="disabled",
                                  yscrollcommand=out_sb.set)
        out_sb.config(command=self.output_box.yview)
        out_sb.pack(side="right", fill="y")
        self.output_box.pack(side="left", fill="both", expand=True)

    
        self.output_box.tag_config("prompt",  foreground=SUCCESS,  font=("Consolas", 10, "bold"))
        self.output_box.tag_config("cmd",     foreground=ACCENT1,  font=("Consolas", 10, "bold"))
        self.output_box.tag_config("stdout",  foreground=TEXT_PRI, font=FONT_MONO)
        self.output_box.tag_config("stderr",  foreground=ERROR,    font=FONT_MONO)
        self.output_box.tag_config("info",    foreground=WARNING,  font=FONT_MONO)
        self.output_box.tag_config("success", foreground=SUCCESS,  font=FONT_MONO)
        self.output_box.tag_config("ts",      foreground=TEXT_SEC, font=("Consolas", 8))

        self._print_banner()


    def _build_monitor_tab(self, parent):
        tk.Label(parent, text="LIVE SYSTEM METRICS", font=("Consolas", 10, "bold"),
                 bg=BG_DEEP, fg=ACCENT1).pack(anchor="w", padx=16, pady=(12, 6))

        grid = tk.Frame(parent, bg=BG_DEEP)
        grid.pack(fill="x", padx=16)

        self.metric_cards = {}
        metrics = [
            ("CPU Usage",       "cpu_pct",   ACCENT1),
            ("RAM Usage",       "ram_pct",   ACCENT2),
            ("RAM Used",        "ram_used",  ACCENT3),
            ("Disk Usage",      "disk_pct",  SUCCESS),
            ("Disk Free",       "disk_free", WARNING),
            ("Uptime",          "uptime",    TEXT_SEC),
        ]
        for i, (label, key, color) in enumerate(metrics):
            card = tk.Frame(grid, bg=BG_CARD, padx=14, pady=10,
                            highlightthickness=1, highlightbackground=BORDER)
            card.grid(row=i // 3, column=i % 3, padx=6, pady=6, sticky="nsew")
            grid.grid_columnconfigure(i % 3, weight=1)

            tk.Label(card, text=label, font=("Consolas", 8), bg=BG_CARD, fg=TEXT_SEC).pack(anchor="w")
            val_lbl = tk.Label(card, text="—", font=("Consolas", 20, "bold"), bg=BG_CARD, fg=color)
            val_lbl.pack(anchor="w")
            self.metric_cards[key] = val_lbl

       
        tk.Label(parent, text="TOP PROCESSES", font=("Consolas", 10, "bold"),
                 bg=BG_DEEP, fg=ACCENT1).pack(anchor="w", padx=16, pady=(16, 4))

        cols = ("PID", "Name", "CPU %", "RAM %", "Status")
        tree_frame = tk.Frame(parent, bg=BG_DEEP)
        tree_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        tree_sb = ttk.Scrollbar(tree_frame, orient="vertical")
        self.proc_tree = ttk.Treeview(tree_frame, columns=cols, show="headings",
                                      height=10, yscrollcommand=tree_sb.set)
        tree_sb.config(command=self.proc_tree.yview)
        tree_sb.pack(side="right", fill="y")
        self.proc_tree.pack(side="left", fill="both", expand=True)

        s = ttk.Style()
        s.configure("Treeview", background=BG_CARD, foreground=TEXT_PRI,
                    fieldbackground=BG_CARD, font=FONT_MONO_SM, rowheight=22)
        s.configure("Treeview.Heading", background=BG_INPUT, foreground=ACCENT1,
                    font=("Consolas", 9, "bold"))
        s.map("Treeview", background=[("selected", ACCENT2)])

        for col in cols:
            self.proc_tree.heading(col, text=col)
            w = 80 if col in ("PID", "CPU %", "RAM %", "Status") else 200
            self.proc_tree.column(col, width=w, anchor="center" if col != "Name" else "w")

   
    def _build_notes_tab(self, parent):
        bar = tk.Frame(parent, bg=BG_PANEL, height=36)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        def nb_btn(txt, cmd, color=ACCENT1):
            tk.Button(bar, text=txt, font=("Consolas", 8, "bold"),
                      bg=BG_CARD, fg=color, activebackground=BG_INPUT,
                      activeforeground=color, relief="flat", bd=0,
                      padx=10, pady=3, cursor="hand2", command=cmd).pack(side="left", padx=4, pady=4)

        nb_btn("💾 SAVE", self._save_notes, SUCCESS)
        nb_btn("📂 OPEN", self._open_notes, ACCENT1)
        nb_btn("✕ CLEAR", lambda: self.notes_box.delete("1.0", tk.END), ERROR)

        tk.Label(bar, text="Scratch pad — saved between sessions",
                 font=("Consolas", 8), bg=BG_PANEL, fg=TEXT_SEC).pack(side="right", padx=12)

        self.notes_box = tk.Text(parent, bg=BG_DEEP, fg=TEXT_PRI,
                                 font=("Consolas", 11), relief="flat", bd=0,
                                 padx=16, pady=12, insertbackground=ACCENT1,
                                 wrap="word")
        self.notes_box.pack(fill="both", expand=True)
        self._load_notes()

   
    def _build_shortcuts_tab(self, parent):
        tk.Label(parent, text="KEYBOARD SHORTCUTS & QUICK LINKS",
                 font=("Consolas", 10, "bold"), bg=BG_DEEP, fg=ACCENT1).pack(anchor="w", padx=16, pady=(12, 6))

        cols_frame = tk.Frame(parent, bg=BG_DEEP)
        cols_frame.pack(fill="both", expand=True, padx=16)

        shortcuts = [
            ("Enter",    "Execute command"),
            ("↑ / ↓",    "Navigate history"),
            ("Tab",      "Auto-complete from history"),
            ("Ctrl+C",   "Kill running process"),
            ("Ctrl+L",   "Clear output"),
            ("Ctrl+H",   "Show history"),
        ]
        left = tk.Frame(cols_frame, bg=BG_DEEP)
        left.pack(side="left", fill="both", expand=True)

        tk.Label(left, text="TERMINAL SHORTCUTS", font=("Consolas", 9, "bold"),
                 bg=BG_DEEP, fg=TEXT_SEC).pack(anchor="w", pady=(0, 6))

        for key, desc in shortcuts:
            row = tk.Frame(left, bg=BG_CARD, pady=4, padx=10)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=key, font=("Consolas", 9, "bold"),
                     bg=BG_CARD, fg=ACCENT1, width=12, anchor="w").pack(side="left")
            tk.Label(row, text=desc, font=("Consolas", 9),
                     bg=BG_CARD, fg=TEXT_PRI).pack(side="left")

        right = tk.Frame(cols_frame, bg=BG_DEEP)
        right.pack(side="left", fill="both", expand=True, padx=(24, 0))

        tk.Label(right, text="QUICK LINKS", font=("Consolas", 9, "bold"),
                 bg=BG_DEEP, fg=TEXT_SEC).pack(anchor="w", pady=(0, 6))

        links = [
            ("▶  YouTube",       "https://www.youtube.com",       ACCENT3),
            ("🎵  Spotify",        "https://open.spotify.com",      SUCCESS),
            ("🐙  GitHub",         "https://github.com",            ACCENT1),
            ("🐳  Docker Hub",     "https://hub.docker.com",        ACCENT2),
            ("📖  Linux Man Pages","https://man7.org/linux/man-pages/", WARNING),
            ("🔍  Explainshell",   "https://explainshell.com",       TEXT_PRI),
        ]
        for label, url, color in links:
            btn = tk.Button(right, text=label, font=("Consolas", 9),
                            bg=BG_CARD, fg=color, activebackground=BG_INPUT,
                            activeforeground=color, relief="flat", bd=0,
                            pady=5, padx=10, cursor="hand2",
                            command=lambda u=url: webbrowser.open(u))
            btn.pack(fill="x", pady=2, anchor="w")

    
        tk.Label(parent, text="Tip: Double-click any command in the sidebar to inject it into the terminal",
                 font=("Consolas", 8), bg=BG_DEEP, fg=TEXT_SEC).pack(anchor="w", padx=16, pady=12)

    
        self.root.bind("<Control-l>", lambda e: self._clear_output())
        self.root.bind("<Control-h>", lambda e: self._show_history())


    def _print_banner(self):
        banner = (
            f"  ╔══════════════════════════════════════════════════╗\n"
            f"  ║   NEXUS SHELL v2.6.0  ·  {platform.system()} {platform.release()[:10]:<12}   ║\n"
            f"  ║   Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}          ║\n"
            f"  ║   Type any command · Double-click sidebar items  ║\n"
            f"  ╚══════════════════════════════════════════════════╝\n\n"
        )
        self._append_output(banner, "success")

    def _append_output(self, text, tag="stdout"):
        self.output_box.config(state="normal")
        self.output_box.insert(tk.END, text, tag)
        self.output_box.config(state="disabled")
        if self.autoscroll_var.get():
            self.output_box.see(tk.END)

    def _run_command(self):
        cmd = self.cmd_entry.get().strip()
        if not cmd:
            return

        ts = datetime.now().strftime("%H:%M:%S")
        self._append_output(f"[{ts}] ", "ts")
        self._append_output("⟩ ", "prompt")
        self._append_output(f"{cmd}\n", "cmd")

        self.history.append(cmd)
        self.history_index = -1
        save_history(self.history)

        self.cmd_entry.delete(0, tk.END)

        threading.Thread(target=self._exec_and_display, args=(cmd,), daemon=True).start()

    def _exec_and_display(self, cmd):
        try:
            self.current_process = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True
            )
            stdout, stderr = self.current_process.communicate(timeout=30)
            rc = self.current_process.returncode

            if stdout:
                self.root.after(0, self._append_output, stdout, "stdout")
            if stderr:
                self.root.after(0, self._append_output, stderr, "stderr")

            status = "✓" if rc == 0 else f"✗ exit {rc}"
            color  = "success" if rc == 0 else "stderr"
            self.root.after(0, self._append_output, f"\n{status}\n\n", color)

        except subprocess.TimeoutExpired:
            self.root.after(0, self._append_output, "⏱ Command timed out (30s limit)\n\n", "stderr")
        except Exception as e:
            self.root.after(0, self._append_output, f"Error: {e}\n\n", "stderr")
        finally:
            self.current_process = None

    def _clear_output(self):
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.config(state="disabled")
        self._print_banner()

    def _kill_process(self):
        if self.current_process:
            self.current_process.terminate()
            self._append_output("⏹ Process terminated\n\n", "stderr")
        else:
            self._append_output("No running process to kill.\n\n", "info")

    def _export_log(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt")],
            title="Export Terminal Log"
        )
        if path:
            content = self.output_box.get("1.0", tk.END)
            with open(path, "w") as f:
                f.write(content)
            self._append_output(f"📄 Log exported to {path}\n\n", "success")

    def _history_up(self, event):
        if not self.history:
            return
        self.history_index = max(0, self.history_index - 1) if self.history_index >= 0 \
            else len(self.history) - 1
        self.cmd_entry.delete(0, tk.END)
        self.cmd_entry.insert(0, self.history[self.history_index])

    def _history_down(self, event):
        if self.history_index < 0:
            return
        self.history_index += 1
        self.cmd_entry.delete(0, tk.END)
        if self.history_index < len(self.history):
            self.cmd_entry.insert(0, self.history[self.history_index])
        else:
            self.history_index = -1

    def _tab_complete(self, event):
        typed = self.cmd_entry.get()
        if not typed:
            return "break"
        matches = [h for h in reversed(self.history) if h.startswith(typed) and h != typed]
        if matches:
            self.cmd_entry.delete(0, tk.END)
            self.cmd_entry.insert(0, matches[0])
        return "break"


    def _on_category_change(self, event):
        cat = self.cat_var.get()
        cmds = list(command_explanations.get(cat, {}).keys())
        self.cmd_listbox.delete(0, tk.END)
        for c in cmds:
            self.cmd_listbox.insert(tk.END, f"  {c}")

    def _on_cmd_select(self, event):
        sel = self.cmd_listbox.curselection()
        if not sel:
            return
        cmd = self.cmd_listbox.get(sel[0]).strip()
        cat = self.cat_var.get()
        info = command_explanations.get(cat, {}).get(cmd, {})
        self._update_explain(cmd, info)

    def _update_explain(self, cmd, info):
        self.explain_text.config(state="normal")
        self.explain_text.delete("1.0", tk.END)
        self.explain_text.insert(tk.END, "CMD  ", "key")
        self.explain_text.insert(tk.END, cmd + "\n", "val")
        self.explain_text.insert(tk.END, "INFO ", "key")
        self.explain_text.insert(tk.END, info.get("explanation", "—") + "\n", "val")
        self.explain_text.insert(tk.END, "EX   ", "key")
        self.explain_text.insert(tk.END, info.get("example", "—") + "\n", "ex")
        if info.get("flags"):
            self.explain_text.insert(tk.END, "FLAGS", "key")
            self.explain_text.insert(tk.END, " " + info["flags"] + "\n", "flag")
        self.explain_text.config(state="disabled")

    def _inject_command(self, event):
        sel = self.cmd_listbox.curselection()
        if not sel:
            return
        cmd = self.cmd_listbox.get(sel[0]).strip()
        cat = self.cat_var.get()
        example = command_explanations.get(cat, {}).get(cmd, {}).get("example", cmd)
        self.cmd_entry.delete(0, tk.END)
        self.cmd_entry.insert(0, example)
        self.cmd_entry.focus()

    def _inject_snippet(self, event):
        sel = self.snip_listbox.curselection()
        if not sel:
            return
        name = self.snip_listbox.get(sel[0]).strip()
        snippet = QUICK_SNIPPETS.get(name, "")
        self.cmd_entry.delete(0, tk.END)
        self.cmd_entry.insert(0, snippet)
        self.cmd_entry.focus()


    def _show_history(self):
        hw = tk.Toplevel(self.root)
        hw.title("COMMAND HISTORY")
        hw.geometry("600x480")
        hw.configure(bg=BG_DEEP)
        hw.grab_set()

        tk.Label(hw, text="COMMAND HISTORY", font=("Consolas", 11, "bold"),
                 bg=BG_DEEP, fg=ACCENT1).pack(pady=(12, 4))

        search_var = tk.StringVar()
        search_entry = tk.Entry(hw, textvariable=search_var, font=FONT_MONO,
                                bg=BG_INPUT, fg=TEXT_PRI, insertbackground=ACCENT1,
                                relief="flat", bd=0,
                                highlightthickness=1, highlightcolor=ACCENT1,
                                highlightbackground=BORDER)
        search_entry.pack(fill="x", padx=16, pady=(0, 6), ipady=4)
        tk.Label(hw, text="Filter…", font=("Consolas", 8), bg=BG_DEEP, fg=TEXT_SEC).pack(anchor="w", padx=16)

        frame = tk.Frame(hw, bg=BG_DEEP)
        frame.pack(fill="both", expand=True, padx=16, pady=8)

        sb = tk.Scrollbar(frame, bg=BG_CARD, troughcolor=BG_DEEP, width=6, relief="flat")
        lb = tk.Listbox(frame, bg=BG_CARD, fg=TEXT_PRI, selectbackground=ACCENT2,
                        font=FONT_MONO_SM, relief="flat", bd=0, activestyle="none",
                        yscrollcommand=sb.set)
        sb.config(command=lb.yview)
        sb.pack(side="right", fill="y")
        lb.pack(side="left", fill="both", expand=True)

        def refresh(val=""):
            lb.delete(0, tk.END)
            for i, cmd in enumerate(reversed(self.history)):
                if val.lower() in cmd.lower():
                    lb.insert(tk.END, f"  {cmd}")

        search_var.trace("w", lambda *a: refresh(search_var.get()))
        refresh()

        btn_row = tk.Frame(hw, bg=BG_DEEP)
        btn_row.pack(pady=8)

        def use_selected():
            sel = lb.curselection()
            if sel:
                self.cmd_entry.delete(0, tk.END)
                self.cmd_entry.insert(0, lb.get(sel[0]).strip())
                hw.destroy()
                self.cmd_entry.focus()

        def clear_all():
            if messagebox.askyesno("Clear History", "Clear all command history?"):
                self.history.clear()
                save_history(self.history)
                lb.delete(0, tk.END)

        self._styled_btn(btn_row, "↳ USE SELECTED", use_selected, SUCCESS).pack(side="left", padx=4)
        self._styled_btn(btn_row, "✕ CLEAR ALL", clear_all, ERROR).pack(side="left", padx=4)
        lb.bind("<Double-Button-1>", lambda e: use_selected())


    def _start_live_metrics(self):
        self._update_metrics()

    def _update_metrics(self):
        try:
            cpu    = psutil.cpu_percent(interval=None)
            ram    = psutil.virtual_memory()
            disk   = psutil.disk_usage("/")
            boot   = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot
            h, rem = divmod(int(uptime.total_seconds()), 3600)
            m, s   = divmod(rem, 60)

            self.metric_cards["cpu_pct"].config(text=f"{cpu:.1f}%")
            self.metric_cards["ram_pct"].config(text=f"{ram.percent:.1f}%")
            self.metric_cards["ram_used"].config(text=f"{ram.used/1e9:.2f} GB")
            self.metric_cards["disk_pct"].config(text=f"{disk.percent:.1f}%")
            self.metric_cards["disk_free"].config(text=f"{disk.free/1e9:.1f} GB")
            self.metric_cards["uptime"].config(text=f"{h:02d}:{m:02d}:{s:02d}")


            for row in self.proc_tree.get_children():
                self.proc_tree.delete(row)

            procs = []
            for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status"]):
                try:
                    procs.append(p.info)
                except Exception:
                    pass
            procs.sort(key=lambda x: x.get("cpu_percent", 0) or 0, reverse=True)

            for p in procs[:20]:
                self.proc_tree.insert("", tk.END, values=(
                    p.get("pid", ""),
                    (p.get("name", "") or "")[:30],
                    f"{p.get('cpu_percent', 0):.1f}",
                    f"{p.get('memory_percent', 0):.1f}",
                    p.get("status", "")
                ))
        except Exception:
            pass

        self.root.after(2000, self._update_metrics)

    def _fetch_weather_async(self):
        threading.Thread(target=self._do_fetch_weather, daemon=True).start()

    def _do_fetch_weather(self):
        try:
            r = requests.get(URL, timeout=8)
            d = r.json()
            if d.get("cod") == 200:
                temp = d["main"]["temp"]
                desc = d["weather"][0]["description"].title()
                text = f"{desc} {temp:.0f}°C"
            else:
                text = "WEATHER N/A"
        except Exception:
            text = "WEATHER ERR"
        self.root.after(0, lambda: self.chip_weather._lbl.config(text=text))
        self.root.after(600000, self._fetch_weather_async)


    def _update_clock(self):
        t = time.strftime("%H:%M:%S")
        self.chip_time._lbl.config(text=t)
        self.root.after(1000, self._update_clock)

    NOTES_FILE = os.path.expanduser("~/.shell_console_notes.txt")

    def _load_notes(self):
        try:
            if os.path.exists(self.NOTES_FILE):
                with open(self.NOTES_FILE) as f:
                    self.notes_box.insert("1.0", f.read())
        except Exception:
            pass

    def _save_notes(self):
        try:
            with open(self.NOTES_FILE, "w") as f:
                f.write(self.notes_box.get("1.0", tk.END))
            messagebox.showinfo("Saved", "Notes saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _open_notes(self):
        path = filedialog.askopenfilename(filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if path:
            with open(path) as f:
                self.notes_box.delete("1.0", tk.END)
                self.notes_box.insert("1.0", f.read())


    @staticmethod
    def _center(win, w, h):
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        win.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    @staticmethod
    def _styled_btn(parent, text, cmd, color=ACCENT1):
        return tk.Button(parent, text=text, font=("Consolas", 8, "bold"),
                         bg=BG_CARD, fg=color, activebackground=BG_INPUT,
                         activeforeground=color, relief="flat", bd=0,
                         padx=14, pady=6, cursor="hand2", command=cmd)


if __name__ == "__main__":

    try:
        import psutil
    except ImportError:
        import subprocess as _sp
        _sp.run(["pip", "install", "psutil", "--break-system-packages", "-q"])
        import psutil

    ShellConsole2026()