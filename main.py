from os import chdir, getcwd, makedirs, listdir
from os.path import dirname, abspath, join, exists

import webview.dom
import webview.dom.element
chdir(dirname(abspath(__file__)))
# -----------------------------------------------------
from game_settings import GameSettings, GameOption

from flask import Flask, render_template, send_file
import webview
from subprocess import run, Popen, PIPE, CREATE_NO_WINDOW
import json
from shutil import rmtree

FLASK = Flask(__name__, static_folder='./Frontend/static', template_folder='./Frontend')
FLASK.config['Image_Display'] = './Frontend/static/Image-Display/'
MAIN_WIN: webview.Window | None = None
GIT_PATH = join('./REQUIRED_BY_INSTALLER', 'cmd', 'git.exe')

CONFIG = {"Game-Path": None}
if not exists('./config/config.json'):
    makedirs('config', exist_ok=True)
    open('./config/config.json', 'w').write(json.dumps({"Game-Path": None}))
else:    
    try:
        CONFIG = json.load(open('./config/config.json'))
    except json.JSONDecodeError as e:
        print("Json decode error")
        exit(1)

# -------------- Register index.html & image-display paths ---------------------
@FLASK.route("/")
def main_route():
    return render_template('index.html')

@FLASK.route("/settings")
def settings_route():
    return render_template('settings.html')

@FLASK.route("/Image-Display/<image>")
def get_image(image):
    # Path treversal patching
    if any(illegal in image for illegal in ["..", "/", "\\"]):
        return send_file(join(FLASK.config['Image_Display'], 'image1.png'))
    return send_file(join(FLASK.config['Image_Display'], image))

class API():
    def closeWin(self):
        global MAIN_WIN
        MAIN_WIN.destroy()

    def minWin(self):
        global MAIN_WIN
        MAIN_WIN.minimize()
    
    def git_exists():
        return run([GIT_PATH, '--version'], stdout=PIPE, stderr=PIPE, text=True, creationflags=CREATE_NO_WINDOW).returncode == 0

    
    def log(self, value):
        print(value)
    
    class settings:

        @classmethod
        def set_contents(self, contents: str, title: str):
            global MAIN_WIN
            MAIN_WIN.dom.get_element('#options').empty()
            MAIN_WIN.evaluate_js(f'document.querySelector("#option-title").innerHTML = `{title}`;')
            MAIN_WIN.evaluate_js(f'document.querySelector("#options").innerHTML = `{contents}`;')
        
        @classmethod
        def multiplayer_config(self):
            global FLASK
            multiplayer_html = open(join(FLASK.template_folder, 'multiplayer-config.html'), 'r').read()

            global CONFIG
            game_settings = GameSettings(CONFIG["Game-Path"])
            cred = game_settings.get_multiplayer_credentials(lambda: MAIN_WIN.create_confirmation_dialog("Failed while trying to store credentials", "Game version does not support multiplayer!\nEither an old version or multiplayer has not been released yet!"))

            self.set_contents(multiplayer_html, "Multiplayer - Config")

            MAIN_WIN.evaluate_js(f'document.querySelector("#host").value = "{cred.get("host", '')}";')
            MAIN_WIN.evaluate_js(f'document.querySelector("#port").value = "{cred.get("port", '')}";')
            MAIN_WIN.evaluate_js(f'document.querySelector("#password").value = "{cred.get("password", '')}";')
        
        @classmethod
        def start_menu(self):
            global FLASK, CONFIG, MAIN_WIN
            start_menu_html = open(join(FLASK.template_folder, 'start-menu.html'), 'r').read()
            self.set_contents(start_menu_html, "Game - Start Menu")

            game_settings = GameSettings(CONFIG["Game-Path"])
            options: list[GameOption] = game_settings.get_ui_x(r'Data\Scripts\051_AddOns\MultiSaves.rb', "SaveData::AUTO_SLOTS + SaveData::MANUAL_SLOTS")

            container = MAIN_WIN.dom.create_element("<div id='options-box'></div>", MAIN_WIN.dom.get_element('#options'))
            element = """<div id='OPTION-{}'>{}{}</div>"""
            button = '<input type="checkbox" name="checkbox" class="cm-toggle" {}>'

            for option in options:
                checked = "checked" if option.state else ""
                MAIN_WIN.dom.create_element(element.format(option.name, button.format(checked), f'<span class="menu-option">{option.INTL}</span>'), container)
        
        @classmethod
        def pause_menu(self):
            global FLASK, CONFIG, MAIN_WIN
            start_menu_html = open(join(FLASK.template_folder, 'pause-menu.html'), 'r').read()
            self.set_contents(start_menu_html, "Game - Pause Menu")

            game_settings = GameSettings(CONFIG["Game-Path"])
            options: list[GameOption] = game_settings.get_ui_x(r'Data\Scripts\016_UI\001_UI_PauseMenu.rb', "def pbStartPokemonMenu", snake_case=False)

            container = MAIN_WIN.dom.create_element("<div id='options-box'></div>", MAIN_WIN.dom.get_element('#options'))
            element = """<div id='OPTION-{}'>{}{}</div>"""
            button = '<input type="checkbox" name="checkbox" class="cm-toggle" {}>'

            for option in options:
                checked = "checked" if option.state else ""
                MAIN_WIN.dom.create_element(element.format(option.name, button.format(checked), f'<span class="menu-option">{option.INTL}</span>'), container)

        @classmethod
        def game_dir(self):
            global FLASK, CONFIG, MAIN_WIN
            start_menu_html = open(join(FLASK.template_folder, 'game-dir.html'), 'r').read()
            self.set_contents(start_menu_html, "Launcher - Game directory")

        @classmethod
        def apply(self):
            global MAIN_WIN
            global CONFIG
            game_settings = GameSettings(CONFIG["Game-Path"])
            open_option: str = MAIN_WIN.dom.get_element('#option-title').node['innerHTML'].strip()
            match open_option:
                case "Multiplayer - Config":
                    host: str = MAIN_WIN.evaluate_js(f'document.querySelector("#host").value;').strip()
                    tmp = MAIN_WIN.evaluate_js(f'document.querySelector("#port").value;')
                    port: int = int(tmp) if tmp != '' else '0'
                    del tmp
                    password: str = MAIN_WIN.evaluate_js(f'document.querySelector("#password").value;').strip()
                    #print(f"{host=}\n{port=}\n{password=}")

                    if not host.startswith('redis-') or not host.endswith('redis-cloud.com'):
                        MAIN_WIN.create_confirmation_dialog("Error saving credentials", "Invalid host domain was provided.")
                        raise Exception("Invalid host given.")
                    if port == 0 or host == '' or password == '':
                        MAIN_WIN.create_confirmation_dialog("Error saving credentials", "Not all credentials given.")
                        raise Exception("Not all credentials given.")
                    
                    game_settings.set_multiplayer_credentials(
                        {
                         "host": host, 
                         "port": port,
                         "password": password
                        }, lambda: MAIN_WIN.create_confirmation_dialog("Failed while trying to store credentials", "Game version does not support multiplayer / credentials have issues.")
                    )
                    print("Updated multiplayer config!")
                case "Launcher - Game directory":
                    print("Launcher - Game dir!")
                case "Game - Start Menu":
                    captured_settings: list = MAIN_WIN.dom.get_element('#options-box').children
                    res = []
                    for setting in captured_settings:
                        name = setting.id.replace('OPTION-', '')
                        checked = setting.children[0].node["checked"]
                        res.append( GameOption(name=name, state=checked) )
                    game_settings.set_ui_x(r'Data\Scripts\051_AddOns\MultiSaves.rb', res)
                    print("Updated start menu config!")
                case "Game - Pause Menu":
                    captured_settings: list = MAIN_WIN.dom.get_element('#options-box').children
                    res = []
                    for setting in captured_settings:
                        name = setting.id.replace('OPTION-', '')
                        checked = setting.children[0].node["checked"]
                        res.append( GameOption(name=name, state=checked) )
                    game_settings.set_ui_x(r'Data\Scripts\016_UI\001_UI_PauseMenu.rb', res, snake_case=False)
                    print("Updated pause menu config!")
                case _:
                    print("Whoops...", open_option)

    class game:

        @classmethod
        def exists(self):
            global CONFIG
            game_path = CONFIG.get("Game-Path", None)
            return exists(CONFIG["Game-Path"]) and ".git" in listdir(game_path) and "Game.exe" in listdir(game_path)

        @classmethod
        def open_folder(self):
            global MAIN_WIN
            global CONFIG
            if not exists(CONFIG.get("Game-Path", '')):
                MAIN_WIN.create_confirmation_dialog("Failed to open folder", "Game not installed!\nPlease Install Game.")
                return
            Popen('explorer "{}"'.format(CONFIG["Game-Path"]), creationflags=CREATE_NO_WINDOW)

        @classmethod
        def open_features(self):
            global MAIN_WIN
            MAIN_WIN.create_confirmation_dialog("SOON - Features", "This button will open up the features section in the future!")

        @classmethod
        def open_settings(self):
            global MAIN_WIN
            if not API.game.exists():
                MAIN_WIN.create_confirmation_dialog("Failed to open folder", "Game not installed!\nPlease Install Game.")
                return
            MAIN_WIN.evaluate_js("window.location.href='settings';")

        @classmethod
        def game_state(self, src: str = "main"):
            global MAIN_WIN
            global CONFIG
            button = MAIN_WIN.dom.get_element('#play-button')
            extra_data_button = MAIN_WIN.dom.get_element('#Extra-info')

            if src == "main" and extra_data_button.text == "Up to date!":
                button.attributes['onclick'] = 'pywebview.api.game.launch();'
                return

            game_path = CONFIG.get("Game-Path", None)
            if not game_path:
                button.text = "Download Game"
                button.attributes['onclick'] = 'pywebview.api.game.download();'
                extra_data_button.text = "🔗 Link existing game"
                extra_data_button.attributes['onclick'] = 'pywebview.api.game.link_game();'
                return
            if not API.game.exists():
                button.text = "Game folder found but damaged (Re-Install)"
                extra_data_button.text = "🔗 Link existing game"
                extra_data_button.attributes['onclick'] = 'pywebview.api.game.link_game();'
                button.attributes['onclick'] = 'pywebview.api.game.download();'
                return
            

            extra_data_button.text = "Checking version..."

            if not API.git_exists():
                button.text = "Git not installed!"
                extra_data_button.text = "Please install git."
                button.attributes['onclick'] = ''
                extra_data_button.attributes['onclick'] = ''
                return
            
            run(f"{GIT_PATH} fetch origin release".split(' '), capture_output=True, text=True, cwd=game_path, creationflags=CREATE_NO_WINDOW)
            hash1 = run(f"{GIT_PATH} rev-parse origin/release".split(' '), capture_output=True, text=True, cwd=game_path, creationflags=CREATE_NO_WINDOW).stdout
            hash2 = run(f"{GIT_PATH} rev-parse HEAD".split(' '), capture_output=True, text=True, cwd=game_path, creationflags=CREATE_NO_WINDOW).stdout

            if hash1 != hash2:
                button.text = "New game update"
                extra_data_button.text = "Click to update"
                extra_data_button.attributes['onclick'] = 'pywebview.api.game.update();'
                button.attributes['onclick'] = ''
                return
            
            button.text = "Play"
            extra_data_button.text = "Up to date!"
            button.attributes['onclick'] = 'pywebview.api.game.launch();'

        @classmethod
        def link_game(self):
            global MAIN_WIN
            button = MAIN_WIN.dom.get_element('#play-button')

            game_folder = MAIN_WIN.create_file_dialog(dialog_type=webview.FOLDER_DIALOG, directory='', allow_multiple=False)[0]
            if not ".git" in listdir(game_folder) or "Game.exe" not in listdir(game_folder):
                button.text = "Game directory invalid"
                button.attributes['onclick'] = 'pywebview.api.game.link_game();'
                return
            
            global CONFIG
            button.text = "Play"
            button.attributes['onclick'] = 'pywebview.api.game.game_state();'
            CONFIG["Game-Path"] = game_folder
        
        @classmethod
        def launch(self):
            global CONFIG
            print("Launching game!")
            cmd = '"' + join(CONFIG["Game-Path"], 'Game.exe') + '"'
            Popen(cmd, creationflags=CREATE_NO_WINDOW)
            API.closeWin(self)
        
        @classmethod
        def update(self):
            # run fetch before else won't work
            global CONFIG
            global MAIN_WIN

            extra_data_button = MAIN_WIN.dom.get_element('#Extra-info')
            button = MAIN_WIN.dom.get_element('#play-button')
            extra_data_button.text = "fetching updates..."
            
            if not API.git_exists():
                button.text = "Git not installed!"
                extra_data_button.text = "Please install git."
                button.attributes['onclick'] = ''
                extra_data_button.attributes['onclick'] = ''
                return
            
            run(f"{GIT_PATH} reset --hard origin/release".split(' '), cwd=CONFIG["Game-Path"], creationflags=CREATE_NO_WINDOW)
            extra_data_button.text = "Up to date!"
            button.text = "Play"
            button.attributes['onclick'] = 'pywebview.api.game.game_state();'

        @classmethod
        def download(self):
            global MAIN_WIN
            extra_data_button = MAIN_WIN.dom.get_element('#Extra-info')
            button = MAIN_WIN.dom.get_element('#play-button')

            button.text = "Installing... Please do not close"

            extra_data_button.attributes['onclick'] = ''
            button.attributes['onclick'] = ''

            if exists('./GameFiles'):
                extra_data_button.text = 'Deleting existing game folder'
                rmtree('./GameFiles')

            if not API.git_exists():
                button.text = "Git not installed!"
                extra_data_button.text = "Please install git."
                button.attributes['onclick'] = ''
                extra_data_button.attributes['onclick'] = ''
                return

            extra_data_button.text = 'Initializing git'
            makedirs('./GameFiles')
            run(f'{GIT_PATH} init .', cwd='./GameFiles', creationflags=CREATE_NO_WINDOW)
            extra_data_button.text = 'Adding origin...'
            run(f'{GIT_PATH} remote add origin https://github.com/kurayamiblackheart/kurayshinyrevamp.git', cwd='./GameFiles', creationflags=CREATE_NO_WINDOW)
            extra_data_button.text = 'fetching latest release'
            run(f'{GIT_PATH} fetch origin release', cwd='./GameFiles', creationflags=CREATE_NO_WINDOW)
            extra_data_button.text = 'placing files...'
            run(f'{GIT_PATH} reset --hard origin/release', cwd='./GameFiles', creationflags=CREATE_NO_WINDOW)

            global CONFIG
            CONFIG["Game-Path"] = join(getcwd(), 'GameFiles')
            button.text = "Play"
            extra_data_button.text = "Up to date!"
            button.attributes['onclick'] = 'pywebview.api.game.launch();'

def main():
    print("Running from directory " + getcwd())

    global MAIN_WIN
    MAIN_WIN = webview.create_window('Kuray Infinite Fusion Launcher', url=FLASK, 
                                    width = 1024, height = 642, 
                                    frameless=True, easy_drag=True, 
                                    js_api=API()
                                    )
    webview.start()

    global CONFIG
    if json.dumps(CONFIG) != open('./config/config.json', 'r').read():
        open('./config/config.json', 'w').write(json.dumps(CONFIG))
        # Update config if changed.


if __name__ == "__main__":
    main()