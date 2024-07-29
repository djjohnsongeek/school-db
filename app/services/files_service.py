from flask import current_app
from app.repo import class_repo
from datetime import datetime
import os

def get_class_roster_file(class_id: int) -> str:
    roster = class_repo.retrieve_roster(class_id)

    download_dir = current_app.config["DOWNLOAD_DIR"]
    download_dir = os.path.join(current_app.root_path, download_dir)
    file_name = "class_roster.txt"
    file_path = os.path.join(download_dir, file_name)

    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    f = open(file_path, "w")
    timestamp = datetime.now()
    f.write(f"{timestamp}")
    f.close()

    return file_name
