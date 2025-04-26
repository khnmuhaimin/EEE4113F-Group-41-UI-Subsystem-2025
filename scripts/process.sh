#!/usr/bin/env bash

get_log_path() {
    local process_tag="$1"
    LOG_PATH="$PROJECT_DIR/logs/$process_tag.log"
}

# Description:
#   This function is used to start a new process in the background. It uses `nohup` to ensure the process continues running after the script ends, and the output is redirected to a log file. The function captures the process ID (PID) of the started process and stores it in a specified directory for later use (e.g., stopping the process).
# 
# Arguments:
#   - $1 (process_tag) : A unique identifier for the process (e.g., "server", "database").
#   - $2 (command)     : The command to be executed to start the process. This should be a full command string, e.g., "gunicorn server.server:server --bind 0.0.0.0:$PORT".
#
# Global Variables Set:
#   - PID_DIR           : The path to the file where the process's PID will be stored. Set to "$PROJECT_DIR/pids/$process_tag.pid".
#   - LOG_PATH           : The path to the log file where the process's output will be redirected. Set to "$PROJECT_DIR/logs/$process_tag.log".
#
# Return Values:
#   - 0 (Success): The process was started successfully, and the PID was stored.
#   - Non-zero (Failure): If the process fails to start, this function will exit silently.
#     Note: Since `start_process` doesn’t explicitly handle errors or return any failure codes, this assumes successful execution unless other issues occur.
start_process() {
    local process_tag="$1"
    local command="$2"

    # global variables
    PID=
    LOG_PATH="$PROJECT_DIR/logs/$process_tag.log"
    PID_DIR="$PROJECT_DIR/pids/$process_tag.pid"

    nohup bash -c "$command" &> "$LOG_PATH" &  # run in a new shell
    PID=$!
    if [[ "$command" != *nginx* ]]; then
        # the command used to start nginx is actually the command to
        # start the LAUNCHER for nginx. If we store nginx's pid using
        # the line below, we'll be storing the pid of the laucnher.
        # Instead, in the nginx.conf.template (and nginx.conf), there
        # is a line to tell nginx to log its pid to REVERSE_PROXY.pid

        echo "$PID" > "$PID_DIR"  # store the PID
    fi
    
    return 0
}


# Description:
#   This function is used to stop a running process identified by a unique name. 
#   It reads the process's PID from a file stored in the project's `pids` 
#   directory and attempts to terminate the process using the `kill` command. 
#   If the process is successfully terminated, the corresponding PID file is removed.
#
# Arguments:
#   - $1 (process_name): A unique identifier for the process (e.g., "server", "database").
#                        This is used to locate the PID file at 
#                        `$PROJECT_DIR/pids/$process_name.pid`.
#
# Global Variables Used:
#   - PROJECT_DIR: The base directory used to locate the `pids` folder.
#
# Return Values:
#   - 0 (Success): The process was successfully terminated and the PID file was deleted.
#   - 1 (Failure): The PID file does not exist, the PID could not be read, or the process
#                 could not be terminated.
stop_process() {
    local process_tag="$1"
    local pid_file="$PROJECT_DIR/pids/$process_tag.pid"

    # Check if the PID file exists
    if [[ -f "$pid_file" ]]; then
        local pid
        pid=$(cat "$pid_file")

        # Try to kill the process
        if kill "$pid"; then
            rm "$pid_file"  || exit 1
            return 0
        else
            return 1
        fi
    else
        return 1
    fi
}


# Description:
# This function checks if a process, identified by a given name, is currently 
# running based on its stored PID. The function reads the PID from a file, 
# attempts to check if the process is running using the `ps` command, and sets 
# the `RUNNING` variable to indicate whether the process is running or not.
#
# Arguments:
# - process_name (string): The name of the process for which to check the 
#   running status. This is used to locate the corresponding PID file 
#   (`$PROJECT_DIR/pids/$process_name.pid`).
#
# Global Variables Set:
# - RUNNING: A global variable that will be set to `$TRUE` if the process is 
#   running, and `$FALSE` if the process is not running or the PID file does 
#   not exist.
#
# Return Values:
# - Always returns `0` (success), but updates the global `RUNNING` variable 
#   based on whether the process is running or not.
#   - If the process is running, `RUNNING` is set to `$TRUE`.
#   - If the process is not running, `RUNNING` is set to `$FALSE`.
process_running() {
    local process_name="$1"
    local pid_dir
    local pid

    # global variables
    RUNNING=
    
    pid_dir="$PROJECT_DIR/pids/$process_name.pid"
    if [[ -f "$pid_dir" ]]; then
        pid="$(cat "$pid_dir")"
        
        if ps -p "$pid" > /dev/null; then
            RUNNING="$TRUE"
        else
            RUNNING="$FALSE"
        fi
    else
        # shellcheck disable=SC2034
        RUNNING="$FALSE"

    fi
    return 0
}