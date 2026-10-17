import tkinter as tk
from tkinter import ttk
import subprocess
import os

def launch_app(app_name, app_command):
    try:
        env = os.environ.copy()
        env["DISPLAY"] = ":0"
        subprocess.Popen(app_command, env=env)
        status_label.config(text=f"🚀 Running: {app_name}", fg="#E95420")
    except Exception as e:
        status_label.config(text=f"❌ Error: {e}", fg="#DF382C")

# Path to the standalone MP3 player sitting right next to this file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MP3_PLAYER_PATH = os.path.join(SCRIPT_DIR, "mp3_player.py")

# 1. Main Window Setup 
root = tk.Tk()
root.title("The Weber Desktop Subsystem")
root.geometry("620x420") 
root.config(cursor="arrow") 

# 2. THREE-COLOR BACKGROUND ENGINE
canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

def draw_three_color_gradient(event):
    canvas.delete("gradient")
    w = event.width
    h = event.height
    
    c1 = (44, 0, 30)      # #2C001E (Ubuntu Aubergine)
    c2 = (79, 24, 33)     # #4f1821 (Midpoint Red-Brown Accent)
    c3 = (233, 84, 32)    # #E95420 (Ubuntu Canonical Orange)
    
    for y in range(h):
        if y < h / 2:
            factor = y / (h / 2)
            r = int(c1[0] + (c2[0] - c1[0]) * factor)
            g = int(c1[1] + (c2[1] - c1[1]) * factor)
            b = int(c1[2] + (c2[2] - c1[2]) * factor)
        else:
            factor = (y - h / 2) / (h / 2)
            r = int(c2[0] + (c3[0] - c2[0]) * factor)
            g = int(c2[1] + (c3[1] - c2[1]) * factor)
            b = int(c2[2] + (c3[2] - c2[2]) * factor)
            
        color_hex = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, y, w, y, tags="gradient", fill=color_hex)
        
    canvas.lower("gradient")

canvas.bind("<Configure>", draw_three_color_gradient)

# 3. Transparent Layout Blocks Over the Canvas Grid
dock_frame = tk.Frame(canvas, bg="#111111", width=70)
dock_frame.pack(side="left", fill="y")
dock_frame.pack_propagate(False)

workspace_frame = tk.Frame(canvas, bg="#2C001E")
workspace_frame.pack(side="right", fill="both", expand=True, padx=25, pady=25)

# 4. Apply Ubuntu Yaru Style Rules
style = ttk.Style()
style.theme_use('clam')
style.configure("Dock.TButton", font=("Ubuntu", 16), foreground="#FFFFFF", background="#222222", padding=10, width=3, borderwidth=0)
style.map("Dock.TButton", background=[("active", "#E95420")])

# 5. LEFT DOCK SHORTCUT LAYOUT (The standalone applications sidebar launcher)
tk.Label(dock_frame, text=" Ubuntu", font=("Ubuntu", 8, "bold"), bg="#111111", fg="#AEA79F").pack(pady=(10, 15))

ttk.Button(dock_frame, text="🎵", style="Dock.TButton", command=lambda: launch_app("Music Player", ["python3", MP3_PLAYER_PATH])).pack(pady=6)
ttk.Button(dock_frame, text="🌐", style="Dock.TButton", command=lambda: launch_app("Firefox Browser", ["firefox"])).pack(pady=6)
ttk.Button(dock_frame, text="📝", style="Dock.TButton", command=lambda: launch_app("Text Editor", ["gedit"])).pack(pady=6)
ttk.Button(dock_frame, text="📁", style="Dock.TButton", command=lambda: launch_app("Files Explorer", ["nautilus"])).pack(pady=6)

# 6. WORKSPACE CONTENT
title_lbl = tk.Label(workspace_frame, text="The Weber desktop Core", font=("Ubuntu", 24, "bold"), fg="#FFFFFF", bg="#2C001E")
title_lbl.pack(anchor="w", pady=(0, 2))

# 7. LEFT DOCK SHORTCUT LAYOUT (The standalone applications sidebar launcher)
tk.Label(dock_frame, text=" Ubuntu", font=("Ubuntu", 8, "bold"), bg="#111111", fg="#AEA79F").pack(pady=(10, 15))

ttk.Button(dock_frame, text="🎵", style="Dock.TButton", command=lambda: launch_app("Music Player", ["python3", MP3_PLAYER_PATH])).pack(pady=6)

# UPDATED: Visual icon button map targeting the doom game file directly
ttk.Button(dock_frame, text="👹🎮", style="Dock.TButton", command=lambda: launch_app("Classic Doom", ["chocolate-doom", "-iwad", "/usr/share/games/doom/doom1.wad"])).pack(pady=6)

ttk.Button(dock_frame, text="🌐", style="Dock.TButton", command=lambda: launch_app("Firefox Browser", ["firefox"])).pack(pady=6)
ttk.Button(dock_frame, text="📝", style="Dock.TButton", command=lambda: launch_app("Text Editor", ["gedit"])).pack(pady=6)
ttk.Button(dock_frame, text="📁", style="Dock.TButton", command=lambda: launch_app("Files Explorer", ["nautilus"])).pack(pady=6)


sub_lbl = tk.Label(workspace_frame, text="Select an application shortcut icon from the launcher dock.", font=("Ubuntu", 10), fg="#AEA79F", bg="#2C001E")
sub_lbl.pack(anchor="w", pady=(0, 40))

# Bottom Status Metrics
status_label = tk.Label(workspace_frame, text="⚙️ System operational.", font=("Ubuntu", 9, "italic"), fg="#AEA79F", bg="#2C001E")
status_label.pack(side="bottom", anchor="w")

# Match child widget background rendering context to the base canvas parameters dynamically
def sync_bg(event):
    color_hex = "#2C001E" 
    workspace_frame.config(bg=color_hex)
    title_lbl.config(bg=color_hex)
    sub_lbl.config(bg=color_hex)
    status_label.config(bg=color_hex)

workspace_frame.bind("<Configure>", sync_bg)

root.mainloop()