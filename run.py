import subprocess
import os
import sys

def launch_app():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    python_executable = os.path.join(base_dir, "portable_python", "python.exe")
    main_script = os.path.join(base_dir, "main.py")

    if not os.path.exists(python_executable):
        raise FileNotFoundError(f"Python not found at {python_executable}")
    if not os.path.exists(main_script):
        raise FileNotFoundError(f"Main script not found at {main_script}")

    subprocess.Popen([python_executable, "-m", "streamlit", "run", main_script])

if __name__ == "__main__":
    launch_app()
