#!/usr/bin/env bash

setup_backend_venv() {
    local venv_dir="$PROJECT_DIR"/backend/.venv
    local requirements_file="$PROJECT_DIR"/backend/requirements.txt

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

    if [[ ! -f "$PROJECT_DIR"/requirements.txt ]]; then
        fail "Couldn't find the dependency list at $PROJECT_DIR/requirements.txt."
        exit 1
    fi
    
    dependencies="$(pip freeze)"
    installed="$(cat "$PROJECT_DIR"/requirements.txt)"
    if [[ "$dependencies" != "$installed" ]]; then
        log "Installing dependencies."
        pip install -r "$requirements_file" -qq
    fi
}


start_server() {

    # noop if the server is running
    process_running "$SERVER_PROCESS_TAG"
    if [[ "$RUNNING" == "$TRUE" ]]; then
        log "The server is already running."
        return 0
    fi

    local original_dir
    original_dir="$(pwd)"  # jump back at the end of the function
    trap 'cd $original_dir' EXIT


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
        return 0
    else
        fail "Something went wrong when starting the server."
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
        log "The server is shutting down. Check the logs to check if the shutdown is complete."
    else
        warn "Could not shut down the server. Perform the shut down manually."
    fi
}