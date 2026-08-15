import ctypes
import random
import threading
import time
import tkinter as tk

# --- Windows API Setup for GDI Effects ---
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# Get screen resolution
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# GDI Raster Operation (ROP) codes
PATINVERT = 0x005A0049
SRCCOPY   = 0x00CC0020

# Screen redraw cleanup flags
RDW_INVALIDATE  = 0x0001
RDW_ERASE       = 0x0004
RDW_ALLCHILDREN = 0x0080
RDW_UPDATENOW   = 0x0100
CLEANUP_FLAGS   = RDW_INVALIDATE | RDW_ERASE | RDW_ALLCHILDREN | RDW_UPDATENOW

# Flag to signal threads to stop cleanly
stop_event = threading.Event()

def gdi_glitch_loop():
    """Background thread handling continuous GDI screen glitches."""
    while not stop_event.is_set():
        hdc = user32.GetDC(0)
        if hdc:
            # Random region coordinates
            x = random.randint(0, max(1, screen_width - 100))
            y = random.randint(0, max(1, screen_height - 100))
            w = random.randint(100, 400)
            h = random.randint(100, 400)

            # Invert colors
            gdi32.PatBlt(hdc, x, y, w, h, PATINVERT)

            # Shift screen pixels
            shift_x = x + random.randint(-20, 20)
            shift_y = y + random.randint(-20, 20)
            gdi32.BitBlt(hdc, shift_x, shift_y, w, h, hdc, x, y, SRCCOPY)

            user32.ReleaseDC(0, hdc)
        
        time.sleep(0.01)

    # Restore screen when exiting loop
    user32.RedrawWindow(0, None, None, CLEANUP_FLAGS)


def start_bouncing_ui():
    """Main thread handling the bouncing overlay window."""
    root = tk.Tk()
    root.title("Tranium")

    # Make window borderless and force it to stay on top
    root.overrideredirect(True)
    root.attributes("-topmost", True)

    win_width = 360
    win_height = 90

    # Initial position and bouncing velocity
    x = random.randint(50, max(51, screen_width - win_width - 50))
    y = random.randint(50, max(51, screen_height - win_height - 50))
    dx = 8
    dy = 8

    # Neon color palette for wall bounce highlights
    colors = ["#FF0055", "#00FFCC", "#FFCC00", "#9900FF", "#00FF00", "#FF6600"]
    color_idx = 0

    # UI Elements
    frame = tk.Frame(root, bg="black", highlightbackground=colors[0], highlightthickness=3)
    frame.pack(fill="both", expand=True)

    label = tk.Label(
        frame,
        text="Subscribe to Tranium",
        font=("Consolas", 18, "bold"),
        fg=colors[0],
        bg="black"
    )
    label.pack(expand=True, fill="both", padx=10, pady=10)

    def update_position():
        nonlocal x, y, dx, dy, color_idx

        x += dx
        y += dy
        bounced = False

        # Bounce off Left / Right edges
        if x <= 0:
            x = 0
            dx = -dx
            bounced = True
        elif x + win_width >= screen_width:
            x = screen_width - win_width
            dx = -dx
            bounced = True

        # Bounce off Top / Bottom edges
        if y <= 0:
            y = 0
            dy = -dy
            bounced = True
        elif y + win_height >= screen_height:
            y = screen_height - win_height
            dy = -dy
            bounced = True

        # Cycle color theme on edge collision
        if bounced:
            color_idx = (color_idx + 1) % len(colors)
            new_color = colors[color_idx]
            label.config(fg=new_color)
            frame.config(highlightbackground=new_color)

        root.geometry(f"{win_width}x{win_height}+{int(x)}+{int(y)}")
        root.after(10, update_position)

    def close_app(event=None):
        stop_event.set()
        root.destroy()

    # Press 'Escape' key anytime to close safely
    root.bind("<Escape>", close_app)

    # Start bounce loop
    update_position()
    root.mainloop()


if __name__ == "__main__":
    print("--------------------------------------------------")
    print("  'Subscribe to Tranium'  ")
    print("--------------------------------------------------")

    # Start GDI glitching in background thread
    glitch_thread = threading.Thread(target=gdi_glitch_loop, daemon=True)
    glitch_thread.start()

    try:
        start_bouncing_ui()
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()
        # Force screen redraw cleanup
        user32.RedrawWindow(0, None, None, CLEANUP_FLAGS)
        print("why did you leave? :(")