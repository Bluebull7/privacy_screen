import tkinter as tk
from tkinter import ttk
import subprocess

# Function to apply gamma and brightness settings
def apply_settings():
    r = red_slider.get()
    g = green_slider.get()
    b = blue_slider.get()
    brightness = brightness_slider.get()
    try:
        subprocess.run(
            ["xrandr", "--output", display_name, "--gamma", f"{r}:{g}:{b}", "--brightness", f"{brightness}"],
            check=True
        )
        status_label.config(text=f"Settings applied: Gamma({r}:{g}:{b}), Brightness({brightness})")
    except subprocess.CalledProcessError:
        status_label.config(text="Error applying gamma/brightness settings.")

# Function to apply a preset
def apply_preset(event):
    preset = preset_var.get()
    r, g, b = gamma_presets[preset]
    red_slider.set(r)
    green_slider.set(g)
    blue_slider.set(b)
    apply_settings()

# Function to reset to default settings
def reset_settings():
    try:
        subprocess.run(
            ["xrandr", "--output", display_name, "--gamma", "1.0:1.0:1.0", "--brightness", "1.0"],
            check=True
        )
        red_slider.set(1.0)
        green_slider.set(1.0)
        blue_slider.set(1.0)
        brightness_slider.set(1.0)
        status_label.config(text="Settings reset to default (Gamma: 1.0:1.0:1.0, Brightness: 1.0)")
    except subprocess.CalledProcessError:
        status_label.config(text="Error resetting settings.")

# Get display name
def get_display_name():
    try:
        result = subprocess.run(["xrandr", "--query"], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if " connected" in line:
                return line.split()[0]
    except subprocess.CalledProcessError:
        return None

# Predefined gamma presets
gamma_presets = {
    "Default (1.0:1.0:1.0)": (1.0, 1.0, 1.0),
    "Desaturated and Dim (0.4:0.4:0.4)": (0.4, 0.4, 0.4),
    "Green-Heavy Tint (0.4:0.7:0.4)": (0.4, 0.7, 0.4),
    "Red-Heavy Tint (0.7:0.4:0.4)": (0.7, 0.4, 0.4),
    "Blue-Heavy Tint (0.4:0.4:0.7)": (0.4, 0.4, 0.7),
    "High Contrast Reduction (0.3:0.6:0.3)": (0.3, 0.6, 0.3),
    "Extreme Color Imbalance (0.1:0.6:0.1)": (0.1, 0.6, 0.1),
    "Warped Gamma (2.5:0.3:0.2)": (2.5, 0.3, 0.2),
}

# Initialize the application
root = tk.Tk()
root.title("Gamma and Brightness Adjustment Tool")

# Get display name
display_name = get_display_name()
if not display_name:
    tk.messagebox.showerror("Error", "Could not detect display name. Ensure xrandr is installed.")
    root.destroy()

# Preset dropdown
preset_var = tk.StringVar()
preset_label = tk.Label(root, text="Gamma Presets:")
preset_label.pack(pady=5)
preset_menu = ttk.Combobox(root, textvariable=preset_var, values=list(gamma_presets.keys()), state="readonly")
preset_menu.bind("<<ComboboxSelected>>", apply_preset)
preset_menu.pack(pady=5)

# Sliders for gamma adjustment
red_slider = tk.Scale(root, from_=0.1, to=3.0, resolution=0.1, label="Red", orient="horizontal")
red_slider.set(1.0)
red_slider.pack(pady=5)

green_slider = tk.Scale(root, from_=0.1, to=3.0, resolution=0.1, label="Green", orient="horizontal")
green_slider.set(1.0)
green_slider.pack(pady=5)

blue_slider = tk.Scale(root, from_=0.1, to=3.0, resolution=0.1, label="Blue", orient="horizontal")
blue_slider.set(1.0)
blue_slider.pack(pady=5)

# Brightness slider
brightness_slider = tk.Scale(root, from_=0.1, to=1.0, resolution=0.1, label="Brightness", orient="horizontal")
brightness_slider.set(1.0)
brightness_slider.pack(pady=5)

# Apply button
apply_button = tk.Button(root, text="Apply Settings", command=apply_settings)
apply_button.pack(pady=10)

# Reset button
reset_button = tk.Button(root, text="Reset Settings", command=reset_settings)
reset_button.pack(pady=5)

# Status label
status_label = tk.Label(root, text="Adjust gamma and brightness settings or select a preset.")
status_label.pack(pady=10)

# Run the application
root.mainloop()
