#!/usr/bin/env bash


help_message="This .sh file contains some helpful scripts.
Run ./scripts {option}
Available options are: start-server, stop-server, start-tunnel, stop-tunnel, tunnel_password."

if [[ $# -eq 0 ]]; then
    echo "$help_message"
fi

if [[ ! -f .env ]]; then
    cp env-template .env
    echo 'No .env file found. A .env template is being generated.'
    echo 'Complete it and try again.'
    exit 0
fi

source .env

case $1 in
    start-server)
        if [[ ! -d '.venv' ]]; then
            python3 -m venv .venv
        fi
        source .venv/bin/activate
        pip install -r requirements.txt -qq
        gunicorn_count=$(ps aux | grep 'gunicorn server:server' | grep -v grep | wc -l)
        if [[ $gunicorn_count -ne 0 ]]; then
            echo 'The server is already running.'
        else
            gunicorn server:server --bind 0.0.0.0:$PORT > server-logs.txt 2>&1 &
            echo 'The server is running in the background.'
            echo 'See server logs at server-logs.txt.'
        fi
        ;;
    stop-server)
        pkill -15 -f 'gunicorn server:server'
        if [[ $? == 0 ]]; then
            echo 'The server was shut down.'
        else
            echo 'The server was not running to begin with.'
        fi
        ;;
    start-tunnel)
        lt_counts=$(ps aux | grep 'npm exec lt' | grep -v grep | wc -l)
        if [[ $lt_counts -ne 0 ]]; then
            echo 'LocalTunnel is already running.'
            echo 'See localtunnel-logs.txt for logs.'
        else
            npm install --silent
            if [[ $SERVER_MODE == 'TEST' ]]; then
                npx lt --port $PORT --subdomain $DOMAIN --https > localtunnel-logs.txt 2>&1 &
                echo "Requests to $DOMAIN.loca.lt are being redirected to the port $PORT."
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