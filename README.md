# ⚡ NEXUS SHELL v2.6

> A modern, feature-rich Linux command learning and execution console built with Python and Tkinter — redesigned for 2026.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

---

## 📸 Overview

Nexus Shell is a desktop GUI application that serves as both a **Linux command reference** and a **live terminal emulator**. It features a dark cyberpunk aesthetic, real-time system monitoring, command history persistence, quick snippets, and more — all wrapped in a sleek 2026-style interface.

Originally built as an OS course project, it has since been fully redesigned with production-grade UI, threaded execution, and an expanded command database covering Git, Docker, networking, and more.

---

## ✨ Features

### 🖥️ Terminal
- Execute any shell command directly from the GUI
- Color-coded output: green = success, red = errors, cyan = commands
- **Threaded execution** — UI never freezes during long commands
- **Kill button** — terminate a running process mid-execution
- **30-second timeout** protection
- **Export log** — save your terminal session to a `.log` file

### 📚 Command Reference Sidebar
- **80+ commands** organized across 10 categories:
  - File Management, Text Processing, Permissions, System Info
  - Networking, Package Management, Archiving, Process Management
  - Git, Docker
- Each command shows: description, example usage, and common flags
- **Double-click** any command to inject its example directly into the terminal

### ⚡ Quick Snippets
- 15 pre-built power-user one-liners (find large files, monitor logs, top CPU processes, etc.)
- Double-click to inject instantly

### ⌨️ History
- **Persistent history** saved to `~/.shell_console_history.json` across sessions (up to 500 entries)
- Navigate with `↑` / `↓` arrow keys
- **Tab autocomplete** from history
- Searchable history window with filter

### 📊 Live System Monitor
- Real-time metrics refreshing every 2 seconds:
  - CPU usage, RAM usage & used, Disk usage & free, System uptime
- **Top 20 processes** table sorted by CPU usage (PID, name, CPU%, RAM%, status)

### ✎ Notes
- Persistent scratch pad saved to `~/.shell_console_notes.txt`
- Open and save external `.txt` files

### 🌤️ Weather
- Live weather data for Dhaka via OpenWeatherMap API
- Displayed in the top status bar, refreshed every 10 minutes

### 🔗 Quick Links
- One-click access to YouTube, Spotify, GitHub, Docker Hub, Linux Man Pages, Explainshell

---

## 🚀 Getting Started

Choose your platform below and follow the steps end-to-end.

---

### 🪟 Windows

**1. Install Python**

Download Python 3.8+ from [python.org](https://www.python.org/downloads/).
During installation, **check "Add Python to PATH"** before clicking Install.

Verify it worked:
```cmd
python --version
pip --version
```

**2. Clone the repository**
```cmd
git clone https://github.com/yourusername/nexus-shell.git
cd nexus-shell
```

Or download the ZIP from GitHub and extract it.

**3. Install dependencies**
```cmd
pip install psutil requests
```

**4. Run the app**
```cmd
python shell_console_2026.py
```

---

### 🐧 Linux (Ubuntu / Debian)

**1. Update your system**
```bash
sudo apt update && sudo apt upgrade -y
```

**2. Install Python and pip**

Ubuntu 22.04+ comes with Python 3 pre-installed. Confirm with:
```bash
python3 --version
```

If not installed:
```bash
sudo apt install python3 python3-pip -y
```

**3. Install Tkinter**

Tkinter is **not bundled** with Python on Linux — you must install it separately:
```bash
sudo apt install python3-tk -y
```

Verify it works:
```bash
python3 -c "import tkinter; print('Tkinter OK')"
```

**4. Clone the repository**
```bash
git clone https://github.com/yourusername/nexus-shell.git
cd nexus-shell
```

**5. Install Python dependencies**
```bash
pip3 install psutil requests
```

**6. Run the app**
```bash
python3 shell_console_2026.py
```

---

### 💻 Running Inside a Virtual Machine (VirtualBox / VMware)

Running Nexus Shell inside a VM (e.g. Ubuntu on VirtualBox) requires a few extra steps because the GUI needs access to the VM's display.

#### Step 1 — Set up your VM display

In **VirtualBox**:
- Go to **Settings → Display**
- Set **Video Memory** to at least **64 MB**
- Enable **3D Acceleration** if available

In **VMware**:
- Go to **VM → Settings → Display**
- Enable **Accelerate 3D graphics**

#### Step 2 — Install Guest Additions (VirtualBox only)

Guest Additions improves display rendering and clipboard sharing.

Boot into your Ubuntu VM, then:
```bash
sudo apt install virtualbox-guest-utils virtualbox-guest-x11 -y
sudo reboot
```

Or from the VirtualBox menu: **Devices → Insert Guest Additions CD image**, then follow the on-screen installer.

#### Step 3 — Install all dependencies inside the VM

Open a terminal inside the VM and run:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk git -y
pip3 install psutil requests
```

#### Step 4 — Clone and run

```bash
git clone https://github.com/yourusername/nexus-shell.git
cd nexus-shell
python3 shell_console_2026.py
```

The GUI window should appear inside your VM desktop.

> **Headless VM / No GUI?** If your VM has no desktop environment (server edition), install one first:
> ```bash
> sudo apt install ubuntu-desktop -y
> sudo reboot
> ```

---

### 🐍 Using a Virtual Environment (Recommended)

It's good practice to isolate project dependencies using a Python virtual environment.

```bash
# Create the virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate          # Linux / macOS / VM
venv\Scripts\activate             # Windows

# Install dependencies
pip install psutil requests

# Run the app
python shell_console_2026.py

# When done, deactivate
deactivate
```

---

### Login Credentials

| Field    | Value  |
|----------|--------|
| Username | `neha` |
| Password | `neha` |

> You can change the credentials by editing the `_do_login` method in the source code.

---

## 📦 Dependencies

| Package    | Purpose                        | Install           |
|------------|--------------------------------|-------------------|
| `psutil`   | System metrics & process info  | `pip install psutil` |
| `requests` | Weather API calls              | `pip install requests` |
| `tkinter`  | GUI framework (built-in)       | Bundled with Python |

---

## 🗂️ Project Structure

```
nexus-shell/
│
├── shell_console_2026.py   # Main application file
├── README.md               # This file
│
# Auto-generated at runtime:
├── ~/.shell_console_history.json   # Persistent command history
└── ~/.shell_console_notes.txt      # Persistent notes
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut     | Action                        |
|--------------|-------------------------------|
| `Enter`      | Execute command               |
| `↑` / `↓`   | Navigate command history      |
| `Tab`        | Autocomplete from history     |
| `Ctrl + L`   | Clear terminal output         |
| `Ctrl + H`   | Open history window           |

---

## 🛠️ Configuration

To change the weather city, edit the top of the file:
```python
CITY = "Dhaka"   # Change to your city
```

To change the API key for weather, replace:
```python
API_KEY = "your_openweathermap_api_key"
```

Get a free API key at [openweathermap.org](https://openweathermap.org/api).

---

## 🧭 Roadmap

- [ ] SSH session manager tab
- [ ] Multiple terminal tabs
- [ ] Custom theme picker
- [ ] Command aliases & macros
- [ ] Search within terminal output
- [ ] Script editor with syntax highlighting

---

## 🙏 Acknowledgements

- [OpenWeatherMap](https://openweathermap.org/) for the weather API
- [psutil](https://github.com/giampaolo/psutil) for system metrics
- Built as part of an Operating Systems course project

---

<div align="center">
Made with ⚡ by <strong>Neha</strong>
</div>
