import os
import shutil
import subprocess

#os.chdir(os.path.join(os.getcwd(), 'scripts'))
# Set variables

REPO_URL = "https://gitlab.com/pokemoninfinitefusion/autogen-fusion-sprites"
LOCAL_REPO_PATH = os.path.join(os.getcwd(), "autogen-fusion-sprites")
TARGET_DIR = os.path.join(os.getcwd(), "infinitefusion-multiplayer", "Graphics", "Battlers")
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


# Move Battlers contents to the target directory
print("Moving files and folders...")
battlers_dir = os.path.join(LOCAL_REPO_PATH, "Battlers")
for folder in os.listdir(battlers_dir):
    src = os.path.join(battlers_dir, folder)
    if os.path.isdir(src):
        dest = os.path.join(TARGET_DIR, folder)
        remove_directory(dest)  # Remove existing folder in target directory
        shutil.move(src, TARGET_DIR)

f = open(CONFIG_PATH, 'r').read().replace('autogen: false', 'autogen: true')
with open(CONFIG_PATH, 'w') as config:
    config.write(f)

print("Done.")
