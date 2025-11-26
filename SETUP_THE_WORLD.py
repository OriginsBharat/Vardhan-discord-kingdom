import customtkinter
from tkinter import filedialog, messagebox
import os
import subprocess
import json
import sys

class SetupWizard(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("My AI World - Setup Wizard")
        self.geometry("800x600")

        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Allow kinks_frame to expand

        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # Secrets
        self.secrets_frame = customtkinter.CTkFrame(self.main_frame)
        self.secrets_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.secrets_frame.grid_columnconfigure(1, weight=1)

        # Create a scrollable frame for the tokens
        self.token_frame = customtkinter.CTkScrollableFrame(self.secrets_frame, label_text="Discord Bot Tokens")
        self.token_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.token_frame.grid_columnconfigure(1, weight=1)

        self.token_entries = {}
        with open("data/character_canon.json", "r", encoding="utf-8") as f:
            character_names = list(json.load(f).keys())

        for i, name in enumerate(character_names):
            label = customtkinter.CTkLabel(self.token_frame, text=f"{name}'s Token:")
            label.grid(row=i, column=0, padx=5, pady=2, sticky="w")
            entry = customtkinter.CTkEntry(self.token_frame, show="*")
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
            self.token_entries[name] = entry

        self.pinecone_key_label = customtkinter.CTkLabel(self.secrets_frame, text="Pinecone API Key:")
        self.pinecone_key_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.pinecone_key_entry = customtkinter.CTkEntry(self.secrets_frame, show="*")
        self.pinecone_key_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.pinecone_env_label = customtkinter.CTkLabel(self.secrets_frame, text="Pinecone Environment:")
        self.pinecone_env_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.pinecone_env_entry = customtkinter.CTkEntry(self.secrets_frame, placeholder_text="e.g., us-west1-gcp")
        self.pinecone_env_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.master_user_id_label = customtkinter.CTkLabel(self.secrets_frame, text="Your Discord User ID:")
        self.master_user_id_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.master_user_id_entry = customtkinter.CTkEntry(self.secrets_frame, placeholder_text="Right-click your profile > Copy User ID")
        self.master_user_id_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # File Paths
        self.paths_frame = customtkinter.CTkFrame(self.main_frame)
        self.paths_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.paths_frame.grid_columnconfigure(1, weight=1)

        self.ollama_path_label = customtkinter.CTkLabel(self.paths_frame, text="Ollama Executable Path:")
        self.ollama_path_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.ollama_path_entry = customtkinter.CTkEntry(self.paths_frame)
        self.ollama_path_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.ollama_browse_button = customtkinter.CTkButton(self.paths_frame, text="Browse", command=lambda: self.browse_file(self.ollama_path_entry))
        self.ollama_browse_button.grid(row=0, column=2, padx=10, pady=5)

        self.comfyui_path_label = customtkinter.CTkLabel(self.paths_frame, text="ComfyUI `run_nvidia_gpu.bat`:")
        self.comfyui_path_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.comfyui_path_entry = customtkinter.CTkEntry(self.paths_frame)
        self.comfyui_path_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.comfyui_browse_button = customtkinter.CTkButton(self.paths_frame, text="Browse", command=lambda: self.browse_file(self.comfyui_path_entry))
        self.comfyui_browse_button.grid(row=1, column=2, padx=10, pady=5)

        self.xtts_path_label = customtkinter.CTkLabel(self.paths_frame, text="XTTSv2 `run.bat`:")
        self.xtts_path_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.xtts_path_entry = customtkinter.CTkEntry(self.paths_frame)
        self.xtts_path_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.xtts_browse_button = customtkinter.CTkButton(self.paths_frame, text="Browse", command=lambda: self.browse_file(self.xtts_path_entry))
        self.xtts_browse_button.grid(row=2, column=2, padx=10, pady=5)

        # Kink Profiles
        self.kinks_frame = customtkinter.CTkScrollableFrame(self.main_frame, label_text="Character Kink Profiles")
        self.kinks_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.kinks_frame.grid_columnconfigure(1, weight=1)

        self.character_kinks = {}
        with open("data/character_canon.json", "r", encoding="utf-8") as f:
            characters = json.load(f)
            for i, char_name in enumerate(characters.keys()):
                label = customtkinter.CTkLabel(self.kinks_frame, text=f"{char_name}:")
                label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
                entry = customtkinter.CTkEntry(self.kinks_frame, placeholder_text="Enter comma-separated kinks")
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
                self.character_kinks[char_name] = entry

        # Setup Button
        self.setup_button = customtkinter.CTkButton(self.main_frame, text="Begin World Setup", command=self.begin_setup)
        self.setup_button.grid(row=3, column=0, padx=20, pady=20)

        self.status_label = customtkinter.CTkLabel(self.main_frame, text="")
        self.status_label.grid(row=4, column=0, padx=20, pady=10)

    def browse_file(self, entry):
        file_path = filedialog.askopenfilename()
        if file_path:
            entry.delete(0, "end")
            entry.insert(0, file_path)

    def browse_folder(self, entry):
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry.delete(0, "end")
            entry.insert(0, folder_path)

    def begin_setup(self):
        self.status_label.configure(text="Beginning setup... This may take a moment.")
        self.update_idletasks()

        tokens = {name: entry.get() for name, entry in self.token_entries.items()}

        # 1. Validate Inputs
        if not all(tokens.values()) or not all([
            self.pinecone_key_entry.get(),
            self.pinecone_env_entry.get(),
            self.master_user_id_entry.get(),
            self.ollama_path_entry.get(),
            self.comfyui_path_entry.get(),
            self.xtts_path_entry.get()
        ]):
            messagebox.showerror("Error", "All secrets and paths must be filled.")
            self.status_label.configure(text="Error: Missing required fields.")
            return

        # 2. Create .env file
        self.status_label.configure(text="Creating .env file...")
        self.update_idletasks()
        with open(".env", "w", encoding="utf-8") as f:
            for name, token in tokens.items():
                f.write(f"{name.upper()}_TOKEN={token}\n")

            f.write(f"PINECONE_API_KEY={self.pinecone_key_entry.get()}\n")
            f.write(f"PINECONE_ENVIRONMENT={self.pinecone_env_entry.get()}\n")
            f.write(f"MASTER_USER_ID={self.master_user_id_entry.get()}\n")
            f.write(f"OLLAMA_PATH={self.ollama_path_entry.get()}\n")
            f.write(f"COMFYUI_PATH={self.comfyui_path_entry.get()}\n")
            f.write(f"XTTS_PATH={self.xtts_path_entry.get()}\n")

        # 3. Save Kink Profiles
        self.status_label.configure(text="Saving kink profiles...")
        self.update_idletasks()
        kinks_data = {name: entry.get() for name, entry in self.character_kinks.items()}
        with open("data/character_kinks.json", "w", encoding="utf-8") as f:
            json.dump(kinks_data, f, indent=4)

        # 4. Create start_world.bat
        self.status_label.configure(text="Creating startup scripts...")
        self.update_idletasks()
        start_world_content = f"""
@echo off
REM Get the directory of the batch script
set "BATCH_DIR=%~dp0"

REM Start AI Servers in the background
echo "Starting Ollama..."
rem Use "" for the title to handle spaces in paths
start "" /B "{self.ollama_path_entry.get()}"

echo "Starting ComfyUI..."
set "COMFYUI_PATH={self.comfyui_path_entry.get()}"
set "COMFYUI_DIR=%COMFYUI_PATH%\\.."
cd /d "%COMFYUI_DIR%"
start "" /B cmd /c ""%COMFYUI_PATH%""

echo "Starting XTTSv2..."
set "XTTS_PATH={self.xtts_path_entry.get()}"
set "XTTS_DIR=%XTTS_PATH%\\.."
cd /d "%XTTS_DIR%"
start "" /B cmd /c ""%XTTS_PATH%""

REM Return to the original directory and add a delay
cd /d "%BATCH_DIR%"
REM Add a delay to allow servers to initialize
timeout /t 30

REM Start the main bot application
echo "Starting My AI World..."
set "MAIN_PY_PATH=%BATCH_DIR%src\\main.py"
start "MyAIWorld" /B python "%MAIN_PY_PATH%"
"""
        with open("start_world.bat", "w", encoding="utf-8") as f:
            f.write(start_world_content)

        # 6. Create invisible_launcher.vbs
        vbs_content = f'''
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "{os.path.abspath(os.getcwd())}"
WshShell.Run "cmd /c ""{os.path.abspath('start_world.bat')}""", 0
Set WshShell = Nothing
'''
        with open("invisible_launcher.vbs", "w", encoding="utf-8") as f:
            f.write(vbs_content)

        # 7. Place Shortcut in Startup Folder
        self.status_label.configure(text="Placing world in Windows Startup...")
        self.update_idletasks()
        try:
            startup_path = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
            vbs_path = os.path.abspath("invisible_launcher.vbs")
            shortcut_path = os.path.join(startup_path, "MyAIWorldLauncher.lnk")

            ps_command = f"""
$Shell = New-Object -ComObject WScript.Shell
$Shortcut = $Shell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{vbs_path}"
$Shortcut.WorkingDirectory = "{os.path.abspath(os.getcwd())}"
$Shortcut.Save()
"""
            subprocess.run(["powershell", "-Command", ps_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)

            messagebox.showinfo("Success", "World Setup Complete! The world will now awaken every time you start your PC.")
            self.status_label.configure(text="Setup complete. You may close this window.")
            self.destroy()

        except Exception as e:
            messagebox.showwarning("Admin Rights Needed",
                f"Could not automatically place the launcher in the Startup folder: {e}\\n\\n"
                "Please run this setup again as an administrator.\\n"
                "Alternatively, you can manually create a shortcut to 'invisible_launcher.vbs' and place it in your Startup folder:\\n"
                f"({startup_path})")
            self.status_label.configure(text="Warning: Manual step required for startup.")


if __name__ == "__main__":
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    app = SetupWizard()
    if not is_admin:
        app.title(app.title() + " (Admin Rights Recommended)")
    app.mainloop()