#!/usr/bin/env bash

setup_localtunnel() {

    local package_file="${PROJECT_DIR}"/package.json

    local current_dir
    current_dir="$(pwd)"  # jump back at the end of the function
    trap 'cd "$current_dir" || exit 1' EXIT

    if [[ -f "$package_file" ]]; then
        log "Installing localtunnel..."
        npm install --silent
        cd "$current_dir" || exit 1
        return 0
    else
        fail "Package file not found at $package_file"
        cd "$current_dir" || exit 1
        exit 1
    fi

}


start_localtunnel() {

    # noop if the server is running
    process_running "$LOCALTUNNEL_PROCESS_TAG"
    if [[ "$RUNNING" == "$TRUE" ]]; then
        log "Localtunnel is already running."
        return 0
    fi

    local current_dir
    current_dir="$(pwd)"  # jump back at the end of the function
    trap 'cd "$current_dir" || exit 1' EXIT

    # setup the localtunnel
    setup_localtunnel || exit 1

    # get command
    if [[ "$ENVIRONMENT" == DEMO ]]; then
        local start_command="npx lt --port $REVERSE_PROXY_PORT --subdomain $SUBDOMAIN --https"
    else
        local start_command="npx lt --port $REVERSE_PROXY_PORT --https"
    fi

    # if startup is successful, print messages
    if start_process "$LOCALTUNNEL_PROCESS_TAG" "$start_command"; then
        log "Started localtunnel."
        log "See $LOG_PATH for server logs."
        return 0
    else
        fail "Something went wrong when starting localtunnel."
        return 1
    fi
}


stop_localtunnel() {
    # noop if the server is running
    process_running "$LOCALTUNNEL_PROCESS_TAG"
    if [[ "$RUNNING" == "$FALSE" ]]; then
        log "Localtunnel was not running."
        return 0
    fi

    # kill the server
    if stop_process "$LOCALTUNNEL_PROCESS_TAG"; then
        log "Localtunnel was shut down."
        return 0
    else
        warn "Could not shut down localtunnel. Perform the shut down manually."
        return 1
    fi
}


get_tunnel_password() {
    local tunnel_password
    tunnel_password="$(curl -s https://loca.lt/mytunnelpassword)"
    log "The tunnel password is $tunnel_password."
}


get_domain() {

    process_running "$LOCALTUNNEL_PROCESS_TAG"
    if [[ "$RUNNING" == "$FALSE" ]]; then
        log "Localtunnel is not running."
        return 0
    fi

    get_log_path "$LOCALTUNNEL_PROCESS_TAG"
    local log_path
    log_path="$LOG_PATH"

    if [[ ! -f "$log_path" ]]; then
        fail "The localtunnel logs was not found at $log_path. Cannot get the domain."
        exit 1
    fi

    local url_counts
    url_counts="$(grep -c http "$log_path")"
    if [[ "$url_counts" -ne 1 ]]; then
        fail "Unable to parse the localtunnel logs."
        exit 1
    fi
    
    local line_with_url
    line_with_url="$(grep -m 1 http "$log_path")"
    for word in $line_with_url; do
        if [[ "$word" == http* ]]; then
            log "$word"
            return 0
        fi
    done
    fail "Something went wrong while reading the domain."
    exit 1
}