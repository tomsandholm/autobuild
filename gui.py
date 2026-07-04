import os
import re
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

# Hardcoded absolute path to your Makefile
MAKEFILE_PATH = "/home/sandholm/prog/autobuild/Makefile"
# Target directory where the make command MUST run
TARGET_WORKING_DIR = os.path.expanduser("~/prog/autobuild")

class MakefileGuiBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Node Build Configuration")
        self.root.geometry("500x500")
        self.root.resizable(True, True)
        
        # Changed "FQDN" to "NAME"
        self.vars_to_collect = ["NAME", "ROLE", "RAM", "DISK"]
        self.entry_fields = {}
        
        # Load default values from Makefile if available
        self.defaults = self.parse_makefile(MAKEFILE_PATH)
        
        self.create_widgets()

    def parse_makefile(self, filepath):
        """Rudimentary parser to extract default values from the Makefile."""
        # Default fallback updated to use NAME instead of FQDN
        defaults = {"NAME": "node-01", "ROLE": "worker", "RAM": "2048", "DISK": "20G"}
        
        if not os.path.exists(filepath):
            print(f"Warning: Makefile not found at {filepath}. Using generic fallbacks.")
            return defaults

        var_regex = re.compile(r'^\s*([A-Za-z0-9_]+)\s*\??=\s*(.*)$')
        
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    match = var_regex.match(line.strip())
                    if match:
                        key, val = match.groups()
                        if key in self.vars_to_collect or key.lower() in [v.lower() for v in self.vars_to_collect]:
                            defaults[key.upper()] = val.strip()
        except Exception as e:
            print(f"Error reading Makefile: {e}")
            
        return defaults

    def create_widgets(self):
        header_label = ttk.Label(
            self.root, 
            text="Configure Node Deployment", 
            font=("Helvetica", 14, "bold")
        )
        header_label.pack(pady=15)

        form_frame = ttk.Frame(self.root, padding="10")
        form_frame.pack(fill="both", expand=True)

        for idx, var in enumerate(self.vars_to_collect):
            label = ttk.Label(form_frame, text=f"{var}:", font=("Helvetica", 11))
            label.grid(row=idx, column=0, sticky="w", pady=8, padx=5)
            
            entry_val = tk.StringVar(value=self.defaults.get(var, ""))
            entry = ttk.Entry(form_frame, textvariable=entry_val, width=30)
            entry.grid(row=idx, column=1, sticky="ew", pady=8, padx=5)
            
            self.entry_fields[var] = entry_val

        form_frame.columnconfigure(1, weight=1)

        separator = ttk.Separator(self.root, orient="horizontal")
        separator.pack(fill="x", padx=15, pady=10)

        btn_frame = ttk.Frame(self.root, padding="10")
        btn_frame.pack(fill="x")

        build_btn = ttk.Button(
            btn_frame, 
            text="🔨 Build Node", 
            command=self.run_make_build
        )
        build_btn.pack(side="right", padx=5)

        cancel_btn = ttk.Button(
            btn_frame, 
            text="Cancel", 
            command=self.root.quit
        )
        cancel_btn.pack(side="right", padx=5)

    def run_make_build(self):
        args = {var: var_str.get().strip() for var, var_str in self.entry_fields.items()}
        
        # Updated validation to check NAME instead of FQDN
        if not args["NAME"]:
            messagebox.showerror("Error", "NAME cannot be empty.")
            return
        if not args["ROLE"]:
            messagebox.showerror("Error", "ROLE cannot be empty.")
            return

        cmd = ["make", "node"]
        for key, val in args.items():
            cmd.append(f"{key}={val}")

        if not os.path.isdir(TARGET_WORKING_DIR):
            messagebox.showerror(
                "Directory Error", 
                f"Target directory does not exist:\n{TARGET_WORKING_DIR}"
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Build", 
            f"Working Directory: {TARGET_WORKING_DIR}\n\nRunning command:\n{' '.join(cmd)}"
        )
        
        if confirm:
            try:
                result = subprocess.run(
                    cmd, 
                    cwd=TARGET_WORKING_DIR, 
                    capture_output=True, 
                    text=True, 
                    check=True
                )
                messagebox.showinfo("Success", f"Build finished successfully!\n\n{result.stdout[-500:]}")
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr if e.stderr else e.stdout
                messagebox.showerror("Build Failed", f"Command failed with exit code {e.returncode}.\n\nError:\n{error_msg[-500:]}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MakefileGuiBuilder(root)
    root.mainloop()
