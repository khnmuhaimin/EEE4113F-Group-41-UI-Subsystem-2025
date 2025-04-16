from dotenv import load_dotenv
load_dotenv()  # load env vars before running the app
import os
import sys

from flask import Flask

from log.log import logger
from database import database  # import database to create the tables
from routes.weighing_nodes import weighing_node_blueprint
from routes.admin import admin_blueprint


server = Flask(__name__)
server.register_blueprint(weighing_node_blueprint)
server.register_blueprint(admin_blueprint)

    
@server.route("/")
def hello_world():
    return "Hello, World!"



if __name__ == "__main__":

    try:
        port = os.environ["PORT"]
        port = int(port)
    except KeyError:
        print("Error: Port was not specified.")
        sys.exit(1)
    except ValueError:
        print(f"Error: Port must be an integer and not \"{port}\".")
        sys.exit(1)


    try:
        server.run(port=port)
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"Error: Port {port} is already in use.")
        else:
            print(f"Error: {str(e)}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid port number {port}. Port must be an integer between 0 and 65535.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: You do not have permission to use port {port}. Try using a port above 1024.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)
