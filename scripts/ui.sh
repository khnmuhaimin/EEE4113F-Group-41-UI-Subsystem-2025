#!/usr/bin/env bash

setup_ui_server() {

    local frontend_dir
    frontend_dir="$PROJECT_DIR"/frontend
    local package_file_path
    package_file_path="$frontend_dir"/package.json

    local current_dir
    current_dir="$(pwd)"  # jump back at the end of the function
    trap 'cd "$current_dir" || exit 1' EXIT

    cd "$frontend_dir" || exit 1

    if [[ -f "$package_file_path" ]]; then
        log "Installing frontend dependencies..."
        npm install --silent
        return 0
    else
        fail "Package file file not found at $package_file_path."
        cd "$current_dir" || exit 1
        exit 1
    fi
}


start_ui_server() {

    # noop if the server is running
    process_running "$UI_PROCESS_TAG"
    if [[ "$RUNNING" == "$TRUE" ]]; then
        log "The UI server is already running."
        return 0
    fi

    local current_dir
    current_dir="$(pwd)"  # jump back at the end of the function
    trap 'cd "$current_dir" || exit 1' EXIT

    cd "$PROJECT_DIR/frontend" || exit

    local start_command
    if [[ "$ENVIRONMENT" == "DEVELOPMENT" ]]; then
        start_command="$PROJECT_DIR/frontend/node_modules/.bin/vite serve $PROJECT_DIR/frontend --port $UI_PORT"
    else
        debug "Building frontend files."
        cd "$PROJECT_DIR"/frontend || exit 1
        npm run build > "$PROJECT_DIR"/logs/UI-BUILD.log 2>&1
        start_command="$PROJECT_DIR/frontend/node_modules/.bin/vite preview $PROJECT_DIR/frontend --port $UI_PORT"
    fi
    # if startup is successful, print messages
    if start_process "$UI_PROCESS_TAG" "$start_command"; then
        log "Starting the UI server."
        log "See $LOG_PATH for server logs."
        return 0
    else
        fail "Something went wrong when starting the UI server."
        return 1
    fi
}


stop_ui_server() {
    # noop if the server is running
    process_running "$UI_PROCESS_TAG"
    if [[ "$RUNNING" == "$FALSE" ]]; then
        log "The UI server was not running."
        return 0
    fi

    # kill the server
    if stop_process "$UI_PROCESS_TAG"; then
        log "The UI server was shut down."
        return 0
    else
        warn "Could not shut down the UI server. Perform the shut down manually."
        return 1
    fi
}