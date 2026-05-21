import subprocess
import tkinter as tk
from tkinter import scrolledtext, ttk
import requests
import time
import webbrowser

API_KEY = "b4422f83630bdb505f11e7a115b6e862"  
CITY = "Dhaka"  
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"


command_explanations = {
    "File Management": {
        "ls": {"explanation": "Lists files and directories in the current directory.", "example": "ls"},
        "pwd": {"explanation": "Prints the current working directory.", "example": "pwd"},
        "cd": {"explanation": "Changes the directory to the specified path.", "example": "cd <directory_name>"},
        "mkdir": {"explanation": "Creates a new directory with the specified name.", "example": "mkdir <directory_name>"},
        "rmdir": {"explanation": "Removes an empty directory.", "example": "rmdir <directory_name>"},
        "rm": {"explanation": "Removes files or directories.", "example": "rm <file_name>"},
        "cp": {"explanation": "Copies files or directories from one location to another.", "example": "cp <source> <destination>"},
        "mv": {"explanation": "Moves or renames files or directories.", "example": "mv <source> <destination>"},
        "touch": {"explanation": "Creates an empty file with the specified name.", "example": "touch <file_name>"},
        "cat": {"explanation": "Concatenates and displays the content of files.", "example": "cat <file_name>"},
        "echo": {"explanation": "Displays a line of text or variable value.", "example": "echo <text>"},
        "find": {"explanation": "Searches for files in a directory hierarchy.", "example": "find <path> -name <file_name>"},
        "ln": {"explanation": "Creates hard or symbolic links between files.", "example": "ln -s <target> <link_name>"}
    },
    "Permissions and Ownership": {
        "chmod": {"explanation": "Changes file or directory permissions.", "example": "chmod 755 <file_name>"},
        "chown": {"explanation": "Changes file or directory owner and group.", "example": "chown <owner>:<group> <file_name>"},
        "chgrp": {"explanation": "Changes the group ownership of a file or directory.", "example": "chgrp <group_name> <file_name>"}
    },
    "System Information": {
        "ps": {"explanation": "Shows the running processes on the system.", "example": "ps aux"},
        "top": {"explanation": "Displays system resource usage and processes in real-time.", "example": "top"},
        "free": {"explanation": "Displays memory usage on the system.", "example": "free -h"},
        "uptime": {"explanation": "Shows how long the system has been running and its load averages.", "example": "uptime"},
        "df": {"explanation": "Displays disk space usage of the file system.", "example": "df -h"},
        "du": {"explanation": "Estimates file space usage.", "example": "du -sh <directory>"},
        "hostname": {"explanation": "Displays or sets the system’s hostname.", "example": "hostname"},
        "date": {"explanation": "Displays or sets the system date and time.", "example": "date"},
        "whoami": {"explanation": "Displays the current user.", "example": "whoami"},
        "dmesg": {"explanation": "Displays kernel-related messages.", "example": "dmesg | tail"}
    },
    "Networking": {
        "ping": {"explanation": "Sends ICMP echo requests to network hosts to check their availability.", "example": "ping <hostname>"},
        "ifconfig": {"explanation": "Displays or configures network interfaces.", "example": "ifconfig"},
        "netstat": {"explanation": "Displays network connections, routing tables, and interface statistics.", "example": "netstat -tuln"},
        "curl": {"explanation": "Transfers data to or from a server using various protocols.", "example": "curl <url>"},
        "wget": {"explanation": "Downloads files from the internet.", "example": "wget <url>"},
        "scp": {"explanation": "Securely copies files between hosts over SSH.", "example": "scp <source> <user@host>:<destination>"},
        "ssh": {"explanation": "Securely connects to a remote machine over the SSH protocol.", "example": "ssh <user@host>"},
        "traceroute": {"explanation": "Traces the route packets take to reach a network host.", "example": "traceroute <hostname>"}
    },
    "Package Management": {
        "apt": {"explanation": "A package management tool for installing software on Debian-based systems.", "example": "apt update && apt upgrade"},
        "yum": {"explanation": "A package management tool for installing software on RedHat-based systems.", "example": "yum install <package_name>"},
        "pip": {"explanation": "Installs and manages Python packages.", "example": "pip install <package_name>"},
        "brew": {"explanation": "A package manager for macOS and Linux.", "example": "brew install <package_name>"}
    },
    "Archiving and Compression": {
        "tar": {"explanation": "Compresses or extracts files from tar archives.", "example": "tar -cvf <archive_name.tar> <files>"},
        "zip": {"explanation": "Compresses files into a zip archive.", "example": "zip <archive_name.zip> <files>"},
        "unzip": {"explanation": "Extracts files from a zip archive.", "example": "unzip <archive_name.zip>"},
        "gzip": {"explanation": "Compresses files using the Gzip compression algorithm.", "example": "gzip <file_name>"},
        "gunzip": {"explanation": "Decompresses files compressed by Gzip.", "example": "gunzip <file_name.gz>"},
        "xz": {"explanation": "Compresses files using the LZMA compression algorithm.", "example": "xz <file_name>"},
        "bzip2": {"explanation": "Compresses files using the Bzip2 compression algorithm.", "example": "bzip2 <file_name>"}
    },
    "Process Management": {
        "kill": {"explanation": "Sends a signal to terminate a process.", "example": "kill <process_id>"},
        "killall": {"explanation": "Kills all processes with a specific name.", "example": "killall <process_name>"},
        "bg": {"explanation": "Resumes suspended jobs in the background.", "example": "bg <job_id>"},
        "fg": {"explanation": "Brings a background job to the foreground.", "example": "fg <job_id>"},
        "jobs": {"explanation": "Lists active jobs.", "example": "jobs"},
        "nohup": {"explanation": "Runs a command immune to hangups, with output to a non-tty.", "example": "nohup <command> &"}
    },
    "System Control": {
        "sudo": {"explanation": "Runs a command with superuser (root) privileges.", "example": "sudo <command>"},
        "shutdown": {"explanation": "Shuts down the system.", "example": "shutdown -h now"},
        "reboot": {"explanation": "Reboots the system.", "example": "reboot"},
        "halt": {"explanation": "Stops all processes and halts the system.", "example": "halt"},
        "systemctl": {"explanation": "Controls system services.", "example": "systemctl <command>"}
    },
    "Logs and Monitoring": {
        "journalctl": {"explanation": "Views logs from the systemd journal.", "example": "journalctl -xe"},
        "tail": {"explanation": "Displays the last part of a file.", "example": "tail -n 10 <file_name>"},
        "head": {"explanation": "Displays the first part of a file.", "example": "head -n 10 <file_name>"},
        "watch": {"explanation": "Runs a command repeatedly at fixed intervals.", "example": "watch -n 2 <command>"},
        "htop": {"explanation": "Interactive process viewer.", "example": "htop"}
    }
}



def fetch_weather():
    try:
        response = requests.get(URL)
        print(f"Response Status Code: {response.status_code}")  
        data = response.json()
        print(f"Response Data: {data}")  
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"].capitalize()
            weather_label.config(text=f"Weather: {weather}, {temp}°C")
        else:
            weather_label.config(text="Weather: Unable to fetch data")
    except Exception as e:
        weather_label.config(text=f"Weather: Error ({str(e)})")
    root.after(600000, fetch_weather)


def execute_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr
    except Exception as e:
        return f"Error: {e}"

def explain_command(cmd):
    category = category_combobox.get()
    return command_explanations.get(category, {}).get(cmd, "No explanation available for this command.")


def run_command():
    command = command_entry.get() or command_combobox.get()
    if command:
        explanation_text.set(explain_command(command))
        output = execute_command(command)
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, output)
        output_box.config(fg="red" if "Error" in output else "black")
        history.append(command)


def clear_output():
    output_box.delete(1.0, tk.END)
    explanation_text.set("")

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Command History")
    history_window.config(bg="#FFB6C1")  
    tk.Label(history_window, text="Command History", bg="#FFB6C1", fg="#2E4053").pack(pady=5)  # Dark text color
    history_listbox = tk.Listbox(history_window, width=50, height=15, bg="#F0F8FF", fg="#2E4053")
    history_listbox.pack(pady=10)
    for cmd in history:
        history_listbox.insert(tk.END, cmd)


def show_category_commands(event):
    selected_category = category_combobox.get()
    commands = list(command_explanations.get(selected_category, {}).keys())
    command_combobox['values'] = commands
    command_combobox.set('')


def update_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=f"Clock: {current_time}")
    root.after(1000, update_clock)


def open_link(url): 
    webbrowser.open(url)


def open_youtube():
    youtube_url = "https://www.youtube.com"
    open_link(youtube_url)

def open_spotify():
    spotify_url = "https://www.spotify.com"
    open_link(spotify_url)


def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "neha" and password == "neha":  
        login_window.destroy()
        open_console()
    else:
        error_label.config(text="Invalid credentials, try again.")


    
def open_console():
    global root, command_entry, command_combobox, category_combobox, explanation_text, weather_label, clock_label, output_box, history
    history = []

    
    root = tk.Tk()
    root.title("Shell Command Console")
    root.geometry("800x600")
    root.config(bg="#FFFAF0")

    
    frame = tk.Frame(root, bg="#FFFAF0")
    frame.pack(pady=10)

    
    tk.Label(frame, text="Category:", bg="#FFFAF0", fg="#2E4053").grid(row=0, column=0, padx=5)  # Dark text color
    category_combobox = ttk.Combobox(frame, values=list(command_explanations.keys()), state="readonly", width=20)
    category_combobox.grid(row=0, column=1, padx=5)
    category_combobox.bind("<<ComboboxSelected>>", show_category_commands)

    tk.Label(frame, text="Command:", bg="#FFFAF0", fg="#2E4053").grid(row=0, column=2, padx=5)  # Dark text color
    command_combobox = ttk.Combobox(frame, state="readonly", width=20)
    command_combobox.grid(row=0, column=3, padx=5)
    
    tk.Label(frame, text="Or Enter Command:", bg="#FFFAF0", fg="#2E4053").grid(row=1, column=0, padx=5)
    command_entry = tk.Entry(frame, width=50)
    command_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=10)

    
    tk.Button(frame, text="Run", command=run_command).grid(row=2, column=1, pady=5)
    tk.Button(frame, text="Clear", command=clear_output).grid(row=2, column=2, pady=5)
    tk.Button(frame, text="History", command=show_history).grid(row=2, column=3, pady=5)

    tk.Label(root, text="Bored?? Refreshments for you!!", bg="#f2f2f2", font=("Arial", 14, "bold"), fg="blue").pack(pady=10)

    button_width = 20 
    tk.Button(root, text="Open YouTube", command=open_youtube).pack(pady=5)
    tk.Button(root, text="Open Spotify", command=open_spotify).pack(pady=5)

    explanation_text = tk.StringVar()
    explanation_label = tk.Label(root, textvariable=explanation_text, bg="#FFFAF0", fg="#2E4053", wraplength=600, justify="left")
    explanation_label.pack(pady=10)


    output_box = scrolledtext.ScrolledText(root, width=90, height=20, bg="#F0F8FF", fg="#2E4053")
    output_box.pack(pady=10)

    
    weather_label = tk.Label(root, text="", bg="#FFFAF0", fg="#2E4053")
    weather_label.pack()
    clock_label = tk.Label(root, text="", bg="#FFFAF0", fg="#2E4053")
    clock_label.pack()

    
    fetch_weather()
    update_clock()

   
    root.mainloop()



login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x300")
login_window.config(bg="#FFFAF0")


tk.Label(login_window, text="Username:", bg="#FFFAF0", fg="#2E4053").pack(pady=5)
username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

tk.Label(login_window, text="Password:", bg="#FFFAF0", fg="#2E4053").pack(pady=5)
password_entry = tk.Entry(login_window, show="*")
password_entry.pack(pady=5)

error_label = tk.Label(login_window, text="", bg="#FFFAF0", fg="red")
error_label.pack(pady=5)

tk.Button(login_window, text="Login", command=login, bg="#32CD32", fg="white").pack(pady=10)


login_window.mainloop()