import shutil
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import FOLDER_RULES


#logging set up, prints to terminal and writes in organizer.log file

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s',
                     datefmt='%Y-%m-%d %H:%M:%S', 
                     handlers=[logging.FileHandler("organizer.log"),
                            logging.StreamHandler()])

#inherits from watchdog, 

class FileOrganizer(FileSystemEventHandler):
    def __init__(self, watch_folder):
        self.watch_folder = Path(watch_folder)



#overriding watchdog's oncreated with our own function, which will be called when a new file is created in the watch folder. It checks if the created item is a directory, if not it calls the organize_file function to move the file to the appropriate folder based on its extension.

    def on_created(self, event): #skips folders and only organizes files
        if event.is_directory:
            return
        self.organize_file(Path(event.src_path))

    def organize_file(self, file_path):
        extension = file_path.suffix.lower() 
        folder_name = FOLDER_RULES.get(extension, "Misc") #crash handling for misc if file type not found in dictionary, it will be moved to misc folder
        destination_folder = self.watch_folder / folder_name
        destination_folder.mkdir(exist_ok=True)
        destination_file = destination_folder / file_path.name

        if destination_file.exists(): #creates the subfolder if it doesn't exist
            logging.info(f"Skipped (already exists): {file_path.name}")
            return
        
        shutil.move(str(file_path), str(destination_file)) #magic file mover
        logging.info(f"Moved: {file_path.name} to {folder_name}")



def scan_existing_files(watch_folder,organizer):
    logging.info("Scanning existing files...")
    for file_path in Path(watch_folder).iterdir():
        if file_path.is_file():
            organizer.organize_file(file_path)

def main():
    watch_folder = Path.home()/"Desktop"/ "Test Downloads" #default watch folder, can be changed to any folder you want
    
    organizer = FileOrganizer(watch_folder)
    scan_existing_files(watch_folder,organizer) #loops through existing files in the folder and runs organize_file on each one before the watcher starts

    observer = Observer()
    observer.schedule(organizer, str(watch_folder), recursive=False) # tells watchdog which folder to watch and which user to handle recursive = false, so it only watches the specified folder and not its subfolders, which is what we want for this organizer.

    observer.start()

    logging.info(f"Watching folder: {watch_folder} for new files...")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
                observer.stop()
                logging.info("Organizer stopped by user.")
            
    observer.join()

if __name__ == "__main__":
    main()