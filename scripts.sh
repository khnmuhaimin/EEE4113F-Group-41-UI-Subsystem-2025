#!/usr/bin/env bash

# ---- Useful constants ----
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PROJECT_DIR

# shellcheck disable=SC2034
TRUE=TRUE
# shellcheck disable=SC2034
FALSE=FALSE
# shellcheck disable=SC2034
SERVER_PROCESS_TAG=SERVER
# shellcheck disable=SC2034
UI_PROCESS_TAG=UI
# shellcheck disable=SC2034
CLOUDFLARED_PROCESS_TAG=CLOUDFLARED

# ---- Importing all scripts
for script in "$PROJECT_DIR"/scripts/*.sh; do
  if [ -f "$script" ]; then
    # shellcheck disable=SC1090
    source "$script"
  fi
done

# load all color codes
loadColors


main() {

    # print help message if exactly zero or more than 1 arguments were given
    if [[ $# -ne 1 ]]; then
        print_help_message
        exit 0
    fi

    # Setting up environment variables
    log "Exporting base environment variables..."
    load_env_file "${PROJECT_DIR}"/.env
    load_environment_specific_file "$ENVIRONMENT"
    log "Environment setup complete."

    case $1 in
        start)
            "$PROJECT_DIR"/scripts.sh start-server
            "$PROJECT_DIR"/scripts.sh start-ui
            "$PROJECT_DIR"/scripts.sh start-tunnel
        ;;
        stop)
            "$PROJECT_DIR"/scripts.sh stop-server
            "$PROJECT_DIR"/scripts.sh stop-ui
            "$PROJECT_DIR"/scripts.sh stop-tunnel
        ;;
        start-server)
            setup_backend_venv
            start_server
        ;;
        stop-server)
            stop_server
        ;;
        start-ui)
            setup_ui_server
            start_ui_server
        ;;
        stop-ui)
            stop_ui_server
        ;;
        start-tunnel)
            start_cloudflared
        ;;
        stop-tunnel)
            stop_cloudflared
        ;;
        *)
            print_help_message  
        ;;
    esac   
}

# ---- Entry Point ----
main "$@"