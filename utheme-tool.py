import tkinter as tk
import os
import platform
from tkinter import ttk, filedialog, messagebox
from create_utheme import create_theme_archive

full_paths = {}
selected_patch_files = set()

def show_hint_dialog(hint_header, hint_body):
    messagebox.showinfo(hint_header, hint_body)

def remove_spaces(new_value):
    return " " not in new_value

def limit_characters(new_value, max_length):
    return len(new_value) <= int(max_length)

def on_scroll(event):
    if platform.system() == "Windows":
        canvas.yview_scroll(-1 * (event.delta // 120), "units")  # Windows scroll
    elif platform.system() == "Darwin":
        canvas.yview_scroll(-1 * event.delta, "units")  # Mac scroll
    #else:
        # Linux scrolling someday... (If someone wants to test this on linux hit me up)

def add_patch_fields():
    global patch_row_count, patch_header_count, patch_widgets
    row = patch_row_count
    patch_row_count += 4

    patch_header = f"Patch {patch_header_count}"
    patch_label = tk.Label(patch_frame, text=patch_header, font=("Arial", 10, "bold"))
    patch_label.grid(row=row, column=0, columnspan=2, pady=5)

    # BPS Section
    bps_label = tk.Label(patch_frame, text="Patch file:")
    bps_label.grid(row=row + 1, column=0, padx=5, sticky="w")
    bps_hint_button = tk.Button(patch_frame, text="?", command=lambda: show_hint_dialog("Info", "Select the path to a patch (.bps) file"), width=2, height=1, relief="solid", borderwidth=1)
    bps_hint_button.grid(row=row + 1, column=2, padx=5, pady=5, sticky="w")
    bps_button = tk.Button(patch_frame, text="Browse", command=lambda: browse_file(bps_button, relative_entry), height=2, width=25)
    bps_button.grid(row=row + 1, column=1, pady=5, padx=10, sticky="ew")

    # Original File Section
    original_label = tk.Label(patch_frame, text="Original file:")
    original_label.grid(row=row + 2, column=0, padx=5, sticky="w")
    original_hint_button = tk.Button(patch_frame, text="?", command=lambda: show_hint_dialog("Info", "Select the path to the original file that relates to the patch file"), width=2, height=1, relief="solid", borderwidth=1)
    original_hint_button.grid(row=row + 2, column=2, padx=5, pady=5, sticky="w")
    original_button = tk.Button(patch_frame, text="Browse", command=lambda: browse_file(original_button, relative_entry), height=2, width=25)
    original_button.grid(row=row + 2, column=1, pady=5, padx=10, sticky="ew")

    # Menu Path Section
    relative_label = tk.Label(patch_frame, text="Menu path:")
    relative_label.grid(row=row + 3, column=0, padx=5, sticky="w")
    relative_hint_button = tk.Button(patch_frame, text="?", command=lambda: show_hint_dialog("Info", "Input the path where the original file would be found in /content\n\n(e.g. if you're using Men.pack you would input: Common/Package/Men.pack)"), width=2, height=1, relief="solid", borderwidth=1)
    relative_hint_button.grid(row=row + 3, column=2, padx=5, pady=5, sticky="w")
    relative_entry = tk.Entry(patch_frame, width=35)
    relative_entry.grid(row=row + 3, column=1, pady=5, padx=10, sticky="ew")

    patch_widgets.append({
        'patch_label': patch_label,
        'bps_label': bps_label,
        'original_label': original_label,
        'relative_label': relative_label,
        'bps_button': bps_button,
        'original_button': original_button,
        'relative_entry': relative_entry,
        'bps_hint_button': bps_hint_button,
        'original_hint_button': original_hint_button,
        'relative_hint_button': relative_hint_button
    })

    patch_header_count += 1

def browse_file(button_widget, relative_entry):
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        full_paths[button_widget] = file_path
        short_path = os.path.basename(file_path)
        button_widget.config(text=short_path)

        if short_path == "Men.pack":
            relative_entry.delete(0, tk.END)
            relative_entry.insert(0, "Common/Package/Men.pack")
        elif short_path == "Men2.pack":
            relative_entry.delete(0, tk.END)
            relative_entry.insert(0, "Common/Package/Men2.pack")
        elif short_path == "cafe_barista_men.bfsar":
            relative_entry.delete(0, tk.END)
            relative_entry.insert(0, "Common/Sound/Men/cafe_barista_men.bfsar")
        check_duplicate_patch_files()

def check_duplicate_patch_files():
    bps_file_paths = []
    for patch in patch_widgets:
        bps_button = patch['bps_button']
        if bps_button in full_paths:
            bps_file_paths.append(full_paths[bps_button])

    if len(bps_file_paths) != len(set(bps_file_paths)):
        messagebox.showerror("Input Error", "Patch files cannot have the same filenames.\n\nIf you have a reason to patch a file with the same filename as one you have already included here (e.g. Text patches are done on a file called AllMessage.szs which has a consistent name across languages and regions), simply rename the .bps so that you may use it here.")
        last_clicked_bps = None
        for patch in reversed(patch_widgets):
            if patch['bps_button'] in full_paths:
                last_clicked_bps = patch['bps_button']
                break
        if last_clicked_bps:
            last_clicked_bps.config(text="Browse")
            del full_paths[last_clicked_bps]

def remove_patch():
    global patch_row_count, patch_header_count
    if patch_widgets:
        last_patch = patch_widgets.pop()

        last_patch['patch_label'].grid_forget()
        last_patch['bps_label'].grid_forget()
        last_patch['original_label'].grid_forget()
        last_patch['relative_label'].grid_forget()
        last_patch['bps_button'].grid_forget()
        last_patch['original_button'].grid_forget()
        last_patch['relative_entry'].grid_forget()
        last_patch['bps_hint_button'].grid_forget()
        last_patch['original_hint_button'].grid_forget()
        last_patch['relative_hint_button'].grid_forget()

        patch_row_count -= 4
        patch_header_count -= 1
        check_duplicate_patch_files()

def create_theme():
    patch_details = []
    for patch in patch_widgets:
        bps_button = patch['bps_button']
        original_button = patch['original_button']
        relative_path = patch['relative_entry'].get()
        bps_path = full_paths.get(bps_button, "")
        original_path = full_paths.get(original_button, "")
        patch_details.append((bps_path, original_path, relative_path))
    theme_name = e_theme_name.get()
    theme_author = e_theme_author.get()
    theme_id = e_theme_id.get()
    theme_region = e_theme_region.get() if e_theme_region.get() else "Universal"

    if not theme_name:
        messagebox.showwarning("Input Error", "Please name your theme")
        return

    if not theme_author:
        messagebox.showwarning("Input Error", "Please input the theme's author")
        return
    
    if not theme_id:
        messagebox.showwarning("Input Error", "Please input the theme ID")
        return
    
    if not patch_details:
        messagebox.showwarning("Input Error", "Please add at least one patch")
        return
    
    if not bps_path:
        messagebox.showwarning("Input Error", "Please select your patch file")
        return

    if not original_path:
        messagebox.showwarning("Input Error", "Please select your original file")
        return
        
    if not relative_path:
        messagebox.showwarning("Input Error", "Please input the menu path")
        return
    
    output_path = filedialog.askdirectory(title="Select Output Folder")

    if output_path:
        utheme_name, err_str = create_theme_archive(theme_name, theme_author, theme_id, theme_region, patch_details, output_path, full_paths)
        if utheme_name:
            messagebox.showinfo("Success", f"Theme archive created successfully! Saved as {utheme_name}")
        else:
            messagebox.showwarning("Utheme Creation Failure", err_str)
    else:
        messagebox.showwarning("Output Error", "Please select an output folder.")

root = tk.Tk()
root.title("Utheme Tool")

if platform.system() == "Darwin":
    # UI is weird on Mac
    root.geometry("550x600")
else:
    # Have to test on Linux distros
    root.geometry("400x600")
root.resizable(False, False)

patch_row_count = 0
patch_header_count = 1
patch_widgets = []

vcmd = (root.register(remove_spaces), '%P')

vcmd_name = (root.register(limit_characters), '%P', 30)
vcmd_author = (root.register(limit_characters), '%P', 25)
vcmd_id = (root.register(limit_characters), '%P', 25)

canvas = tk.Canvas(root)
canvas.pack(side="left", fill="both", expand=True)
canvas.bind_all("<MouseWheel>", on_scroll) 

scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", update_scroll_region)

h_main = tk.Label(scrollable_frame, text="Utheme Tool", font=("Arial", 24, "bold"))
h_main.grid(row=0, column=0, columnspan=3, pady=10, sticky="n")

h_desc = tk.Label(scrollable_frame, text="Tool to create Wii U theme archives (utheme)", font=("Arial", 12))
h_desc.grid(row=1, column=0, columnspan=3, pady=5, sticky="n")

h_theme_metadata = tk.Label(scrollable_frame, text="Theme Metadata", font=("Arial", 12, "bold"))
h_theme_metadata.grid(row=2, column=0, columnspan=3, pady=5, sticky="n")

tk.Label(scrollable_frame, text="Theme Name:").grid(row=3, column=0, padx=5, sticky="e")
e_theme_name = tk.Entry(scrollable_frame, width=25, validate="key", validatecommand=vcmd_name)
e_theme_name.grid(row=3, column=1, pady=5, padx=10, sticky="w")

tk.Label(scrollable_frame, text="Theme Author:").grid(row=4, column=0, padx=5, sticky="e")
e_theme_author = tk.Entry(scrollable_frame, width=25, validate="key", validatecommand=vcmd_author)
e_theme_author.grid(row=4, column=1, pady=5, padx=10, sticky="w")

tk.Label(scrollable_frame, text="Theme ID:").grid(row=5, column=0, padx=5, sticky="e")
e_theme_id = tk.Entry(scrollable_frame, width=25, validate="key", validatecommand=vcmd_id)
e_theme_id.grid(row=5, column=1, pady=5, padx=10, sticky="w")

id_hint_button = tk.Button(scrollable_frame, text="?", command=lambda: show_hint_dialog("Info", "An ID for your theme. Will be used as the name of the SDCafiine modpack when installed with Themiify among other things."), width=2, height=1, relief="solid", borderwidth=1)
id_hint_button.grid(row=5, column=2, padx=5, pady=5, sticky="w")

tk.Label(scrollable_frame, text="Theme Region:").grid(row=6, column=0, padx=5, sticky="e")
regions = ["Universal", "America", "Japan", "Europe"]
e_theme_region = ttk.Combobox(scrollable_frame, values=regions, width=22, state="readonly")
e_theme_region.grid(row=6, column=1, pady=5, padx=10, sticky="w")
region_hint_button = tk.Button(scrollable_frame, text="?", command=lambda: show_hint_dialog("Info", "Select the region for your theme (Defaults to Universal).\n\nNOTE: The only reason to select a specific region is if a theme has text patches (which are region specific), otherwise please use the Universal region. Please do not add text patches from different regions in your theme archive, they will fail to install with Themiify."), width=2, height=1, relief="solid", borderwidth=1)
region_hint_button.grid(row=6, column=2, padx=5, pady=5, sticky="w")

h_theme_patches = tk.Label(scrollable_frame, text="Patches", font=("Arial", 12, "bold"))
h_theme_patches.grid(row=7, column=0, columnspan=3, pady=10, sticky="n")

patch_frame = tk.Frame(scrollable_frame)
patch_frame.grid(row=8, column=0, columnspan=3, pady=5)

add_patch_button = tk.Button(scrollable_frame, text="Add New Patch Files", command=add_patch_fields, width=20, height=1, font=("Arial", 10))
add_patch_button.grid(row=9, column=0, columnspan=3, pady=5)

remove_patch_button = tk.Button(scrollable_frame, text="Remove Last Patch Files", command=remove_patch, width=20, height=1, font=("Arial", 10))
remove_patch_button.grid(row=10, column=0, columnspan=3, pady=5)

create_button = tk.Button(scrollable_frame, text="Create Theme Archive", command=create_theme, width=20, height=1, font=("Arial", 10))
create_button.grid(row=11, column=0, columnspan=3, pady=15)

root.mainloop()
