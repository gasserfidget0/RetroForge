import os
import requests
import threading
import re

DOWNLOAD_DIR = os.path.join(os.environ.get('USERPROFILE', 'C:\\'), 'Downloads', 'RetroForge')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class Downloader:
    def __init__(self, window):
        self.window = window
        self.is_downloading = False
        
    def fetch_latest_release(self, repo, asset_pattern):
        url = f"https://api.github.com/repos/{repo}/releases/latest"
        resp = requests.get(url).json()
        
        if 'assets' not in resp:
            # Fallback to releases list if latest isn't explicitly marked
            url = f"https://api.github.com/repos/{repo}/releases"
            releases = requests.get(url).json()
            if not releases:
                raise Exception("No releases found")
            resp = releases[0]
            
        for asset in resp.get('assets', []):
            if re.search(asset_pattern, asset['name'], re.IGNORECASE):
                return asset['name'], asset['browser_download_url'], asset['size']
                
        raise Exception(f"No asset matching pattern '{asset_pattern}' found in latest release.")
        
    def download_file(self, url, filename, total_size):
        self.is_downloading = True
        filepath = os.path.join(DOWNLOAD_DIR, filename)
        
        # Check if already downloaded
        if os.path.exists(filepath) and os.path.getsize(filepath) == total_size:
            self.window.evaluate_js(f"updateDownloadProgress(100, 'Already downloaded: {filename}')")
            self.window.evaluate_js(f"onDownloadComplete('{filepath.replace('\\', '\\\\')}')")
            self.is_downloading = False
            return filepath
            
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                downloaded = 0
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            percent = int((downloaded / total_size) * 100)
                            
                            # Throttle JS updates slightly to avoid overwhelming the bridge
                            if downloaded % (8192 * 100) == 0 or downloaded == total_size:
                                self.window.evaluate_js(f"updateDownloadProgress({percent}, 'Downloading {filename}... {percent}%')")
                                
            self.window.evaluate_js(f"updateDownloadProgress(100, 'Download complete!')")
            self.window.evaluate_js(f"onDownloadComplete('{filepath.replace('\\', '\\\\')}')")
        except Exception as e:
            self.window.evaluate_js(f"updateDownloadProgress(0, 'Error: {str(e)}')")
        finally:
            self.is_downloading = False
            return filepath
            
    def start_download(self, repo, asset_pattern):
        if self.is_downloading:
            return {"ok": False, "error": "ALREADY_DOWNLOADING", "message": "A download is already in progress."}
            
        def worker():
            try:
                self.window.evaluate_js("updateDownloadProgress(0, 'Fetching release info from GitHub...')")
                name, url, size = self.fetch_latest_release(repo, asset_pattern)
                self.download_file(url, name, size)
            except Exception as e:
                self.window.evaluate_js(f"updateDownloadProgress(0, 'Error: {str(e)}')")
                self.is_downloading = False
                
        threading.Thread(target=worker, daemon=True).start()
        return {"ok": True, "message": "Download started"}
