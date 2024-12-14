from os import path
import re
from json import loads, load, dumps, dump

class GameOption:
    def __init__(self, name: str = '', state: bool = True, INTL: str = None):
        self.name = name
        self.state = state
        self.INTL = name if not INTL else INTL
    
    def __repr__(self):
        return str({"name": self.name, "state": self.state, "INTL": self.INTL})
    
    def __iter__(self):
        yield from self.__dict__.items()

class GameSettings:
    def __init__(self, game_path: str):
        self.path = game_path
    
    def get_ui_x(self, rel_path: str, start_at: str, break_at: str = "commands[cmd", snake_case = True) -> list[GameOption]:
        ui_x = path.join(self.path, rel_path)

        is_enabled = lambda option, lines: not (f"#commands[cmd{'_' if snake_case else ''}{option}" in ''.join(lines))

        options = []
        with open(ui_x, 'r') as f:
            break_chr = '_' if snake_case else 'd'
            lines = f.readlines()
            i = 0
            while len(lines) > i and start_at not in lines[i-1]:
                i+= 1; continue
            for line_idx in range(i, len(lines)):
                line: str = lines[line_idx]
                if break_at in line:
                    break # End of setting up settings
                if ('cmd' not in line) and ("-1" not in line):
                    continue
                start = -1
                end = -1
                for idx, chr in enumerate(line):
                    if start == -1 and chr == break_chr: start = idx + 1; continue
                    if start != -1 and chr == ' ': 
                        end = idx
                        break
                option_name = line[start:end]
                options.append( GameOption(name=option_name, state=is_enabled(option_name, lines)) )
        
        self.get_ui_names(rel_path, options, start_at, snake_case)
        return options

    def get_ui_names(self, rel_path: str, setting_names: list[GameOption], start_at: str, snake_case = True) -> None:
        ui_x = path.join(self.path, rel_path)
        prefix = "commands[cmd"
        suffix = "_INTL"
        break_chr = '_' if snake_case else 'd'

        with open(ui_x, 'r') as f:
            lines = f.readlines()
            i = 0
            while len(lines) > i and start_at not in lines[i-1]:
                i+= 1; continue
            for line_idx in range(i, len(lines)):
                line: str = lines[line_idx]
                if (prefix not in line) or (suffix not in line):
                    continue
                start = -1
                end = -1
                for idx in range(line.index('['), len(line)):
                    chr = line[idx]
                    if start == -1 and chr == break_chr: start = idx + 1; continue
                    if start != -1 and chr == ' ': 
                        end = idx
                        break
                option_name = line[start:end]
                for option in setting_names:
                    if option.name == option_name:
                        option.INTL = re.findall(r'_INTL\((["\'].*?["\'])\)', line)[0][1:-1]
                        break

    def set_ui_x(self, rel_path: str, new_options: list[GameOption], snake_case = True) -> None:
        ui_load = path.join(self.path, rel_path)
        pattern = f"commands[cmd{'_' if snake_case else ''}" + "{}"

        is_enabled = lambda option, file: not ('#'+pattern.format(option) in file)

        res = open(ui_load, 'r').read()
        for option in new_options:
            if option.state: # enable option
                res = res.replace('#'+pattern.format(option.name), pattern.format(option.name))
                continue
            if is_enabled(option.name, res): # disable option
                res = res.replace(pattern.format(option.name), '#'+pattern.format(option.name))

        with open(ui_load, 'w') as f:
            f.write(res)
    
    def set_multiplayer_credentials(self, credentials: dict, error_func: callable):
        file_path = path.join(self.path, 'Multiplayer', 'credentials.json')
        if not path.exists(file_path):
            error_func()
            raise Exception("Multiplayer directory does not exist!")

        if not credentials.get('host') or not credentials.get('port') or not credentials.get('password'):
            error_func()
            raise Exception("credentials have some issues!")

        with open(file_path, 'w') as f:
            f.write(dumps(credentials))
    
    def get_multiplayer_credentials(self, error_func: callable) -> dict:
        file_path = path.join(self.path, 'Multiplayer', 'credentials.json')
        if not path.exists(file_path):
            error_func()
            raise Exception("Multiplayer directory does not exist!")
        return load(open(file_path))

def main():
    '''
    #game_settings = GameSettings(r'D:\\Program-Files\\PokemonEssentials\\inf-fusion\\gh\\Electron-FusionLauncher\\fusionlauncher\\src\\KIF')
    #game_settings = GameSettings(r'D:\Program-Files\PokemonEssentials\inf-fusion\gh\kurayshinyrevamp')
    game_settings = GameSettings('D:\\Program-Files\\PokemonEssentials\\inf-fusion\\gh\\DEBUG')

    #"""
    options: list[GameOption] = game_settings.get_ui_x(r'Data\Scripts\051_AddOns\MultiSaves.rb', "SaveData::AUTO_SLOTS + SaveData::MANUAL_SLOTS")
    print(options)
    exit()
    #for option in options:
    #    option.state = True

    #game_settings.set_ui_x(r'Data\Scripts\051_AddOns\MultiSaves.rb', options)
    #"""
    #print(game_settings.get_ui_x(r'Data\Scripts\051_AddOns\MultiSaves.rb', "SaveData::AUTO_SLOTS + SaveData::MANUAL_SLOTS"))
    #print(game_settings.get_ui_load())
    #print()

    """
    pause_options: list[GameOption] = game_settings.get_ui_x(r'Data\Scripts\016_UI\001_UI_PauseMenu.rb', "def pbStartPokemonMenu", snake_case=False)
    for option in pause_options:
        print(option)
    #    option.state = False
    #game_settings.set_ui_x(r'Data\Scripts\016_UI\001_UI_PauseMenu.rb', pause_options, snake_case=False)
    """

    #options = {'continue': True, 'new_game': True, 'options': True, 'language': True, 'mystery_gift': True, 'debug': True, 'quit': True, 'doc': True, 'discord': True, 'pifdiscord': True, 'wiki': True}
    #game_settings.set_ui_load(options)
    '''

if __name__ == "__main__":
    main()