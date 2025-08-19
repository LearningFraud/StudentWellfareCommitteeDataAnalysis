import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def quit_app():
    sys.exit()

def get_screen_geometry(window):
    window.update_idletasks()
    return window.winfo_screenwidth(), window.winfo_screenheight()

def scale_font(base_ratio, screen_height, max_size=24):
    return min(int(screen_height * base_ratio), max_size)

def add_navigation_buttons(parent, logo_path, current_window):
    nav_frame = tk.Frame(parent, bg="#00a8eb")
    nav_frame.pack(side='bottom', fill='x', pady=10)

    tk.Button(nav_frame, text="Back to Home",
              command=lambda: homePage(logo_path, current_window)).pack(side='left', padx=20)
    tk.Button(nav_frame, text="Exit", command=quit_app).pack(side='right', padx=20)

def load_scaled_logo(path, screen_height, scale_factor=0.15):
    img = Image.open(path)
    new_height = int(screen_height * scale_factor)
    aspect_ratio = img.width / img.height
    new_width = int(new_height * aspect_ratio)
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized_img)


def homePage(logo_path, prev_window=None):
    if prev_window:
        prev_window.destroy()

    home_window = tk.Toplevel()
    home_window.title("GHS SRC - Correlation Survey Homepage")
    home_window.configure(bg="#00a8eb")

    screen_width, screen_height = get_screen_geometry(home_window)
    home_window.geometry(f"{screen_width}x{screen_height}")

    logo_img = load_scaled_logo(logo_path, screen_height)
    logo_label = tk.Label(home_window, image=logo_img, bg="#00a8eb")
    logo_label.image = logo_img
    logo_label.pack(pady=int(screen_height * 0.02))

    title_font = scale_font(0.03, screen_height)
    desc_font = scale_font(0.02, screen_height)

    tk.Label(home_window, text="Welcome to the GHS SRC\nCorrelation Survey Homepage",
             font=("Helvetica", title_font, "bold"), fg="white", bg="#00a8eb").pack(pady=int(screen_height * 0.03))

    tk.Label(home_window, text="Links to other pages can be found here.\nThis is the landing portal for the UI.",
             font=("Helvetica", desc_font), fg="white", bg="#00a8eb").pack(pady=int(screen_height * 0.02))

    for text, command in [("Go to Menu", lambda: open_menu(logo_path, home_window)), ("Exit", quit_app)]:
        tk.Button(home_window, text=text, font=("Helvetica", desc_font), command=command).pack(pady=int(screen_height * 0.015))

def open_menu(logo_path, home_window):
    home_window.destroy()
    menu_window = tk.Toplevel()
    menu_window.title("Page Selection")
    menu_window.configure(bg="#00a8eb")

    screen_width, screen_height = get_screen_geometry(menu_window)
    menu_window.geometry(f"{screen_width}x{screen_height}")
    font_size = scale_font(0.025, screen_height)

    tk.Label(menu_window, text="Select a page to continue", font=("Helvetica", font_size), bg="#00a8eb").pack(pady=int(screen_height * 0.03))

    for text, command in [("Data Page", lambda: dataPage(logo_path, menu_window)),
                          ("Project Page", lambda: projectPage(logo_path, menu_window)),
                          ("Exit", quit_app)]:
        tk.Button(menu_window, text=text, font=("Helvetica", font_size), command=command).pack(pady=int(screen_height * 0.02))

def dataPage(logo_path, menu_window):
    menu_window.destroy()
    data_window = tk.Toplevel()
    data_window.title("Data Menu")
    data_window.configure(bg="#00a8eb")

    screen_width, screen_height = get_screen_geometry(data_window)
    data_window.geometry(f"{screen_width}x{screen_height}")
    font_size = scale_font(0.025, screen_height)

    tk.Label(data_window, text="What Kind Of Data Do You Need?", bg="#00a8eb", font=("Helvetica", font_size)).pack(pady=int(screen_height * 0.03))

    for text, command in [("Home Page", lambda: homePage(logo_path, data_window)),
                          ("Data Visualisation", lambda: dataVisPage(logo_path, data_window)),
                          ("Raw Data", lambda: rawDataPage(logo_path, data_window)),
                          ("Exit", quit_app)]:
        tk.Button(data_window, text=text, font=("Helvetica", font_size), command=command).pack(pady=int(screen_height * 0.02))

def rawDataPage(logo_path, prev_window):
    prev_window.destroy()
    raw_data_window = tk.Toplevel()
    raw_data_window.title("Raw Data")
    raw_data_window.configure(bg="#00a8eb")

    screen_width, screen_height = get_screen_geometry(raw_data_window)
    raw_data_window.geometry(f"{screen_width}x{screen_height}")

    df = pd.read_csv("CleanedDataset-Manual.csv")
    if "Timestamp" in df.columns:
        df = df.drop(columns=["Timestamp"])

    tree = ttk.Treeview(raw_data_window)
    tree.pack(fill='both', expand=True)

    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    for text, command in [("Back to Home", lambda: homePage(logo_path, raw_data_window)), ("Exit", quit_app)]:
        tk.Button(raw_data_window, text=text, command=command).pack(pady=int(screen_height * 0.015))

def dataVisPage(logo_path, prev_window):
    prev_window.destroy()
    data_vis_window = tk.Toplevel()
    data_vis_window.title("Data Visualisation")
    data_vis_window.configure(bg="#00a8eb")

    screen_width, screen_height = get_screen_geometry(data_vis_window)
    data_vis_window.geometry(f"{screen_width}x{screen_height}")
    font_size = scale_font(0.03, screen_height)

    tk.Label(data_vis_window, text="Data Visualisation", bg="#00a8eb", font=("Helvetica", font_size)).pack(pady=int(screen_height * 0.03))
    showData(data_vis_window)

    for text, command in [("Back to Home", lambda: homePage(logo_path, data_vis_window)), ("Exit", quit_app)]:
        tk.Button(data_vis_window, text=text, command=command).pack(pady=int(screen_height * 0.015))
    add_navigation_buttons(data_vis_window, logo_path, data_vis_window)


def projectPage(logo_path, menu_window):
    menu_window.destroy()
    project_window = tk.Toplevel()
    project_window.title("Project Information")
    project_window.configure(bg="#00a8eb")

    screen_width, screen_height = get_screen_geometry(project_window)
    project_window.geometry(f"{screen_width}x{screen_height}")
    font_size = scale_font(0.03, screen_height)

    tk.Label(project_window, text="Project Information", bg="#00a8eb", font=("Helvetica", font_size)).pack(pady=int(screen_height * 0.03))
    tk.Label(project_window, text="This project is about analyzing student learning data.", bg="#00a8eb").pack(pady=int(screen_height * 0.02))

    for text, command in [("Project Overview", lambda: showNotebook("Overview.ipynb", logo_path, project_window)),
                          ("Project Journal", lambda: showNotebook("ProjectJournal.ipynb", logo_path, project_window)),
                          ("Back to Home", lambda: homePage(logo_path, project_window)),
                          ("Exit", quit_app)]:
        tk.Button(project_window, text=text, command=command).pack(pady=int(screen_height * 0.015))

def showNotebook(filename, logo_path, prev_window):
    prev_window.destroy()
    nb_window = tk.Toplevel()
    nb_window.title(filename)

    screen_width, screen_height = get_screen_geometry(nb_window)
    nb_window.geometry(f"{screen_width}x{screen_height}")

    text_frame = tk.Frame(nb_window)
    text_frame.pack(fill='both', expand=True)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side='right', fill='y')

    text_widget = tk.Text(text_frame, wrap='word', yscrollcommand=scrollbar.set, font=("Courier", 11))
    text_widget.pack(fill='both', expand=True)
    scrollbar.config(command=text_widget.yview)

    with open(filename, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    for cell in notebook.get("cells", []):
        if cell["cell_type"] == "markdown":
            text_widget.insert("end", "\n--- Markdown Cell ---\n", "bold")
            text_widget.insert("end", "".join(cell["source"]) + "\n\n")
        elif cell["cell_type"] == "code":
            text_widget.insert("end", "\n--- Code Cell ---\n", "bold")
            text_widget.insert("end", "".join(cell["source"]) + "\n\n")
    text_widget.tag_config("bold", font=("Courier", 11, "bold"))

    for text, command in [("Back to Home", lambda: homePage(logo_path, nb_window)), ("Exit", quit_app)]:
        tk.Button(nb_window, text=text, command=command).pack(pady=int(screen_height * 0.015))

def showData(parent_window):
    data = pd.read_csv('CleanedDataset-Manual.csv')
    data['RoomDecor'] = pd.to_numeric(data['RoomDecor'], errors='coerce')
    data['RoomLearn'] = pd.to_numeric(data['RoomLearn'], errors='coerce')
    data = data.dropna(subset=['RoomDecor', 'RoomLearn'])

    x = data['RoomLearn']
    y = data['RoomDecor']
    r, p = pearsonr(x, y)

    fig = Figure(figsize=(8, 8), dpi=100)
    ax = fig.add_subplot(111)

    hist = ax.hist2d(x, y, bins=[10, 10], cmap='Blues')
    fig.colorbar(hist[3], ax=ax, label='Frequency')

    ax.scatter(x, y, color='white', edgecolor='black', alpha=0.6)

    ax.add_patch(plt.Rectangle((5, 5), 5, 5, linewidth=2, edgecolor='cyan',
                               facecolor='none', linestyle='--'))

    ax.text(0.02, 0.98, f"Pearson r = {r:.3f}\nP-value = {p:.3f}",
            transform=ax.transAxes, fontsize=11,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='black', alpha=0.8))

    interpretation_text = (
        "Hypothesized zone (5,5 to 10,10)\n"
        "may indicate clustering or behavioral significance.\n"
        "• Weak correlation\n"
        "• Not statistically significant (p ≥ 0.05)"
    )
    ax.text(0.02, 0.02, interpretation_text,
            transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='black', alpha=0.8))

    ax.set_xlabel('Student Learning (10 = fully understands content)', fontsize=12)
    ax.set_ylabel('Room Decoration (1 = no markers, 10 = style-level artwork)', fontsize=12)
    ax.set_title('Overlay of Scatter Plot and 2D Histogram\nCorrelation Between Room Decoration and Student Learning', fontsize=14)
    ax.grid(False)

    canvas = FigureCanvasTkAgg(fig, master=parent_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

# 🔰 Entry Point
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide root window

    logo_path = "GHSLogo.png"  # Path to your logo image

    homePage(logo_path)
    root.mainloop()
