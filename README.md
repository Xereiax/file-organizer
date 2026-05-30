## File Organizer

This is a Python desktop app that automatically sorts files into subfolders by type. Built with a real-time activity log and a clean dark UI


## Features

- Automatically sorts files into folders (Images, Videos, Documents, etc.)
- Actively watches a folder for new files
- Scans and sorts existing files on startup
- Browse and select any folder to watch
- Live activity log inside the app
- Built with Python, CustomTkinter, and Watchdog

## Setup

pip install -r requirements.txt

## Run
python ui.py

## How it works
Files are sorted based on their extension using a rules dictionary found in config.py. If you want to add your own file types, goto config.py and add them without touching any other code.