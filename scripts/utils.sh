#!/usr/bin/env bash

set -e  # Exit on error

function loadColors() {
    # shellcheck disable=SC2034
    BLACK='\033[30m'
    # shellcheck disable=SC2034
    RED='\033[31m'
    # shellcheck disable=SC2034
    GREEN='\033[32m'
    # shellcheck disable=SC2034
    YELLOW='\033[33m'
    # shellcheck disable=SC2034
    BLUE='\033[34m'
    # shellcheck disable=SC2034
    MAGENTA='\033[35m'
    # shellcheck disable=SC2034
    CYAN='\033[36m'
    # shellcheck disable=SC2034
    WHITE='\033[37m'
    # shellcheck disable=SC2034
    BRIGHT_BLACK='\033[90m'
    # shellcheck disable=SC2034
    BRIGHT_RED='\033[91m'
    # shellcheck disable=SC2034
    BRIGHT_GREEN='\033[92m'
    # shellcheck disable=SC2034
    BRIGHT_YELLOW='\033[93m'
    # shellcheck disable=SC2034
    BRIGHT_BLUE='\033[94m'
    # shellcheck disable=SC2034
    BRIGHT_MAGENTA='\033[95m'
    # shellcheck disable=SC2034
    BRIGHT_CYAN='\033[96m'
    # shellcheck disable=SC2034
    BRIGHT_WHITE='\033[97m'
    # shellcheck disable=SC2034
    RESET='\033[0m'
}

# This function logs an informational message to the console with an [INFO] tag.
#
# Usage:
#   log <message>
log() {
    echo -e "${GREEN}[INFO]$RESET $*"
}

# This function logs an warning message to the console with an [WARN] tag.
#
# Usage:
#   log <message>
warn() {
    echo "${YELLOW}[WARN]$RESET $*"
}


# This function logs an error message to the console with an [ERROR] tag and exits the script 
# with a non-zero status, indicating failure.
#
# Usage:
#   fail <error_message>
fail() {
    echo "${RED}[ERROR] $*" >&2
    exit 1
}