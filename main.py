# GHS SRC - Correlation Survey UI
# This script provides a graphical user interface for the GHS SRC Correlation Survey project.
# It allows users to navigate through different pages, view data visualizations, and access project information.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import tkinter as tk
from tkinter import ttk
import json
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def quit_app():
    sys.exit()

def homePage(logo, prev_window=None):
    if prev_window:
        prev_window.destroy()

    home_window = tk.Toplevel()
    home_window.title("GHS SRC - Correlation Survey Homepage")
    home_window.configure(bg="#00a8eb")
    home_window.attributes('-fullscreen', True)
    home_window.iconphoto(False, logo)

    logo_label = tk.Label(home_window, image=logo, bg="#00a8eb")
    logo_label.image = logo
    logo_label.pack(pady=10)

    title = tk.Label(home_window, text="Welcome to the GHS SRC\nCorrelation Survey Homepage",
                     font=("Helvetica", 20, "bold"), fg="white", bg="#00a8eb")
    title.pack(pady=20)

    desc = tk.Label(home_window, text="Links to other pages can be found here.\nThis is the landing portal for the UI.",
                    font=("Helvetica", 12), fg="white", bg="#00a8eb")
    desc.pack(pady=10)

    tk.Button(home_window, text="Go to Menu", font=("Helvetica", 12),
              command=lambda: open_menu(logo, home_window)).pack(pady=15)
    tk.Button(home_window, text="Exit", font=("Helvetica", 12),
              command=quit_app).pack(pady=10)

def open_menu(logo, home_window):
    home_window.destroy()
    menu_window = tk.Toplevel()
    menu_window.title("Page Selection")
    menu_window.configure(bg="#00a8eb")
    menu_window.attributes('-fullscreen', True)
    menu_window.iconphoto(False, logo)

    tk.Label(menu_window, text="Select a page to continue", font=("Helvetica", 14), bg="#00a8eb").pack(pady=20)
    tk.Button(menu_window, text="Data Page", command=lambda: dataPage(logo, menu_window)).pack(pady=10)
    tk.Button(menu_window, text="Project Page", command=lambda: projectPage(logo, menu_window)).pack(pady=10)
    tk.Button(menu_window, text="Exit", command=quit_app).pack(pady=10)

def dataPage(logo, menu_window):
    menu_window.destroy()
    data_window = tk.Toplevel()
    data_window.title("Data Menu")
    data_window.configure(bg="#00a8eb")
    data_window.attributes('-fullscreen', True)
    data_window.iconphoto(False, logo)

    tk.Label(data_window, text="What Kind Of Data Do You Need?", bg="#00a8eb", font=("Helvetica", 20)).pack(pady=20)
    tk.Button(data_window, text="Home Page", command=lambda: homePage(logo, data_window)).pack(pady=10)
    tk.Button(data_window, text="Data Visualisation", command=lambda: dataVisPage(logo, data_window)).pack(pady=10)
    tk.Button(data_window, text="Raw Data", command=lambda: rawDataPage(logo, data_window)).pack(pady=10)
    tk.Button(data_window, text="Exit", command=quit_app).pack(pady=10)

def rawDataPage(logo, prev_window):
    prev_window.destroy()
    raw_data_window = tk.Toplevel()
    raw_data_window.title("Raw Data")
    raw_data_window.configure(bg="#00a8eb")
    raw_data_window.attributes('-fullscreen', True)
    raw_data_window.iconphoto(False, logo)

    df = pd.read_csv("CleanedDataset-Manual.csv")

    # 🧹 Drop the Timestamp column if it exists
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

    tk.Button(raw_data_window, text="Back to Home", command=lambda: homePage(logo, raw_data_window)).pack(pady=10)
    tk.Button(raw_data_window, text="Exit", command=quit_app).pack(pady=10)

def dataVisPage(logo, prev_window):
    prev_window.destroy()
    data_vis_window = tk.Toplevel()
    data_vis_window.title("Data Visualisation")
    data_vis_window.configure(bg="#00a8eb")
    data_vis_window.attributes('-fullscreen', True)
    data_vis_window.iconphoto(False, logo)

    tk.Label(data_vis_window, text="Data Visualisation", bg="#00a8eb", font=("Helvetica", 20)).pack(pady=20)
    showData(data_vis_window)
    tk.Button(data_vis_window, text="Back to Home", command=lambda: homePage(logo, data_vis_window)).pack(pady=10)
    tk.Button(data_vis_window, text="Exit", command=quit_app).pack(pady=10)

def projectPage(logo, menu_window):
    menu_window.destroy()
    project_window = tk.Toplevel()
    project_window.title("Project Information")
    project_window.configure(bg="#00a8eb")
    project_window.attributes('-fullscreen', True)
    project_window.iconphoto(False, logo)

    tk.Label(project_window, text="Project Information", bg="#00a8eb", font=("Helvetica", 20)).pack(pady=20)
    tk.Label(project_window, text="This project is about analyzing student learning data.", bg="#00a8eb").pack(pady=10)
    tk.Button(project_window, text="Project Overview", command=lambda: showOverview(logo, project_window)).pack(pady=10)
    tk.Button(project_window, text="Project Journal", command=lambda: showPJ(logo, project_window)).pack(pady=10)
    tk.Button(project_window, text="Back to Home", command=lambda: homePage(logo, project_window)).pack(pady=10)
    tk.Button(project_window, text="Exit", command=quit_app).pack(pady=10)

def showOverview(logo, prev_window):
    prev_window.destroy()
    nb_window = tk.Toplevel()
    nb_window.title("Project Overview")
    nb_window.geometry("800x600")
    nb_window.iconphoto(False, logo)

    text_frame = tk.Frame(nb_window)
    text_frame.pack(fill='both', expand=True)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side='right', fill='y')

    text_widget = tk.Text(text_frame, wrap='word', yscrollcommand=scrollbar.set, font=("Courier", 11))
    text_widget.pack(fill='both', expand=True)
    scrollbar.config(command=text_widget.yview)

    with open("Overview.ipynb", "r", encoding="utf-8") as f:
        notebook = json.load(f)

    for cell in notebook.get("cells", []):
        if cell["cell_type"] == "markdown":
            text_widget.insert("end", "\n--- Markdown Cell ---\n", "bold")
            text_widget.insert("end", "".join(cell["source"]) + "\n\n")
        elif cell["cell_type"] == "code":
            text_widget.insert("end", "\n--- Code Cell ---\n", "bold")
            text_widget.insert("end", "".join(cell["source"]) + "\n\n")

    text_widget.tag_config("bold", font=("Courier", 11, "bold"))
    tk.Button(nb_window, text="Back to Home", command=lambda: homePage(logo, nb_window)).pack(pady=10)
    tk.Button(nb_window, text="Exit", command=quit_app).pack(pady=10)

def showPJ(logo, prev_window):
    prev_window.destroy()
    nb_window = tk.Toplevel()
    nb_window.title("Project Journal")
    nb_window.geometry("800x600")
    nb_window.iconphoto(False, logo)

    text_frame = tk.Frame(nb_window)
    text_frame.pack(fill='both', expand=True)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side='right', fill='y')

    text_widget = tk.Text(text_frame, wrap='word', yscrollcommand=scrollbar.set, font=("Courier", 11))
    text_widget.pack(fill='both', expand=True)
    scrollbar.config(command=text_widget.yview)

    with open("ProjectJournal.ipynb", "r", encoding="utf-8") as f:
        notebook = json.load(f)

    for cell in notebook.get("cells", []):
        if cell["cell_type"] == "markdown":
            text_widget.insert("end", "\n--- Markdown Cell ---\n", "bold")
            text_widget.insert("end", "".join(cell["source"]) + "\n\n")
        elif cell["cell_type"] == "code":
            text_widget.insert("end", "\n--- Code Cell ---\n", "bold")
            text_widget.insert("end", "".join(cell["source"]) + "\n\n")

        text_widget.tag_config("bold", font=("Courier", 11, "bold"))
    tk.Button(nb_window, text="Back to Home", command=lambda: homePage(logo, nb_window)).pack(pady=10)
    tk.Button(nb_window, text="Exit", command=quit_app).pack(pady=10)

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

    logo = tk.PhotoImage(file="GHSLogo.png")  # ✅ Safe to load after root

    homePage(logo)
    root.mainloop()
