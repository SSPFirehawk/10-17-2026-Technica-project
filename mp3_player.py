import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import os
import sys

audio_process = None
current_file_path = ""

def select_file():
    global current_file_path
    # Opens a native file picker looking for MP3s
    file_path = filedialog.askopenfilename(
        title="Select an MP3 File",
        filetypes=[("Audio Files", "*.mp3"), ("All Files", "*.*")]
    )
    if file_path:
        current_file_path = file_path
        track_label.config(text=f"🎵 {os.path.basename(file_path)}", foreground="#1e90ff")
        status_label.config(text="Track loaded.", foreground="#2ed573")

def play_music():
    global audio_process, current_file_path
    if not current_file_path:
        status_label.config(text="Select an MP3 first!", foreground="#ff4757")
        return
    stop_music()
    try:
        # cvlc runs VLC in a headless command-line mode behind the scenes
        audio_process = subprocess.Popen(
            ["cvlc", "--play-and-exit", current_file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        status_label.config(text="▶ Playing...", foreground="#2ed573")
    except Exception as e:
        status_label.config(text=f"Playback Error: {e}", foreground="#ff4757")

def stop_music():
    global audio_process
    if audio_process and audio_process.poll() is None:
        audio_process.terminate()  # Safely stops the background music engine
        audio_process = None
        status_label.config(text="⏹ Stopped.", foreground="#57606f")

def safe_exit():
    stop_music()
    root.destroy()
    sys.exit(0)

# Window Setup
root = tk.Tk()
root.title("Linux Custom MP3 Player")
root.geometry("400x260")
root.configure(bg="#ffffff")
root.config(cursor="arrow")  # Keeps the mouse pointer visible
root.protocol("WM_DELETE_WINDOW", safe_exit)  # Safe closure hook

style = ttk.Style()
style.theme_use('clam')

main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill="both", expand=True)

title_label = ttk.Label(main_frame, text="WSL Audio Engine", font=("Helvetica", 14, "bold"))
title_label.pack(anchor="w", pady=(0, 10))

# Track Display Box
track_frame = ttk.Frame(main_frame, padding="10", relief="solid", borderwidth=1)
track_frame.pack(fill="x", pady=10)

track_label = ttk.Label(track_frame, text="No track selected", font=("Helvetica", 10, "italic"), foreground="#a4b0be")
track_label.pack(anchor="center")

# Media Buttons
controls_frame = ttk.Frame(main_frame)
controls_frame.pack(fill="x", pady=10)

ttk.Button(controls_frame, text="📁 Browse", command=select_file).pack(side="left", padx=2, expand=True, fill="x")
ttk.Button(controls_frame, text="▶ Play", command=play_music).pack(side="left", padx=2, expand=True, fill="x")
ttk.Button(controls_frame, text="⏹ Stop", command=stop_music).pack(side="left", padx=2, expand=True, fill="x")

# Status Footer
status_label = ttk.Label(main_frame, text="Ready.", font=("Helvetica", 10), foreground="#a4b0be")
status_label.pack(anchor="w", pady=(10, 0))

root.mainloop()
