#!/usr/bin/env bash

help_message="This .sh file contains some helpful scripts.
Run ./scripts {option}
Available options are: start-server, stop-server, restart-server, start-tunnel, stop-tunnel, tunnel_password."

if [[ $# -eq 0 ]]; then
    echo "$help_message"
    exit 0
fi

source .env

setup_backend_venv() {
    if [ ! -d "/backend/.venv/" ]; then
        python3 -m venv /backend/.venv/
    fi
    source .venv/bin/activate
    pip install -r requirements.txt -qq
}


load_env() {
    print_env_variables_output="$(python3 backend/config/print_env_variables.py)"
    if [[ $? == 0 ]]; then
        eval "$print_env_variables_output"
    else
        echo "$print_env_variables_output"
        exit 1
    fi
}




case $1 in
    start-server)
        setup_backend_venv
        load_env
        cd backend
        gunicorn_count=$(ps aux | grep 'gunicorn server.server:server' | grep -v grep | wc -l)
        if [[ $gunicorn_count -ne 0 ]]; then
            echo 'The server is already running.'
        else
            if [[ $ENVIRONMENT == 'DEVELOPMENT' ]]; then
                log_level="DEBUG"
            else
                log_level="INFO"
            fi
            gunicorn server.server:server --bind 0.0.0.0:$PORT --access-logfile - --log-level $log_level > server-logs.txt 2>&1 &
            echo 'The server is running in the background.'
            echo 'See server logs at server-logs.txt.'
        fi
        cd ..
        ;;
    stop-server)
        pkill -15 -f 'gunicorn server.server:server'
        if [[ $? == 0 ]]; then
            echo 'The server was shut down.'
        else
            echo 'The server was not running to begin with.'
        fi
        ;;
    restart-server)
        ./scripts.sh stop-server
        sleep 1
        ./scripts.sh start-server
        ;;
    start-tunnel)
        setup_backend_venv
        load_env
        lt_counts=$(ps aux | grep 'npm exec lt' | grep -v grep | wc -l)
        if [[ $lt_counts -ne 0 ]]; then
            echo 'LocalTunnel is already running.'
            echo 'See localtunnel-logs.txt for logs.'
        else
            npm install --silent
            if [[ $ENVIRONMENT == 'DEMO' ]]; then
                npx lt --port $PORT --subdomain $SUBDOMAIN --https > localtunnel-logs.txt 2>&1 &
                echo "Requests to $SUBDOMAIN.loca.lt are being redirected to the port $PORT."
                echo 'See localtunnel-logs.txt for logs.'
            else
                npx lt --port $PORT --https > localtunnel-logs.txt 2>&1 &
                echo "Requests to a random domain are being redirected to the port $PORT."
                echo 'See localtunnel-logs.txt for logs.'
            fi
        fi
        ;;
    stop-tunnel)
        pkill -15 -f 'npm exec lt'
        if [[ $? == 0 ]]; then
            echo 'LocalTunnel was shut down.'
        else
            echo 'LocalTunnel was not running to begin with.'
        fi
        ;;
    tunnel-password)
        tunnel_password=$(curl -s https://loca.lt/mytunnelpassword)
        echo "The tunnel password is $tunnel_password."
        ;;
    *)
        echo "$help_message"
        ;;
esac