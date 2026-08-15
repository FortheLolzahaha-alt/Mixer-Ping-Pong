import os
import platform
import subprocess
import ctypes
import webbrowser
import time
import random
import threading
import sys

# --- Configuration ---
image_filename = "omg.jpg"
image_path = os.path.abspath(image_filename)

url = "https://www.youtube.com/watch?v=9qlRN4WWf5w"
total_iterations = 200
delay_seconds = 1
file_name = "im-inside-your-pc.txt"

# Phrases for Text-to-Speech
tts_phrases = [
    "Subscribe to Tranium",
    "i love you Tranium",
    "this is fun right?"
]


# --- Windows C Structure for Mouse Coordinates ---
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


# --- Helper Function: Change Desktop Wallpaper ---
def set_wallpaper(path):
    system = platform.system()
    if system == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
    elif system == "Darwin":  # macOS
        script = f'tell application "Finder" to set desktop picture to POSIX file "{path}"'
        subprocess.run(["osascript", "-e", script])
    elif system == "Linux":  # GNOME
        subprocess.run([
            "gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{path}"
        ])


# --- Helper Function: Launch a Random Application ---
def open_random_app():
    system = platform.system()
    if system == "Windows":
        apps = ["calc.exe", "notepad.exe", "mspaint.exe", "explorer.exe", "write.exe"]
        subprocess.Popen([random.choice(apps)])
    elif system == "Darwin":
        apps = ["Calculator", "TextEdit", "Notes", "Preview"]
        subprocess.Popen(["open", "-a", random.choice(apps)])
    elif system == "Linux":
        apps = ["gnome-calculator", "gedit", "xterm"]
        subprocess.Popen([random.choice(apps)])


# --- Helper Function: Run 'asd' Python Script ---
def run_asd_script():
    # Automatically finds asd.py (or asd) and runs it using the current Python interpreter
    target = "asd.py" if os.path.exists("asd.py") else "asd"
    subprocess.Popen([sys.executable, target])


# --- Helper Function: Show Error Dialog ---
def show_error_message():
    system = platform.system()
    if system == "Windows":
        # 0x10 is the system code for MB_ICONERROR (Red X symbol)
        ctypes.windll.user32.MessageBoxW(0, "this is fun right?", "Fatal Error", 0x10)
    elif system == "Darwin":
        script = 'display dialog "this is fun right?" with icon stop buttons {"OK"} default button "OK"'
        subprocess.run(["osascript", "-e", script])
    elif system == "Linux":
        subprocess.run(["zenity", "--error", "--text=this is fun right?"])

def spawn_error_thread():
    # Spawns the error box in a separate thread so it doesn't block the loop
    threading.Thread(target=show_error_message, daemon=True).start()


# --- Feature 1: Text-to-Speech (Non-blocking) ---
def speak(text):
    system = platform.system()
    def _speak():
        if system == "Windows":
            cmd = f"Add-Type -AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.Speak('{text}')"
            subprocess.run(["powershell", "-Command", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif system == "Darwin":
            subprocess.run(["say", text])
        elif system == "Linux":
            subprocess.run(["spd-say", text])
            
    threading.Thread(target=_speak, daemon=True).start()


# --- Feature 2: Master Volume Spike (100%) ---
def max_volume():
    system = platform.system()
    if system == "Windows":
        # Send 50 VK_VOLUME_UP key events to max out master volume
        VK_VOLUME_UP = 0xAF
        for _ in range(50):
            ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 2, 0)
    elif system == "Darwin":
        subprocess.run(["osascript", "-e", "set volume output volume 100"])
    elif system == "Linux":
        subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "100%"])


# --- Feature 4: Ghost Mouse Cursor Movement ---
def nudge_mouse():
    system = platform.system()
    if system == "Windows":
        pt = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        dx = random.randint(-20, 20)
        dy = random.randint(-20, 20)
        ctypes.windll.user32.SetCursorPos(pt.x + dx, pt.y + dy)
    elif system == "Linux":
        subprocess.run(["xdotool", "mousemove_relative", "--", str(random.randint(-20, 20)), str(random.randint(-20, 20))])


# --- Feature 5: Keyboard Toggles (Caps Lock / Num Lock Rave) ---
def toggle_keyboard_lock():
    system = platform.system()
    if system == "Windows":
        # 0x14 = Caps Lock, 0x90 = Num Lock
        key = random.choice([0x14, 0x90])
        ctypes.windll.user32.keybd_event(key, 0, 0, 0)
        ctypes.windll.user32.keybd_event(key, 0, 2, 0)
    elif system == "Darwin":
        script = 'tell application "System Events" to key code 57'
        subprocess.run(["osascript", "-e", script])
    elif system == "Linux":
        subprocess.run(["xdotool", "key", "Caps_Lock"])


# --- Part 1: Change Wallpaper ---
if os.path.exists(image_path):
    set_wallpaper(image_path)
    print(f"Wallpaper changed using '{image_filename}'")
else:
    print(f"Notice: '{image_filename}' not found. Skipping wallpaper change.")


# --- Part 2: Create and Open Text File ---
with open(file_name, "w") as file:
    file.write("i love you :3")

if platform.system() == 'Windows':
    os.startfile(file_name)
elif platform.system() == 'Darwin':
    subprocess.call(('open', file_name))
else:
    subprocess.call(('xdg-open', file_name))


# --- Part 3: Main Automation Loop ---
print("Starting loop...")

for i in range(1, total_iterations + 1):
    # Randomly pick an action to perform during this iteration
    action = random.choice(["browser", "app", "error", "tts", "ghost_mouse", "caps_rave", "run_script"])
    
    if action == "browser":
        max_volume()
        webbrowser.open(url)
        print(f"[{i}/{total_iterations}] ")

    elif action == "app":
        open_random_app()
        print(f"[{i}/{total_iterations}] ")

    elif action == "run_script":
        run_asd_script()
        print(f"[{i}/{total_iterations}] ")

    elif action == "error":
        spawn_error_thread()
        print(f"[{i}/{total_iterations}] ")

    elif action == "tts":
        phrase = random.choice(tts_phrases)
        speak(phrase)
        print(f"[{i}/{total_iterations}] Spoke phrase: '{phrase}'")

    elif action == "ghost_mouse":
        nudge_mouse()
        print(f"[{i}/{total_iterations}] ")

    elif action == "caps_rave":
        toggle_keyboard_lock()
        print(f"[{i}/{total_iterations}] ")
        
    time.sleep(delay_seconds)

print("Dont go pls :(")
