# NOTE: Put config in an instance folder

import os
cwd = os.getcwd()

DB_NAME = ""
DB_USER = ""
DB_PORT = 0
DB_HOST = ""
DB_PASSWORD = ""

# LOCKOUT_DUR_MINUTES must be > LOCKOUT RANGE
LOCKOUT_RANGE_MINUTES = 0
LOCKOUT_DUR_MINUTES = 0
FAILED_LOGIN_THRESHOLD = 0

CONTACT_EMAIL = ""
MAILJET_API_KEY = ""
MAILJET_SECRET_KEY = ""
MAILJET_SENDER_EMAIL = ""

LOG_FILE_PATH = os.path.join(cwd, "instance", "error_logs.txt")

# API CONFIG
ALLOWED_CATEGORIES = ["staff"]
ALLOWED_ACTIONS = ["delete"]