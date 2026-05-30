import threading 
import time
import logging
from tkinter import filedialog
from pathlib import Path
import customtkinter as ctk
from watchdog.observers import Observer
from organizer import FileOrganizer, scan_existing_files


#globals 
observer = None
watch_folder = Path.home()/"Desktop"/ "Test Downloads" #default watch folder, can be changed to any folder you want


def browse_folder():
    file_path = filedialog.askdirectory()
    if file_path:
        global watch_folder
        watch_folder = Path(file_path)
        label_folder.configure(text=f"Watching: {watch_folder}") 

def start_organizer():
    global observer
    organizer = FileOrganizer(watch_folder)
    scan_existing_files(watch_folder,organizer) #loops through existing files in the folder and runs organize_file on each one before the watcher starts

    observer = Observer()
    observer.schedule(organizer, str(watch_folder), recursive=False) # tells watchdog which folder to watch and which user to handle recursive = false, so it only watches the specified folder and not its subfolders, which is what we want for this organizer.

    observer.start()
    logging.info(f"Watching folder: {watch_folder} for new files...")
    btn_start.configure(state="disabled")
    btn_stop.configure(state="normal")
    start_thread()


def stop_organizer():
    global observer
    if observer:
        observer.stop()
        observer.join()
        logging.info("Organizer stopped by user.")
        btn_start.configure(state="normal")
        btn_stop.configure(state="disabled")

def run_loop():
    if observer:
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            observer.stop()
            logging.info("Organizer stopped by user.")
            observer.join()

def start_thread():
    thread = threading.Thread(target=run_loop, daemon=True)
    thread.start()


def log_message(message):
    textbox.configure(state="normal")
    textbox.insert("end", message + "\n")
    textbox.configure(state="disabled")
    textbox.see("end")

class TextHandler(logging.Handler):
    def emit(self, record):
        message = self.format(record)
        textbox.after(0, log_message, message)
# Set up logging



#window 

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("File Organizer")
app.geometry("600x500")

#widgets
#labels and buttons
label_title = ctk.CTkLabel(app, text="File Organizer", font=ctk.CTkFont(size=20, weight="bold"))
label_title.pack(pady=(20,5))

label_folder = ctk.CTkLabel(app, text=f"Watching: {watch_folder}", font=ctk.CTkFont(size=12), text_color="gray")
label_folder.pack(pady=(0,15))

btn_browse = ctk.CTkButton(app, text="Browse Folder", command=browse_folder, width=200)
btn_browse.pack(pady=(0,15))

btn_start = ctk.CTkButton(app, text="Start Organizing", command=start_organizer, width=200, fg_color="green", hover_color="darkgreen")
btn_start.pack(pady=(0,15))

btn_stop = ctk.CTkButton(app, text="Stop Organizing", command=stop_organizer, width=200, fg_color="red", hover_color="darkred", state="disabled")
btn_stop.pack(pady=5)

label_log = ctk.CTkLabel(app, text ="Activitiy Log:")
label_log.pack(pady=(15,5))

textbox = ctk.CTkTextbox(app, width=560, height=200, state ="disabled")
textbox.pack(pady=5)

handler = TextHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

#app starting

app.mainloop()