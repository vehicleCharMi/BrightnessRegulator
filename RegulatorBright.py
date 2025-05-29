import tkinter as tk
import subprocess

def set_brightness(value):
    brightness = float(value) / 100
    subprocess.run(["xrandr", "--output", output_name, "--brightness", str(brightness)])
    label.config(text=f"Brightness: {int(float(value))}%")

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
    root = tk.Tk()
    root.title("Brightness Controller")

    # Убираем параметры прозрачности и безрамочности
    root.configure(bg="black")

    # Центрирование окна
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 300
    window_height = 120
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Ярлык яркости
    global label
    label = tk.Label(root, text="Brightness: 100%", font=("Arial", 14), fg="white", bg="black")
    label.pack(pady=(15, 5))

    # Слайдер
    slider = tk.Scale(
        root, from_=10, to=100,
        orient="horizontal", length=250,
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

    # Закрытие по Esc
    root.bind("<Escape>", lambda e: root.destroy())

    root.mainloop()

if __name__ == "__main__":
    create_ui()
