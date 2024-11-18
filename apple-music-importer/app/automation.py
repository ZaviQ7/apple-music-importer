import os
import platform
import subprocess
from pathlib import Path

def get_downloads_path():
    """Get the user's Downloads folder path"""
    if platform.system() == "Windows":
        try:
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                downloads_path = winreg.QueryValueEx(key, downloads_guid)[0]
            return downloads_path
        except Exception:
            # Fallback to default Windows Downloads path
            return str(Path.home() / "Downloads")
    else:
        # macOS and Linux
        return str(Path.home() / "Downloads")

def open_downloads_folder():
    """Open the Downloads folder using the appropriate system command"""
    try:
        downloads_path = get_downloads_path()
        
        if platform.system() == "Windows":
            # Open and focus the Downloads folder
            subprocess.run(['explorer', downloads_path])
        elif platform.system() == "Darwin":  # macOS
            # Use AppleScript to activate Finder and open path
            script = f'''
            tell application "Finder"
                activate
                open POSIX file "{downloads_path}"
                set the front window to window 1
            end tell
            '''
            subprocess.run(['osascript', '-e', script])
        else:  # Linux
            # Most Linux file managers should focus the new window by default
            subprocess.run(['xdg-open', downloads_path])
        
        return True, None
    except Exception as e:
        return False, str(e)

def get_system_info():
    """Get system information for troubleshooting"""
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": platform.python_version(),
        "downloads_path": get_downloads_path()
    }