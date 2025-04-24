#!/usr/bin/env bash

set -e  # Exit on error

# This function logs an informational message to the console with an [INFO] tag.
#
# Usage:
#   log <message>
log() {
    echo "[INFO] $*"
}

# This function logs an warning message to the console with an [WARN] tag.
#
# Usage:
#   log <message>
warn() {
    echo "[WARN] $*"
}


# This function logs an error message to the console with an [ERROR] tag and exits the script 
# with a non-zero status, indicating failure.
#
# Usage:
#   fail <error_message>
fail() {
    echo "[ERROR] $*" >&2
    exit 1
}