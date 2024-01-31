# OS Course 402-1, Project
# Amirhosein Farhangian
# Arian Jafari

import subprocess
from pathlib import Path
import os
import re

def get_help():
    print(
        "prev       \t\t-> get previous command\n"
        "history    \t\t-> print command history\n"
        "del-history\t\t-> delete command history\n"
        "|          \t\t-> execute in pipe mode\n"
        "=>         \t\t-> store command in a file\n"
        "<=         \t\t-> run commands from a file\n"
        ">          \t\t-> store command output in a file\n"
        "<          \t\t-> run command via options which are stored in a file"
    )

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

def execute_command_via_file(command:str):
    command, input_file = command.split("<=")
    with open(input_file.strip(), "r") as file:
        file_content = file.read()
        commands = file_content.replace("\n", ";")
    try:
        result = subprocess.run(
            commands,
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
        print(e)

def store_command_in_specified_file(command:str):
    command, output_file = command.split("=>")
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
        print(e)

    try:
        os.system(f"rm {output_file}; clear")
    except:
        # file not found!
        pass

    with open(output_file.strip(), "w") as file:
        file.write(command)
    print("command successfully written in the specified file.")




def output_redirection_execution(command:str):
    command, output_file = command.split(">")
    try:
        result = subprocess.run(
            command,
            shell=True,
            text=True, 
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError as e:
        print(e)

    if result.stderr:
        print(f"fail: {result.stderr}")
    else:
        try:
            os.system(f"rm {output_file}; clear")
        except:
            # file not found!
            pass
        with open(output_file.strip(), "w") as file:
            file.write(result.stdout)
        print("command output successfully written in the specified file.")

def input_redirection_execution(command:str):
    command, input_file = command.split("<")
    
    with open(input_file.strip(), "r") as file:
        try:
            result = subprocess.run(
                    command,
                    stdin=file,
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
            print(e)


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
        print(e)


def get_and_run_command():
    while True:
        # get input from user
        command = input(f"→ {relatvie_path} @ ")

        # if user want to exit
        if command == "exit":
            break
        
        # if command is prev, get previous command
        elif command == "prev":
            command = get_prev_command(2)
            normal_execution(command)

        elif re.match(r"^prev \d+$", command):
            command, command_idx = command.split(" ")
            command = get_prev_command(command_idx=int(command_idx))
            normal_execution(command)

        # get help 
        elif command == "ash-help":
            get_help()

        # get history command
        elif command == "history":
           get_history(count=5+1) 
        elif re.match(r"history \d+$", command):
            command, count = command.split(" ")
            get_history(count=int(count)+1)

        # if command is delete history
        elif command == "del-history":
           del_history()
        
        # handling pipe
        elif "|" in command:
            pipe_execution(command)
        # normal execution
        elif "<=" in command:
            execute_command_via_file(command)
        elif "=>" in command:
            store_command_in_specified_file(command)
        elif ">" in command:
            output_redirection_execution(command)
        elif "<" in command:
            input_redirection_execution(command)
        else:
            normal_execution(command)

        # write the command in the history
        with open("cmds_history.txt", "a") as file:
            file.write(f"{command}\n")

        
if __name__ == "__main__":
    # get relative path to show on the prompt
    path = Path.cwd()
    relatvie_path = path.parts[-1]
    os.system("clear")
    print("run ash-help for command list.")
    # Get and Run command
    get_and_run_command()

