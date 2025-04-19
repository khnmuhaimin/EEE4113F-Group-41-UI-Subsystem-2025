from flask_cors import CORS
from flask import Flask

from config.config import Config, Environment
from database.database import DatabaseEngineProvider
from routes.weighing_nodes import weighing_node_blueprint
from routes.admin import admin_blueprint

Config.useConfig(Environment.DEVELOPMENT)
DatabaseEngineProvider.load_default_database()

server = Flask(__name__)
CORS(server, origins="http://localhost:5173")

# register blueprints here
server.register_blueprint(weighing_node_blueprint, url_prefix="/weighing-nodes")
server.register_blueprint(admin_blueprint, url_prefix="/admins")

    
@server.route('/')
def index():
    return "Hello, World!"