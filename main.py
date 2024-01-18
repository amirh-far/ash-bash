import subprocess
from pathlib import Path
import os
import re

def get_prev_command(command_idx):
    with open('cmds_history.txt') as file:
        commands_history = file.read().split("\n")
        # Checking if file is empty
        if commands_history:
            if command_idx == 2:
                print(f"\r→ {relatvie_path} @ {commands_history[-command_idx]}", end="")
                return commands_history[-2]
            else:
                print(f"\r→ {relatvie_path} @ {commands_history[command_idx]}", end="")
                return commands_history[command_idx]
        else:
            return None
        
def get_history(count):
    with open("cmds_history.txt", "r") as file:
        file.seek(0)
        prev_commands_list = file.read().split("\n")
        history_length = len(prev_commands_list)
        if count < history_length:
            idx = history_length - count
            print()
            
            for cmd in prev_commands_list[history_length - count: history_length - 1]:
                print(f"{idx}| {cmd}")
                idx += 1
        else:
            idx = 0
            for cmd in prev_commands_list[: history_length - 1]:
                print(f"{idx}| {cmd}")
                idx += 1


            

def del_history():
    os.system("rm cmds_history.txt")
    print("command history deleted.")

def pipe_execution(command:str):
    command_1, command_2 = command.split("|")

    process_1 = subprocess.Popen(
        command_1,
        stdout=subprocess.PIPE,
        text=True,
        shell=True
    )
    process_2 = subprocess.Popen(
        command_2,
        stdin=process_1.stdout,
        stdout=subprocess.PIPE,
        shell=True,
        text=True
    )
    output, _ = process_2.communicate()
    print(output)


def normal_execution(command:str):
    try:
        result = subprocess.run(
            command,
            shell=True,
            text=True, 
            check=True,
            capture_output=True
        )

        if result.stderr:
            print(result.stderr)
        else:
            print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("Error Output (stderr):", e.stderr)


def get_and_run_command():
    while True:
        command = input(f"→ {relatvie_path} @ ")

        # if user want to exit
        if command == "exit":
            break
        
        # if command is prev, get previous command
        if command == "prev":
            command = get_prev_command(2)
        elif re.match(r"^prev \d+$", command):
            command, command_idx = command.split(" ")
            command = get_prev_command(command_idx=int(command_idx))
        
        # get history command
        if command == "history":
           get_history(count=5+1) 
        elif re.match(r"history \d+$", command):
            command, count = command.split(" ")
            get_history(count=int(count)+1)

        # if command is delete history
        if command == "del-history":
           del_history()
        
        # handling pipe
        if "|" in command:
            pipe_execution(command)
        # normal execution
        else:
            normal_execution(command)

        # write the command in the history
        with open("cmds_history.txt", "a") as file:
            file.write(f"{command}\n")

        
if __name__ == "__main__":
    # get relative path to show on the prompt
    path = Path.cwd()
    relatvie_path = path.parts[-1]

    # Get and Run command
    os.system("clear")
    get_and_run_command()

