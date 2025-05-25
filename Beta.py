import sys
import ctypes
import subprocess
import tkinter as tk
import threading
import os
import itertools
import traceback
from tkinter import filedialog, messagebox

# --- Check for admin rights ---
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

if os.name == "nt" and not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# --- Package manager commands ---
package_managers = {
    "Chocolatey": {
        "check_command": "choco --version",
        "list_command": "choco list -l",
        "outdated_command": "choco outdated",
        "update_command": "choco upgrade all -y",
        "manager_update_command": "choco upgrade chocolatey -y"
    },
    "Winget": {
        "check_command": "winget --version",
        "list_command": "winget list",
        "outdated_command": "winget upgrade",
        "update_command": "winget upgrade --all",
        "manager_update_command": None
    },
    "Scoop": {
        "check_command": "scoop --version",
        "list_command": "scoop list",
        "outdated_command": "scoop status",
        "update_command": "scoop update *",
        "manager_update_command": None
    },
    "NPM": {
        "check_command": "npm --version",
        "list_command": "npm -g list --depth=0",
        "outdated_command": "npm -g outdated --parseable",
        "update_command": "npm update -g",
        "manager_update_command": None
    },
    "Pip": {
        "check_command": "pip --version",
        "list_command": "pip list",
        "outdated_command": "pip list --outdated",
        "update_command": "pip install --upgrade pip setuptools",
        "manager_update_command": None
    },
    "Gem": {
        "check_command": "gem --version",
        "list_command": "gem list",
        "outdated_command": "gem outdated",
        "update_command": "gem update",
        "manager_update_command": None
    },
    "Homebrew": {
        "check_command": "brew --version",
        "list_command": "brew list --formula",
        "outdated_command": "brew outdated",
        "update_command": "brew upgrade",
        "manager_update_command": None
    }
}

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        error = result.stderr
        if result.returncode != 0:
            error += f"\nError code: {result.returncode}\n"
        return output, error
    except Exception:
        return "", traceback.format_exc()

def show_env_info():
    print("\n--- Environment Variables ---")
    print(f"PATH:\n{os.environ.get('PATH', '')}\n")
    sys.stdout.flush()

class PackageManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Package Manager Overview & Update")
        self.info_frames = {}

        # --- Spinner Label (NEU) ---
        self.spinner_label = tk.Label(self.root, text="", font=("Consolas", 18))
        self.spinner_label.pack(pady=(5, 0))

        self.init_gui()

    def init_gui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(padx=10, pady=10, fill="x")
        btn_frame = tk.Frame(top_frame)
        btn_frame.pack(side="top", fill="x")
        self.update_btn = tk.Button(btn_frame, text="Check & Update Packages", command=self.start_update_thread)
        self.update_btn.pack(side="left", padx=5)
        # --- Export/Import Buttons mit Spinner ---
        self.export_btn = tk.Button(btn_frame, text="Export Packages", command=self.export_packages_thread)
        self.export_btn.pack(side="left", padx=5)
        self.import_btn = tk.Button(btn_frame, text="Import Packages", command=self.import_packages_thread)
        self.import_btn.pack(side="left", padx=5)

        info_frame = tk.Frame(self.root)
        info_frame.pack(padx=10, pady=10, fill="x")
        for manager in package_managers.keys():
            frame = tk.LabelFrame(info_frame, text=manager)
            frame.pack(side="top", fill="x", padx=5, pady=2)
            self.info_frames[manager] = {
                "frame": frame,
                "version": tk.Label(frame, text="Version: -"),
                "installed": tk.Label(frame, text="Installed Packages: -"),
                "updates": tk.Label(frame, text="Updates Available: -"),
                "spinner": tk.Label(frame, text="", font=("Consolas", 14))
            }
            self.info_frames[manager]["version"].pack(side="left", padx=10)
            self.info_frames[manager]["installed"].pack(side="left", padx=10)
            self.info_frames[manager]["updates"].pack(side="left", padx=10)
            self.info_frames[manager]["spinner"].pack(side="left", padx=10)

    # --- Spinner-Logik für oben im Fenster ---
    def start_top_spinner(self):
        self.spinner_label._spinner_cycle = itertools.cycle(['/', '-', '\\', '|'])
        self.spinner_label._running = True
        self.animate_top_spinner()

    def animate_top_spinner(self):
        if getattr(self.spinner_label, "_running", False):
            self.spinner_label.config(text=next(self.spinner_label._spinner_cycle))
            self.spinner_label.after(100, self.animate_top_spinner)
        else:
            self.spinner_label.config(text="")

    def stop_top_spinner(self):
        self.spinner_label._running = False

    # --- Export/Import mit Ladeanimation ---
    def export_packages_thread(self):
        self.start_top_spinner()
        def do_export():
            self.export_packages()
            self.stop_top_spinner()
        threading.Thread(target=do_export, daemon=True).start()

    def import_packages_thread(self):
        self.start_top_spinner()
        def do_import():
            self.import_packages()
            self.stop_top_spinner()
        threading.Thread(target=do_import, daemon=True).start()

    def start_update_thread(self):
        threading.Thread(target=self.update_all_managers, daemon=True).start()

    def start_spinner(self, manager):
        label = self.info_frames[manager]["spinner"]
        label._spinner_cycle = itertools.cycle(['/', '-', '\\', '|'])
        label._running = True
        self.animate_spinner(manager)

    def animate_spinner(self, manager):
        label = self.info_frames[manager]["spinner"]
        if getattr(label, "_running", False):
            label.config(text=next(label._spinner_cycle))
            label.after(100, lambda: self.animate_spinner(manager))
        else:
            label.config(text="")

    def stop_spinner(self, manager):
        self.info_frames[manager]["spinner"]._running = False

    def update_all_managers(self):
        show_env_info()
        for manager, cmds in package_managers.items():
            self.start_spinner(manager)
            print(f"--- {manager} ---")
            sys.stdout.flush()
            version, err = run_command(cmds["check_command"])
            if version:
                self.info_frames[manager]["version"].config(text=f"Version: {version.splitlines()[0]}")
                print(f"Version: {version}")
            else:
                self.info_frames[manager]["version"].config(text="Not installed")
                self.info_frames[manager]["installed"].config(text="Installed Packages: -")
                self.info_frames[manager]["updates"].config(text="Updates Available: -")
                print(f"{manager} not found.\n")
                if err:
                    print(err)
                self.stop_spinner(manager)
                continue
            installed, inst_err = run_command(cmds["list_command"])
            installed_count = len([line for line in installed.splitlines() if line.strip()]) if installed else 0
            self.info_frames[manager]["installed"].config(text=f"Installed Packages: {installed_count}")
            print(f"Installed Packages: {installed_count}")
            outdated, outd_err = run_command(cmds["outdated_command"])
            outdated_count = len([line for line in outdated.splitlines() if line.strip()]) if outdated else 0
            self.info_frames[manager]["updates"].config(text=f"Updates Available: {outdated_count}")
            print(f"Updates Available: {outdated_count}")
            if err:
                print("Error:", err)
            if inst_err:
                print("Error:", inst_err)
            if outd_err:
                print("Error:", outd_err)
            print(f"Updating packages...")
            sys.stdout.flush()
            update_out, update_err = run_command(cmds["update_command"])
            if update_out:
                print(update_out)
            if update_err:
                print("Error:", update_err)
            if cmds["manager_update_command"]:
                print(f"Updating {manager} itself...")
                mgr_out, mgr_err = run_command(cmds["manager_update_command"])
                if mgr_out:
                    print(mgr_out)
                if mgr_err:
                    print("Error:", mgr_err)
            print()
            sys.stdout.flush()
            self.stop_spinner(manager)
        print("All package managers checked and updated.")
        sys.stdout.flush()

    def export_packages(self):
        export_data = {}
        for manager, cmds in package_managers.items():
            out, _ = run_command(cmds["list_command"])
            if out:
                pkgs = [line.strip() for line in out.splitlines() if line.strip()]
                export_data[manager] = pkgs
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file:
            with open(file, "w", encoding="utf-8") as f:
                for manager, pkgs in export_data.items():
                    f.write(f"[{manager}]\n")
                    for pkg in pkgs:
                        f.write(pkg + "\n")
            self.root.after(0, lambda: messagebox.showinfo("Export", "Package list exported."))

    def import_packages(self):
        file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file:
            return
        with open(file, "r", encoding="utf-8") as f:
            current_manager = None
            pkgs = {}
            for line in f:
                line = line.strip()
                if line.startswith("[") and line.endswith("]"):
                    current_manager = line[1:-1]
                    pkgs[current_manager] = []
                elif current_manager and line:
                    pkgs[current_manager].append(line)
        for manager, packages in pkgs.items():
            if manager in package_managers and packages:
                print(f"Installing packages for {manager}:")
                for pkg in packages:
                    if manager == "Chocolatey":
                        cmd = f"choco install {pkg} -y"
                    elif manager == "Winget":
                        cmd = f"winget install --id {pkg} -e --accept-source-agreements --accept-package-agreements"
                    elif manager == "Scoop":
                        cmd = f"scoop install {pkg}"
                    elif manager == "NPM":
                        cmd = f"npm install -g {pkg}"
                    elif manager == "Pip":
                        cmd = f"pip install {pkg}"
                    elif manager == "Gem":
                        cmd = f"gem install {pkg}"
                    elif manager == "Homebrew":
                        cmd = f"brew install {pkg}"
                    else:
                        continue
                    print(cmd)
                    out, err = run_command(cmd)
                    if out:
                        print(out)
                    if err:
                        print(err)
        self.root.after(0, lambda: messagebox.showinfo("Import", "Packages installed (see terminal for details)."))

# --- Main program ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PackageManagerGUI(root)
    root.mainloop()

