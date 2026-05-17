import sys
import os
import socket
import threading
import time
import webbrowser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.app import create_app


def open_browser_when_ready():
    for _ in range(40):
        try:
            conn = socket.create_connection(("127.0.0.1", 5000), timeout=1)
            conn.close()
            webbrowser.open("http://127.0.0.1:5000")
            return
        except OSError:
            time.sleep(0.5)


if __name__ == "__main__":
    flask_app = create_app()
    print("Starting Billing App at http://127.0.0.1:5000 ...")
    print("Your browser will open automatically. If it does not, navigate there manually.")
    threading.Thread(target=open_browser_when_ready, daemon=True).start()
    flask_app.run(debug=False, host="127.0.0.1", port=5000)
