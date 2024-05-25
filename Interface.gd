extends Control

#FIXME: SWITCH THOSE # LINES WHEN SWITCHING BETWEEN DEVELOPING & EXPORTING
var project_dir = OS.get_executable_path().get_base_dir()
#var project_dir = "PATH/TO/PROJECT/builds"

var MenuOpen: bool = false
var InstallMenuOpen: bool = false
var MessageMenuOpen: bool = false
var SpritesMenuOpen: bool = false
var SettingsMenuOpen: bool = false
var IsPythonInstalled: bool = false



# File paths
var runfile: String = project_dir.path_join("scripts/runfile.py")
var startfile: String = project_dir.path_join("scripts/startfile.bat")
var pythonInstalled: String = project_dir.path_join("scripts/PythonInstalled.bat")
var redisInstalled: String = project_dir.path_join("scripts/RedisInstalled.py")
var configFile: String = project_dir.path_join("scripts/config.txt")

var installRepo: String = project_dir.path_join("scripts/install_repo.bat")
var installPython: String = project_dir.path_join("scripts/install_python.bat")
var installRedis: String = project_dir.path_join("scripts/install_redis.bat")

var installAutogen: String = project_dir.path_join("scripts/install_autogen.py")
var installCustom: String = project_dir.path_join("scripts/install_custom.py")

var database_path: String = project_dir.path_join("infinitefusion-multiplayer/multiplayer/redis/redis-db.py")
var database_info_path: String = project_dir.path_join("infinitefusion-multiplayer/multiplayer/redis/db-info.txt")
var game_path: String = project_dir.path_join("infinitefusion-multiplayer/Game.exe")
var graphics_path: String = project_dir.path_join("infinitefusion-multiplayer/Graphics")

var redis_host: String
var redis_port: String
var redis_pw: String
#var game_path #TODO: Fetch from config

func _on_launch_game_pressed():
	if FileAccess.file_exists(game_path):
		openFile(game_path)
	else:
		if (MenuOpen and !InstallMenuOpen) or !MenuOpen:
			FileDoesNotExistNote()
		elif MenuOpen and InstallMenuOpen:
			_on_install_menu_pressed()
			FileDoesNotExistNote()
	
func _on_start_server_pressed():
	if FileAccess.file_exists(database_path):
		openFile(database_path)
	else:
		if (MenuOpen and !InstallMenuOpen) or !MenuOpen:
			FileDoesNotExistNote()
		elif MenuOpen and InstallMenuOpen:
			_on_install_menu_pressed()
			FileDoesNotExistNote()

func PythonInstalledConfig():
	var exit_code = OS.execute("cmd.exe", ["/C", pythonInstalled])
	#print("Exit code:", exit_code)
	if exit_code == 1:
		print("Python is not installed")
		$InstallMenu/InstallPython/TextureRect.texture = load("res://Images/icons8-exit-96.png")
		IsPythonInstalled = false
		return false
	elif exit_code == 0:
		print("Python is installed")
		$InstallMenu/InstallPython/TextureRect.texture = load("res://Images/icons8-tick-box-48.png")
		RedisInstalledConfig()
		IsPythonInstalled = true
		return true
	else:
		print("There was an error detecting installation of python. exit code: ", exit_code)
		$InstallMenu/InstallPython/TextureRect.texture = load("res://Images/icons8-exit-96.png")
		IsPythonInstalled = false
		return false

func RedisInstalledConfig():
	var exit_code = OS.execute("cmd.exe", ["/C", "start", "/min", "python", redisInstalled])
	if exit_code == 1:
		print("Redis is not installed")
		$InstallMenu/InstallRedis/TextureRect.texture = load("res://Images/icons8-exit-96.png")
		IsPythonInstalled = false
		return false
	elif exit_code == 0:
		print("Redis is installed")
		$InstallMenu/InstallRedis/TextureRect.texture = load("res://Images/icons8-tick-box-48.png")
		IsPythonInstalled = true
		return true
	else:
		print("There was an error fetching exit code from redis_check. exit code: ", exit_code)
		$InstallMenu/InstallRedis/TextureRect.texture = load("res://Images/icons8-exit-96.png")
		IsPythonInstalled = false
		return false

func _ready():
	print("runfile directory: ", runfile)
	print("database_path: ", database_path)
	
	#$MainButtons/VBoxContainer/Wiki.text = runfile
	if !PythonInstalledConfig():
		DownloadPythonNote()

	#IsPythonInstalled = openFile(pythonInstalled)
	#print(IsPythonInstalled)


func DownloadGame():
	pass

func DownloadPythonNote():
	$MessageNote/MessageName.text = "Python required for this step"
	$MessageNote/MessageContents.text = "Please go under Install Menu\nand download python."
	$MessageNote.visible = true
	MenuOpen = true
	MessageMenuOpen = true

func FileDoesNotExistNote():
	$MessageNote/MessageName.text = "File DoesNotExist"
	$MessageNote/MessageContents.text = 'If this is the game / server,\nplease make sure that you have\nInstalled the game inside "Install Menu"\nCorrectly,\nand that Python & Redis are installed'
	$MessageNote.visible = true
	MenuOpen = true
	MessageMenuOpen = true
	

func openFile(script_path):
	if !IsPythonInstalled:
		if MenuOpen and !MessageMenuOpen:
			_on_install_menu_pressed()
		DownloadPythonNote()
		print("Unable to open file, python is not installed.")
		return false
	#var script_path: String = 
	var exit_code = OS.execute("cmd.exe", ["/C", "start", "/min", "python", runfile , script_path])
	if exit_code == OK:
		print("Script ran successfully in new terminal")
		return true
	else:
		print("Failed to run script")
		print("Exit code: ", exit_code)
		return false

func _on_wiki_pressed():
	OS.shell_open("https://github.com/NoamRothschild/infinitefusion-multiplayer/blob/main/readme.md")


func _on_install_menu_pressed():
	if !InstallMenuOpen:
		if MenuOpen:
			$MessageNote.visible = false
			$SettingsMenu.visible = false
			$SpriteMenu.visible = false
			MessageMenuOpen = false
			SettingsMenuOpen = false
			SpritesMenuOpen = false
		MenuOpen = true
		InstallMenuOpen = true
		$InstallMenu.visible = true
		$"InstallMenu/Download Game/Confirm".visible = false
		$"InstallMenu/Download Game/DownloadGameNote".visible = false
		#PythonInstalledConfig()
	else:
		MenuOpen = false
		InstallMenuOpen = false
		$InstallMenu.visible = false
		

#func updateConfig(new_content: String):
#	var config_data = FileAccess.open("user://PIF-MP_config.txt", FileAccess.READ).get_as_text()
#	FileAccess.open("user://PIF-MP_config.txt", FileAccess.WRITE).store_string(config_data + new_content)

func _on_install_python_pressed():
	OS.execute("cmd.exe", ["/C", "start", startfile, installPython])
	PythonInstalledConfig()

func _on_install_redis_pressed():
	openFile(installRedis)


func _on_close_note_pressed():
	MenuOpen = false
	MessageMenuOpen = false
	$MessageNote.visible = false


func _on_close_window_pressed():
	get_tree().quit()


func _on_download_game_pressed():
	if !(FileAccess.file_exists(game_path) and FileAccess.file_exists(database_path)):
		openFile(installRepo)
	else:
		$"InstallMenu/Download Game/Confirm".visible = true
		$"InstallMenu/Download Game/DownloadGameNote".visible = true


func _on_confirm_pressed():
	openFile(installRepo)


func _on_sprite_menu_pressed():
	$InstallMenu.visible = false
	InstallMenuOpen = false
	$SettingsMenu.visible = false
	SettingsMenuOpen = false
	MenuOpen = false
	
	if !IsPythonInstalled:
		DownloadPythonNote()
		return
	
	$MessageNote.visible = false
	MessageMenuOpen = false
	
	if !SpritesMenuOpen:
		$SpriteMenu.visible = true
		SpritesMenuOpen = true
		MenuOpen = true
		var config_data = FileAccess.open(configFile, FileAccess.READ).get_as_text()
		for line in config_data.split("\n"):
			if "autogen:" in line:
				if "false" in line:
					$"SpriteMenu/Autogen sprites/TextureRect".texture = load("res://Images/icons8-exit-96.png")
				elif "true" in line:
					$"SpriteMenu/Autogen sprites/TextureRect".texture = load("res://Images/icons8-tick-box-48.png")
			elif "custom:" in line:
				if "false" in line:
					$"SpriteMenu/Custom sprites/TextureRect".texture = load("res://Images/icons8-exit-96.png")
				elif "true" in line:
					$"SpriteMenu/Custom sprites/TextureRect".texture = load("res://Images/icons8-tick-box-48.png")
	else:
		$SpriteMenu.visible = false
		SpritesMenuOpen = false
		MenuOpen = false

	


func _on_autogen_sprites_pressed():
	if FileAccess.file_exists(game_path):
		openFile(installAutogen) #Game files exist


func _on_custom_sprites_pressed():
	if FileAccess.file_exists(game_path):
		openFile(installCustom) #Game files exist


func _on_settings_pressed():
	if !SettingsMenuOpen:
		$InstallMenu.visible = false
		InstallMenuOpen = false
		$MessageNote.visible = false
		MessageMenuOpen = false
		$SpriteMenu.visible = false
		SpritesMenuOpen = false
		
		SettingsMenuOpen = true
		MenuOpen = true
		$SettingsMenu.visible = true
		
		var database_info = FileAccess.open(database_info_path, FileAccess.READ).get_as_text().split('\n')
		redis_host = database_info[0].replace(" ", "").substr(6).replace("'", "")
		redis_port = database_info[1].replace(" ", "").substr(5)
		redis_pw = database_info[2].replace(" ", "").substr(10).replace("'", "")
		$SettingsMenu/Host.text = redis_host
		$SettingsMenu/Port.text = redis_port
		$SettingsMenu/Password.text = redis_pw
	else:
		$SettingsMenu.visible = false
		SettingsMenuOpen = false
		MenuOpen = false


func _on_open_redis_pressed():
	OS.shell_open("https://redis.io/try-free/")
func _on_host_text_changed(new_text):
	redis_host = new_text
func _on_port_text_changed(new_text):
	redis_port = new_text
func _on_password_text_changed(new_text):
	redis_pw = new_text


func _on_apply_pressed():
	$SettingsMenu.visible = false
	var database_info = FileAccess.open(database_info_path, FileAccess.WRITE)
	var host_line = "host = '" + redis_host + "'"
	var port_line = "port = " + redis_port
	var pw_line = "password = '" + redis_pw + "'"
	database_info.store_string(host_line + '\n' + port_line + '\n' + pw_line)
	$TopNote.text = "Saved changes to database!"
	$TopNote.visible = true
	$TopNote/Timer.start()
	MenuOpen = false
	SettingsMenuOpen = false

func _on_close_menu_pressed():
	$SettingsMenu.visible = false
	SettingsMenuOpen = false
	MenuOpen = false


func _on_timer_timeout():
	$TopNote/Timer.stop()
	$TopNote.visible = false


func _on_sprite_close_menu_pressed():
	MenuOpen = false
	SpritesMenuOpen = false
	$SpriteMenu.visible = false


func _on_close_install_menu_pressed():
	MenuOpen = false
	InstallMenuOpen = false
	$InstallMenu.visible = false