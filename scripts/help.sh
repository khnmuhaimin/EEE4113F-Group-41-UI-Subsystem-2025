#!/usr/bin/env bash

# This function prints a help message to the terminal that provides information
# about the available options in the script.
# It lists the available commands/options and guides the user on how to use them.
#
# Usage:
#   print_help_message
print_help_message() {
    local options="help, start-server, stop-server, start-tunnel, stop-tunnel, get-tunnel-password, get-domain, start-proxy, stop-proxy"
    
    local help_message="This .sh file contains some helpful scripts.
    
Run './scripts {option}' to execute a command.
Available options are:
$options"

    echo "$help_message"
}