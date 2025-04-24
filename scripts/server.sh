#!/usr/bin/env bash

setup_backend_venv() {
    local venv_dir="${PROJECT_DIR}"/backend/.venv
    local requirements_file="${PROJECT_DIR}"/backend/requirements.txt

    if [[ ! -d "$venv_dir" ]]; then
        if python3 -m venv "$venv_dir"; then
            log "Created a python virtual environment for the backend."
        else
            fail "Couldn't create a python virtual environment for the backend."
            exit 1
        fi
    fi

    # Activate virtual environment
    # shellcheck source=/dev/null
    if ! source "$venv_dir"/bin/activate; then
        fail "Couldn't activate the python virtual environment for the backend."
        exit 1
    fi
    # Install dependencies quietly
    if [[ -f "$requirements_file" ]]; then
        log "Installing Python dependencies from $requirements_file..."
        pip install -r "$requirements_file" -qq
    else
        fail "Requirements file not found: $requirements_file"
        exit 1
    fi
    return 0
}


# Description:
#   Starts the server process by setting up the Python virtual environment,
#   navigating to the backend directory, and running the `gunicorn` server.
#   If the server is already running, it skips the operation. The function
#   handles logging and returns an appropriate status code based on success or failure.
#
# Arguments:
#   None
#
# Global Variables:
#   SERVER_PROCESS_TAG - Tag used to identify the server process.
#   RUNNING - Global variable set by `check_process` to indicate if the process is running.
#   TRUE - Constant representing "true" used for process check comparison.
#   ENVIRONMENT - Environment variable that determines the environment (e.g., DEVELOPMENT).
#   LOG_PATH - Path to the log file for the server.
#   PROJECT_DIR - The root project directory.
#   SERVER_PORT - The port number to bind the server to.
#
# Return Values:
#   0 - If the server was started successfully.
#   1 - If there was an issue starting the server.
start_server() {

    # noop if the server is running
    process_running "$SERVER_PROCESS_TAG"
    if [[ "$RUNNING" == "$TRUE" ]]; then
        log "The server is already running."
        return 0
    fi

    local current_dir
    current_dir="$(pwd)"  # jump back at the end of the function

    # start the server
    setup_backend_venv || exit 1
    cd "${PROJECT_DIR}/backend" || exit 1
    if [[ "$ENVIRONMENT" == DEVELOPMENT ]]; then
        local log_level=DEBUG
    else
        local log_level=INFO
    fi

    # if successful, print messages
    local start_command="gunicorn server.server:server --bind 0.0.0.0:$SERVER_PORT --access-logfile - --log-level $log_level"
    if start_process "$SERVER_PROCESS_TAG" "$start_command"; then
        log "Started the server."
        log "See $LOG_PATH for server logs."
        cd "$current_dir" || exit 1
        return 0
    else
        fail "Something went wrong when starting the server."
        cd "$current_dir" || exit 1
        return 1
    fi
}


stop_server() {
    # noop if the server is running
    process_running "$SERVER_PROCESS_TAG"
    if [[ "$RUNNING" == "$FALSE" ]]; then
        log "The server was not running."
        return 0
    fi

    # kill the server
    if stop_process "$SERVER_PROCESS_TAG"; then
        log "The server was shut down."
    else
        warn "Could not shut down the server. Perform the shut down manually."
    fi
}