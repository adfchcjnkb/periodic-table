"""
📄 backend/run.py - Super Simple Runner
"""
#!/usr/bin/env python3
import os
import sys
import socket
import webbrowser
import threading
import time
import http.server
import socketserver
from pathlib import Path

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ██████╗ ███████╗██████╗ ██╗ ██████╗ ██████╗ ██╗ █████╗   ║
║   ██╔══██╗██╔════╝██╔══██╗██║██╔═══██╗██╔══██╗██║██╔══██╗   ║
║   ██████╔╝█████╗  ██████╔╝██║██║   ██║██████╔╝██║███████║   ║
║   ██╔══██╗██╔══╝  ██╔══██╗██║██║   ██║██╔═══╝ ██║██╔══██║   ║
║   ██║  ██║███████╗██║  ██║██║╚██████╔╝██║     ██║██║  ██║   ║
║   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝   ║
║                                                          ║
║              🚀 PERIODIC TABLE API 🚀                    ║
║               Simple Static Server                       ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)

def find_free_port(start=8000):
    for port in range(start, 9000):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.bind(('127.0.0.1', port))
                return port
        except:
            continue
    return start

def serve_static(port=8000):
    """Serve static files"""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"\n📂 Serving from: {project_root}")
    print(f"🌐 URL: http://127.0.0.1:{port}")
    print(f"📄 Main page: http://127.0.0.1:{port}/index.html")
    print("🛑 Press Ctrl+C to stop\n")
    
    # Open browser
    def open_browser():
        time.sleep(1)
        webbrowser.open(f"http://127.0.0.1:{port}/index.html")
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start server
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"✅ Server started successfully!")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def main():
    print_banner()
    
    port = find_free_port(8000)
    
    # Check if we should try FastAPI
    api_file = Path(__file__).parent / "api.py"
    if api_file.exists():
        print("🔍 Found api.py")
        
        # Check if it's FastAPI or Django
        with open(api_file, 'r') as f:
            content = f.read()
            
        if "FastAPI" in content or "fastapi" in content:
            print("✅ Detected FastAPI")
            try:
                import uvicorn
                print("🚀 Starting FastAPI...")
                
                def open_browser():
                    time.sleep(2)
                    webbrowser.open(f"http://127.0.0.1:{port}/docs")
                
                threading.Thread(target=open_browser, daemon=True).start()
                
                uvicorn.run("api:app", host="127.0.0.1", port=port, reload=False)
                return
            except Exception as e:
                print(f"⚠️ FastAPI failed: {e}")
                print("🔄 Falling back to static server...")
    
    # Default to static server
    serve_static(port)

if __name__ == '__main__':
    main()