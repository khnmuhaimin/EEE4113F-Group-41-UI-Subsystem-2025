#!/usr/bin/env bash

set -e  # Exit on error

function loadColors() {
    BLACK='\033[30m'
    RED='\033[31m'
    GREEN='\033[32m'
    YELLOW='\033[33m'
    BLUE='\033[34m'
    MAGENTA='\033[35m'
    CYAN='\033[36m'
    WHITE='\033[37m'
    BRIGHT_BLACK='\033[90m'
    BRIGHT_RED='\033[91m'
    BRIGHT_GREEN='\033[92m'
    BRIGHT_YELLOW='\033[93m'
    BRIGHT_BLUE='\033[94m'
    BRIGHT_MAGENTA='\033[95m'
    BRIGHT_CYAN='\033[96m'
    BRIGHT_WHITE='\033[97m'
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