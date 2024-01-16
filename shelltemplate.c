#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <sys/types.h>



#define MAX_LINE 80
#define MAX_ARGS 40
#define HISTORY_PATH ".history"

// Flags and variables for file I/O, piping, etc.
int p_wait;
int in_file, out_file;
int saved_in, saved_out;
int in, out;
int pipe_ind;
int save_c;

// Function to parse user input into command and arguments
void parseInput(char *command, char **args)
{
  // Implementation for parsing input
}

// Function to check flags related to file I/O and piping
void checkFlags(char **args)
{
  // Implementation for checking flags
}

// Function to manage command history
void manageHistory(char **args)
{
  // Implementation for managing history
}

// Function to execute a command
void execute(char **args)
{
  // Implementation for executing a command
}

// Function to save a command in history
void saveCommand(char *command)
{
  // Implementation for saving a command in history
}

// Main function
int main(void)
{
  char command[MAX_LINE];
  char last_command[MAX_LINE];
  char parse_command[MAX_LINE];
  char *args[MAX_ARGS];
  char *argsp1[MAX_ARGS], *argsp2[MAX_ARGS];
  int should_run = 1, history = 0;
  int alert;
  int pipech[2];

  while (should_run)
  {
    // Displaying shell prompt
    printf("OSshell$ ");
    fflush(stdout);

    // Getting user input
    fgets(command, MAX_LINE, stdin);

    // Resetting flags and variables
    p_wait = 1;
    alert = 0;
    out_file = in_file = -1;
    pipe_ind = -1;
    save_c = 1;

    // Copying the command for history and parsing
    strcpy(parse_command, command);
    parseInput(parse_command, args);

    // Checking for empty command
    if (args[0] == NULL || !strcmp(args[0], "\0") || !strcmp(args[0], "\n"))
      continue;

    // Handling exit command
    if (!strcmp(args[0], "exit"))
    {
      should_run = 0;
      continue;
    }

    // Handling history command
    if (!strcmp(args[0], "!!"))
    {
      if (history)
      {
        printf("%s", last_command);
        strcpy(command, last_command);
        strcpy(parse_command, command);
        parseInput(parse_command, args);
      }
      else
      {
        printf("No commands in history \n");
        continue;
      }
    }

    // Checking flags for file I/O and piping
    checkFlags(args);

    // Handling input file
    if (in_file != -1)
    {
      // Implementation for handling input file
    }

    // Handling output file
    if (out_file != -1)
    {
      // Implementation for handling output file
    }

    // Handling piping
    if (pipe_ind != -1)
    {
      // Implementation for handling piping
    }

    // Executing the command
    if (!alert && should_run)
    {
      // Handling history command execution
      if (!strcmp(args[0], "history"))
        manageHistory(args);
      else
      {
        // Handling stop/continue commands
        if (!strcmp(args[0], "stop") || !strcmp(args[0], "continue"))
        {
          // Implementation for handling stop/continue
        }

        // Forking a new process for command execution
        if (fork() == 0)
        {
          // Handling piping in child process
          if (pipe_ind != -1)
          {
            // Implementation for piping
          }
          else
            execute(args);
        }
        else
        {
          // Waiting for the child process to finish
          if (p_wait)
            wait(NULL);
        }
      }

      // Saving the command in history
      strcpy(last_command, command);
      if (save_c)
        saveCommand(command);
      history = 1;
    }

    // Resetting file descriptors
    dup2(saved_out, 1);
    dup2(saved_in, 0);
  }

  return 0;
}

