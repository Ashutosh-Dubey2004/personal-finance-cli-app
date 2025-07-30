import shutil
import os
from ui_utils import pause
from db_init import DB_NAME

BACKUP_NAME = "finance_backup.db"

def backupDatabase():
    try:
        if os.path.exists(DB_NAME):
            shutil.copy(DB_NAME, BACKUP_NAME)
            pause("Backup created successfully.")
        else:
            pause("Database file not found.")
    except Exception as e:
        pause(f"Error while creating backup: {e}")

def restoreDatabase():
    try:
        if os.path.exists(BACKUP_NAME):
            shutil.copy(BACKUP_NAME, DB_NAME)
            pause("Database restored from backup.")
        else:
            pause("Backup file not found.")
    except Exception as e:
        pause(f"Error while restoring backup: {e}")
