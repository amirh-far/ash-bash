import subprocess
from pathlib import Path

def get_last_command():
    with open("prev_cmds.txt", "r"):
        # Move to the end of the file
        file.seek(0, 2)

        # Get the current position in the file
        current_position = file.tell()

        # Move backward to find the beginning of the last line
        while current_position > 0:
            file.seek(current_position - 1)
            char = file.read(1)
            print(char)

            # Check if the character is a newline character
            if char == '\n':
                break

            # Move the cursor to the previous position
            current_position -= 1

        # Move the cursor to the beginning of the last line
    file.seek(current_position + 1)








if __name__ == "__main__":
    # open previous commands file to append new commands
    file = open("prev_cmds.txt", "a+")

    # get relative path to show on the prompt
    path = Path.cwd()
    relatvie_path = path.parts[-1]

    while True:
        command = input(f"→ {relatvie_path} @ ")

        # if user want to exit
        if command == "exit":
            break

        elif command == "^[[A":
            last_cmd = get_last_command()
    
            
        else:
            file.write(f"{command}\n")

        if command == "history":
            with open("prev_cmds.txt", "r") as file:
                prev_commands_list = file.read().split("\n")
                for cmd in prev_commands_list:
                    print(cmd)
            

        # run the commnad
        res = subprocess.run(command, shell=True, text=True, capture_output=True)
        # print the result of command that has been run
        print(res.stdout)
