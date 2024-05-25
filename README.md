# PIF MultiplayerLauncher
An easy to install launcher for my [PIF Multiplayer project](https://github.com/NoamRothschild/infinitefusion-multiplayer)

![MultiplayerLauncher(PIF)](https://github.com/NoamRothschild/MultiplayerLauncher/assets/98104540/ee687fd7-4f34-4011-adf1-7fef7b50ed7f)

This launcher will save you from all of the troubles when installing my [Multiplayer Extension](https://github.com/NoamRothschild/infinitefusion-multiplayer), not only making the installing process faster, but also simpler.

## How to install:
- Go to the [releases tab](https://github.com/NoamRothschild/MultiplayerLauncher/releases) and install the latest PIF-MultiplayerLauncher.zip
- After done installing, extract & open up PIF-MultiplayerLauncher.exe
  
If you see a Microsoft Defender SmartScreen warning when opening our app, please follow these steps to proceed:
1. Click on "More info" in the warning dialog.
2. Click "Run anyway" to start the app.

This Microsoft Defender SmartScreen message appears because the app is not recognized by Microsoft's database and lacks a verified publisher, do not worry.

### What to-do
- Note: before we start, please do not close any terminals (the black windows with text) while they are going unless their last line is 'Press any key to exit' or are empty even after a few minuets.

After you have opened the app, you can jump into the "Install Menu" and download Python, and also redis once thats done.
After that, click on Download Game to install the game.

If you want to play preloaded, you can then go onto the "Sprite Menu" & install both the autogenerated sprites & the custom sprites (you can run both in parallel)

### Im done installing! how do I start?

Unfortunately, you will need to do 1 more step that cannot be automated.
- Click on "Open redis" inside the "Settings", and sign up and create a database for free (pick the closest to you).
- After you are done, you can click on your database and then press 'connect' under endpoint in the databases list.
- Select 'Redis Client' and select 'Python'
- Copy the host, port & password (press on the eye icon to show) to your app and click on 'apply changes'
- Make sure to send your friend those same credentials (Both players need to put the same database information inside the settings menu)

## We are done!
- all you need to do right now is start up the game. this may take some time on your first launch.
- After the game was opened and a save was entered, go inside the game settings, make sure DEBUG is set to true in case any errors occur, and set your player number
- **The player MUST be different on each player, 1 player is num1 and the other is num2, not doing so will cause the program to not work**
- You can now exit the menu & open up the server from the Launcher. the server must be up & running at all times when playing.
  
# Have fun!
