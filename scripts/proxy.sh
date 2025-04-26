#!/usr/bin/env bash

start_reverse_proxy_server() {

    # noop if nginx is running
    process_running "$REVERSE_PROXY_PROCESS_TAG"
    if [[ "$RUNNING" == "$TRUE" ]]; then
        log "The reverse proxy server is already running."
        return 0
    fi

    local nginx_template_path
    local nginx_conf_path
    nginx_template_path="$PROJECT_DIR"/nginx.conf.template
    nginx_conf_path="$PROJECT_DIR"/nginx.conf
    if [[ ! -f "$nginx_template_path" ]]; then
        fail "Could not find the Nginx config template at $nginx_template_path."
        exit 1
    fi

    # shellcheck disable=SC2016
    envsubst '${PROJECT_DIR} ${REVERSE_PROXY_PROCESS_TAG} ${REVERSE_PROXY_PORT} ${SERVER_PORT} ${UI_PORT}' < "$nginx_template_path" > "$nginx_conf_path"
    if ! nginx -t -c "$nginx_conf_path"; then
        fail "Nginx config test failed."
        return 1
    fi

    local start_command
    start_command="nginx -c $PROJECT_DIR/nginx.conf"

    # if successful, print messages
    if start_process "$REVERSE_PROXY_PROCESS_TAG" "$start_command"; then
        log "Started the reverse proxy server."
        log "See $LOG_PATH for reverse proxy server logs."
        return 0
    else
        fail "Something went wrong when starting the reverse proxy server."
        return 1
    fi
}


stop_reverse_proxy_server() {
    # noop if the server is running
    process_running "$REVERSE_PROXY_PROCESS_TAG"
    log "ARE WE RUNNING: $RUNNING"
    if [[ "$RUNNING" == "$FALSE" ]]; then
        log "The reverse proxy server was not running."
        return 0
    fi

    # kill the server
    if stop_process "$REVERSE_PROXY_PROCESS_TAG"; then
        log "The reverse proxy server was shut down."
        return 0
    else
        warn "Could not shut down the reverse proxy server. Perform the shut down manually."
        return 1
    fi
}