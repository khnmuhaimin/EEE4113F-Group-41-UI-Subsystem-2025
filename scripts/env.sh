#!/usr/bin/env bash

# This function loads and exports environment variables from a specified file.
#
# Usage:
#   load_env_file <env_file>
load_env_file() {
    local env_file="$1"
    if [[ -f "$env_file" ]]; then
        log "Loading environment variables from $env_file"
        set -o allexport
        # shellcheck disable=SC1090
        source "$env_file"
        set +o allexport
    else
        fail "Environment file '$env_file' not found."
    fi
}


# This function loads and exports environment-specific variables 
# based on the value of the environment parameter.
# Must be either is `DEVELOPMENT` or `DEMO`.
#
# Usage:
#   load_environment_specific_file <env>
load_environment_specific_file() {
    local env="$1"
    local env_file
    case "$env" in
        DEVELOPMENT)
            env_file="$PROJECT_DIR/.env.development"
            ;;
        DEMO)
            env_file="$PROJECT_DIR/.env.demo"
            ;;
        *)
            fail "ENVIRONMENT must be set to either DEVELOPMENT or DEMO."
            ;;
    esac
    load_env_file "$env_file"
}