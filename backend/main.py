import webview
import os
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Api:
    def get_version(self):
        try:
            with open(os.path.join(get_base_path(), 'VERSION'), 'r') as f:
                return f.read().strip()
        except:
            return "v1.0.0 'Apple'"

if __name__ == '__main__':
    api = Api()
    html_path = os.path.join(get_base_path(), 'frontend', 'index.html')
    
    window = webview.create_window(
        'RetroForge', 
        url=html_path,
        js_api=api,
        width=1000, 
        height=700,
        min_size=(800, 600),
        background_color='#0f1117'
    )
    
    webview.start(debug=True)
