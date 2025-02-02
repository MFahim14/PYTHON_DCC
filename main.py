import subprocess
import sys
import os
from threading import Thread

def run_flask_server():
    """Run the Flask server."""
    os.chdir("server")
    subprocess.run([sys.executable, "server.py"])

def run_pyqt_ui():
    """Run the PyQt5 UI."""
    os.chdir("ui")
    subprocess.run([sys.executable, "inventory_ui.py"])

if __name__ == "__main__":
    print("Starting Flask server and PyQt5 UI...")

    # Run Flask server in a separate thread
    flask_thread = Thread(target=run_flask_server)
    flask_thread.daemon = True
    flask_thread.start()

    # Run PyQt5 UI
    run_pyqt_ui()