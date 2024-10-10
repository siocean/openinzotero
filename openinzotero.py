import re
import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import json

def load_config(config_path):
    """Load configuration from JSON file."""
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
            #print(f"Loaded config: {config}")  # Debug statement
            return config
    #print("Config file not found.")  # Debug statement
    return {}

def save_config(app_path, config_path):
    """Save the secondary application path to the JSON file."""
    normalized_path = os.path.normpath(app_path)
    with open(config_path, 'w') as f:
        json.dump({"secondary_app": normalized_path}, f)
    #print(f"Saved config: {normalized_path}")  # Debug statement

def process_file(file_path):
    # Extract the file name from the full file path
    file_name = os.path.basename(file_path)
    #print(f"Processing file: {file_name}")  # Debug statement

    # Define the regex pattern to extract only the value after "ItemKey_" and before the .pdf extension
    pattern = r"ItemKey_(\w+)\.pdf$"
    match = re.search(pattern, file_name)
    
    if match:
        # Extract only the value after "ItemKey_"
        item_key = match.group(1)
        
        # Create the command to open Zotero with the specific item key
        #command = f'start zotero://select/library/items/{item_key}'
        command = f'start zotero://open-pdf/library/items/{item_key}'

        # Execute the command to open Zotero
        try:
            os.system(command)
            ##print(f"Opened Zotero for item key: {item_key}")  # Debug statement
        except Exception as e:
            print(f"Failed to open Zotero: {e}")
    else:
        # If the file name does not match the expected pattern, check for config in the exe directory
        exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        config_path = os.path.join(exe_dir, "config.json")
        config = load_config(config_path)
        secondary_app = config.get("secondary_app")

        if secondary_app:
            #print("File name not supported. Opening with the secondary default application...")
            try:
                # Use the absolute path for the secondary application and pass the full path of the file
                subprocess.run([secondary_app, os.path.abspath(file_path)], check=True)
                #print(f"Opened file with secondary app: {secondary_app}")  # Debug statement
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open the file with the secondary application: {e}")
        else:
            #print("Secondary application is not configured.")  # Debug statement
            messagebox.showinfo("Information", "No secondary application configured.")

def configure_application():
    """Open a dialog to configure the secondary application."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    app_path = filedialog.askopenfilename(title="Select Secondary Default Application", 
                                           filetypes=[("Executable Files", "*.exe"), 
                                                      ("All Files", "*.*")])
    
    if app_path:
        # Save config in the directory of the executable
        exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        config_path = os.path.join(exe_dir, "config.json")
        save_config(app_path, config_path)
        messagebox.showinfo("Information", f"Secondary application set to: {app_path}")
    else:
        messagebox.showinfo("Information", "No application selected.")

if __name__ == "__main__":
    # Check if a file path was provided as a command line argument
    if len(sys.argv) > 1:
        process_file(sys.argv[1])  # Process the file passed as an argument
    else:
        #print("No file path provided.")
        configure_application()  # Prompt to set the secondary application if no file path is given
