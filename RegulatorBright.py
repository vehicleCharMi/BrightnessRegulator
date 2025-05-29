import tkinter as tk
import subprocess

MIN_BRIGHTNESS = 10

def disable_auto_dim():
    try:
        subprocess.run(["gsettings", "set", "org.gnome.settings-daemon.plugins.power", "idle-dim", "false"])
        subprocess.run(["gsettings", "set", "org.gnome.settings-daemon.plugins.power", "brightness-dim-battery", "false"])
        subprocess.run(["gsettings", "set", "org.gnome.settings-daemon.plugins.power", "ambient-enabled", "false"])
    except Exception as e:
        print("Failed to disable auto dimming:", e)

def set_brightness(value):
    val = max(float(value), MIN_BRIGHTNESS)
    brightness = val / 100
    subprocess.run(["xrandr", "--output", output_name, "--brightness", str(brightness)])
    slider.set(val)
    label.config(text=f"Brightness: {int(val)}%")

def get_primary_output():
    result = subprocess.run(["xrandr"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if " connected primary" in line:
            return line.split()[0]
    for line in result.stdout.splitlines():
        if " connected" in line:
            return line.split()[0]
    return None

output_name = get_primary_output()
if output_name is None:
    print("No display detected.")
    exit(1)

def create_ui():
    global slider, label

    disable_auto_dim()

    root = tk.Tk()
    root.title("Brightness Controller")
    root.configure(bg="black")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 320
    window_height = 160
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    label = tk.Label(root, text="Brightness: 100%", font=("Arial", 14), fg="white", bg="black")
    label.pack(pady=(15, 5))

    slider = tk.Scale(
        root, from_=MIN_BRIGHTNESS, to=100,
        orient="horizontal", length=280,
        command=set_brightness,
        showvalue=False,
        troughcolor="#444",
        fg="white",
        bg="black",
        highlightthickness=0,
        sliderlength=20,
    )
    slider.set(100)
    slider.pack()

    root.bind("<Escape>", lambda e: root.destroy())
    root.mainloop()

if __name__ == "__main__":
    create_ui()
