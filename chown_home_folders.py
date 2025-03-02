import os
import shutil
import subprocess
from pathlib import Path

HOME = Path("/home")
TURNIN = "turnin"
COLLECTED = "collected"
ROOT = "root"
MODE = 0o555

def chown_home_folders() -> None:
    for user in HOME.iterdir(): #type: Path
        if user.is_dir():
            shutil.chown(user, user.name, user.name)
            chown_children_recursively(user, user.name, user.name)

        collected = user / TURNIN / COLLECTED
        if collected.is_dir():
            shutil.chown(collected, ROOT, ROOT)
            chown_children_recursively(collected, ROOT, ROOT)
            os.chmod(collected, MODE)
            chmod_children_recursively(collected, MODE)

def chown_children_recursively(path: Path, user: str, group: str) -> None:
    subprocess.run(["find", f"{path}", "-xtype", "l", "-exec", "rm", "{}", "\\;"])
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            shutil.chown(os.path.join(root, dir), user, group)
        for file in files:
            shutil.chown(os.path.join(root, file), user, group)

def chmod_children_recursively(path: Path, mode: int) -> None:
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            os.chmod(os.path.join(root, dir), mode)
        for file in files:
            os.chmod(os.path.join(root, file), mode)


if __name__ == "__main__":
    chown_home_folders()
