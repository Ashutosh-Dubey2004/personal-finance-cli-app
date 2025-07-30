import shutil
import os
from ui_utils import pause
from db_init import DB_NAME

backupFileName = "finance_backup.db"

def backupDatabase():
    try:
        if os.path.exists(DB_NAME):
            shutil.copy(DB_NAME, backupFileName)
            pause("Backup created successfully.")
        else:
            pause("Database file not found.")
    except Exception as e:
        pause(f"Error while creating backup: {e}")

def restoreDatabase():
    try:
        if os.path.exists(backupFileName):
            shutil.copy(backupFileName, DB_NAME)
            pause("Database restored from backup.")
        else:
            pause("Backup file not found.")
    except Exception as e:
        pause(f"Error while restoring backup: {e}")
