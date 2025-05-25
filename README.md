# Every-Update


# 🛠️ Guide: Python package manager GUI with loading animation for export/import

## Prerequisites

- Python 3.7+**
- The most important package managers (Chocolatey, Winget, Scoop, NPM, Pip, Gem, Homebrew) are supported and should be in the PATH.
- The script from the file `every_update_1.0.0.py` (see below).
- CURRENTLY ONLY AVAILABLE FOR WINDOWS  

---

## Installation

1. install **Python**  
   [Download Python](https://www.python.org/downloads/) and install it, if not already done.

2. install **required packages**  
   The script uses only standard libraries (`tkinter`, `subprocess`, etc.), no external packages necessary.

3 **Save script**  
   Save the script e.g. as `every_update_1.0.0.py` on your PC.

---

## Start the application

Open a terminal (cmd, PowerShell) and start the script with:

```sh
python every_update_1.0.0.py
```

> **Note:**  
> Under Windows, the script may require administrator rights in order to use the package manager.  
> The script requests these rights automatically.

---

## Operation

### Main functions

- Check & Update Packages**  
  Checks all supported package managers, shows available updates and installs them on request.

- **Export Packages**  
  Exports all installed packages of all supported managers to a text file.  

- Import Packages**  
  Imports a previously exported package list and installs all packages contained therein automatically.  

### GUI elements

- **Center:**  
  Overview of all package managers with:
  - Version
  - Number of installed packages
  - Number of available updates
  - Own spinner per manager during updates

---

## Export/import of package lists

### Export

1. click on **Export Packages**.
2. select a storage location and file name (e.g. `packages.txt`).
3. a confirmation appears after completion.

### Import

1. click on **Import Packages**.
2. select the previously exported file.
3. the packages will be installed automatically (see Terminal for details).

---

## Hints

- **Terminal output:**  
  All details, errors and progress are displayed in the real terminal window, not in the GUI.
- **Loading animation:**  
  During export/import an animated spinner can be seen at the top of the window.
- **Administrator rights:**  
  Admin rights are required for many package managers. The script starts automatically with elevated rights if required.

---

## Troubleshooting

- **GUI does not start:**  
  Make sure that Python is installed and the script is not executed by a restricted user account.
- **A package manager is missing:**  
  Check if the package manager is installed and in the PATH, it is not bad if a package manager is missing.
- Error during export/import:**  
  See the output in the terminal window for details and error causes.

---

## Customizations

- **Add more package managers:**  
  Add to the `package_managers` dictionary in the script.
- **Customize design/spinner:**  
  Customize the spinner logic or layout in the script according to your wishes.

---

**Have fun managing your packages** 🚀

Translated with DeepL.com (free version)
