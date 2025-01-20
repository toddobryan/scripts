import os
import shutil
from pathlib import Path

HOME = Path("/home")

def chown_home_folders():
    for user in HOME.iterdir():
        if user.is_dir():
            shutil.chown(user, user.name, user.name)
            chown_children_recursively(user, user.name, user.name)

def chown_children_recursively(path: Path, user: str, group: str):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            shutil.chown(os.path.join(root, dir), user, group)
        for file in files:
            shutil.chown(os.path.join(root, file), user, group)

