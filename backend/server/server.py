from flask_cors import CORS
from flask import Flask

from config.config import Config
from database.database import DatabaseEngineProvider, DefaultDataProvider
from routes.weighing_nodes import weighing_node_blueprint
from routes.admin import admin_blueprint
from log.log import logger


logger.info(f"The server is running in the {Config.ENVIRONMENT} environment.")

DatabaseEngineProvider.load_default_database()
DefaultDataProvider.load_default_admin(DatabaseEngineProvider.get_database_engine())

server = Flask(__name__)
CORS(server, supports_credentials=True, origins=Config.BASE_URL)

# register blueprints here
server.register_blueprint(weighing_node_blueprint, url_prefix="/weighing-nodes")
server.register_blueprint(admin_blueprint, url_prefix="/admins")

    
@server.route('/')
def index():
    return "Hello, World!"