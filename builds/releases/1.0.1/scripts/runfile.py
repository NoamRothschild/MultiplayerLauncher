if __name__ == "__main__":
    from os import system
    from sys import argv
    from subprocess import Popen
    arg = argv[1]
    #print(f"Executing {arg}...")
    def run_in_new_terminal(command):
        terminal_command = f'start cmd /c "{command}"'
        Popen(terminal_command, shell=True)

    if arg.endswith('.py'):
        run_in_new_terminal(f"python {arg}")
    else:
        Popen(arg, shell=True)

    #print("Finished process")
    exit()
