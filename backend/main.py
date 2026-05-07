import webview
import os
import sys
import json
from sd_detector import get_removable_drives
from downloader import Downloader

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Api:
    def __init__(self):
        self.window = None
        self.downloader = None
        self.manifest_data = None
        
    def set_window(self, window):
        self.window = window
        self.downloader = Downloader(window)

    def get_version(self):
        try:
            with open(os.path.join(get_base_path(), 'VERSION'), 'r', encoding='utf-8') as f:
                return f.read().strip()
        except:
            return "v1.0.0 'Apple'"
            
    def get_drives(self):
        try:
            drives = get_removable_drives()
            return {"ok": True, "data": drives}
        except Exception as e:
            return {"ok": False, "error": "DRIVE_SCAN_FAILED", "message": str(e)}

    def get_os_catalog(self):
        try:
            if not self.manifest_data:
                manifest_path = os.path.join(get_base_path(), 'manifests', 'devices.json')
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    self.manifest_data = json.load(f)
            return {"ok": True, "data": self.manifest_data}
        except Exception as e:
            return {"ok": False, "error": "MANIFEST_LOAD_FAILED", "message": str(e)}
            
    def download_os(self, repo, asset_pattern):
        try:
            return self.downloader.start_download(repo, asset_pattern)
        except Exception as e:
            return {"ok": False, "error": "DOWNLOAD_INIT_FAILED", "message": str(e)}

if __name__ == '__main__':
    api = Api()
    html_path = os.path.join(get_base_path(), 'frontend', 'index.html')
    
    window = webview.create_window(
        'RetroForge', 
        url=html_path,
        js_api=api,
        width=900, 
        height=750,
        min_size=(800, 600),
        background_color='#0f1117'
    )
    
    api.set_window(window)
    webview.start(debug=True)
