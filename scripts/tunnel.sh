#!/usr/bin/env bash


start_cloudflared() {

    # noop if the server is running
    process_running "$CLOUDFLARED_PROCESS_TAG"
    if [[ "$RUNNING" == "$TRUE" ]]; then
        log "Cloudflared tunnel is already running."
        return 0
    fi

    # get paths to config and tunnel credentials
    local config_template_path
    local config_path
    local tunnel_credentials_path

    config_path="$PROJECT_DIR"/cloudflared/config.yml
    config_template_path="$PROJECT_DIR"/cloudflared/config.yml.template
    if [[ ! -f "$config_template_path" ]]; then
        fail "Cloudflared tunnel configuration template file not found at $config_template_path."
        exit 1
    fi

    local json_counts
    json_counts="$(find "$PROJECT_DIR"/cloudflared -maxdepth 1 -type f -name "*.json" | wc -l)"
    if [[ "$json_counts" -ne 1 ]]; then
        fail "There should be exactly one .json file in $PROJECT_DIR/cloudflared to store the tunnel credentials."
        exit 1
    fi
    tunnel_credentials_path="$(find "$PROJECT_DIR"/cloudflared -maxdepth 1 -type f -name "*.json")"

    CLOUDFLARED_TUNNEL_CREDENTIALS_PATH="$tunnel_credentials_path"
    export CLOUDFLARED_TUNNEL_CREDENTIALS_PATH
    CLOUDFLARED_TUNNEL_ID="$(basename "$tunnel_credentials_path" .json)"
    export CLOUDFLARED_TUNNEL_ID
    envsubst < "$config_template_path" > "$PROJECT_DIR"/cloudflared/config.yml

    # generate start command
    local start_command
    start_command="cloudflared tunnel --config $config_path --cred-file $tunnel_credentials_path run $CLOUDFLARED_TUNNEL_ID"

    # if startup is successful, print messages
    if start_process "$CLOUDFLARED_PROCESS_TAG" "$start_command"; then
        log "Starting the Cloudflared tunnel."
        log "See $LOG_PATH for the Cloudflared tunnel logs."
        return 0
    else
        fail "Something went wrong when starting the Cloudflared tunnel."
        exit 1
    fi
}


stop_cloudflared() {
    # noop if not running
    process_running "$CLOUDFLARED_PROCESS_TAG"
    if [[ "$RUNNING" == "$FALSE" ]]; then
        log "The Cloudflared tunnel was not running."
        return 0
    fi

    # kill
    if stop_process "$CLOUDFLARED_PROCESS_TAG"; then
        log "The Cloudflared tunnel is busy shutting down. Check the logs to check if the shutdown is complete."
        return 0
    else
        warn "Could not shut down the Cloudflared tunnel. Perform the shut down manually."
        return 1
    fi
}