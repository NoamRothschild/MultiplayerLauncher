from os import chdir
from os.path import dirname, abspath, join
chdir(join(dirname(abspath(__file__)), ".."))

import os
import shutil
import subprocess
import stat

#os.chdir(os.path.join(os.getcwd(), 'scripts'))
# Set variables

REPO_URL = "https://gitlab.com/pokemoninfinitefusion/customsprites"
LOCAL_REPO_PATH = os.path.join(os.getcwd(), "custom-fusion-sprites")
TARGET_DIR = os.path.join(os.getcwd(), "infinitefusion-multiplayer", "Graphics")
GIT_PATH = os.path.join(os.getcwd(), 'scripts', 'REQUIRED_BY_INSTALLER_UPDATER', 'cmd', 'git.exe')
CONFIG_PATH = os.path.join(os.getcwd(), 'scripts', 'config.txt')

# Function to remove a directory and its contents
def remove_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)

# Clone the repository
if os.path.exists(LOCAL_REPO_PATH):
    print("Deleting existing repository directory...")
    remove_directory(LOCAL_REPO_PATH    )


print("Cloning repository...")
subprocess.run([GIT_PATH, "clone", REPO_URL, LOCAL_REPO_PATH])


print("Moving files and folders...")

dest = os.path.join(TARGET_DIR, 'CustomBattlers')
remove_directory(dest)
shutil.move(os.path.join(LOCAL_REPO_PATH, 'CustomBattlers'), dest)
os.makedirs(os.path.join(dest, 'customBaseSprites'))
os.makedirs(os.path.join(dest, 'indexed'))
# Moved CustomBattlers contents to the target directory

dest = os.path.join(TARGET_DIR, 'Other')
for item in os.listdir(os.path.join(LOCAL_REPO_PATH, 'Other')):
    local_path = os.path.join(LOCAL_REPO_PATH, 'Other', item)
    if os.path.isdir(local_path):
        print("Folder:", item)
        shutil.move(local_path, os.path.join(TARGET_DIR, item))
    else:
        print("File:", item)
        shutil.move(local_path, os.path.join(TARGET_DIR, item))
remove_directory(os.path.join(LOCAL_REPO_PATH, 'Other'))
# Moved Other's contents to the target directory

f = open(CONFIG_PATH, 'r').read().replace('custom: false', 'custom: true')
with open(CONFIG_PATH, 'w') as config:
    config.write(f)

input("Done.")
exit()