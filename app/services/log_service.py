from flask import current_app
from datetime import datetime
import os

def record_log(msg: str, app_area: str, log_type: str):
    log_path = current_app.config["LOG_FILE_PATH"]
    log_path = os.path.join(current_app.root_path, log_path)
    f = open(log_path, "a")
    timestamp = datetime.now()
    log_str = f"{log_type.upper()}: {app_area} - {msg} ({timestamp})\n"
    f.write(log_str)
    f.close()