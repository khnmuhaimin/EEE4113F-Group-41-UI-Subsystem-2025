from dotenv import load_dotenv
load_dotenv()  # load env vars before running the app
from flask_cors import CORS
import os
import sys

from flask import Flask

from database.database import DatabaseEngineProvider
from routes.weighing_nodes import weighing_node_blueprint
from routes.admin import admin_blueprint

DatabaseEngineProvider.load_default_database()

server = Flask(__name__)
CORS(server, origins="http://localhost:5173")

# register blueprints here
server.register_blueprint(weighing_node_blueprint, url_prefix="/weighing-nodes")
server.register_blueprint(admin_blueprint, url_prefix="/admins")

    
@server.route('/')
def index():
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
