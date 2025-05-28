import os
from flask_cors import CORS
from flask import Flask

from websockets.notifications_manager import NotificationsManager
from config.config import Config
from database.database import DatabaseEngineProvider, DefaultDataProvider
from routes.weighing_nodes import weighing_node_blueprint
from routes.admin import admin_blueprint
from routes.dashboard import dashboard_blueprint
from routes.weight_readings import weight_readings_blueprint
from log.log import logger


NotificationsManager.push_notification("The server is starting...")


logger.info(f"The server is running from dir {os.getcwd()}")
logger.info(f"The server is running in the {Config.ENVIRONMENT} environment.")

DatabaseEngineProvider.load_default_database()
DefaultDataProvider.load_default_admin(DatabaseEngineProvider.get_database_engine())
DefaultDataProvider.load_default_nodes(DatabaseEngineProvider.get_database_engine())
DefaultDataProvider.load_default_weight_readings(DatabaseEngineProvider.get_database_engine())
# DefaultDataProvider.export_weighing_nodes_to_csv(DatabaseEngineProvider.get_database_engine())
# DefaultDataProvider.export_weight_readings_to_csv(DatabaseEngineProvider.get_database_engine())

server = Flask(__name__)
CORS(server, supports_credentials=True, origins=Config.BASE_URL)

# register blueprints here
server.register_blueprint(weighing_node_blueprint, url_prefix="/api/weighing-nodes")
server.register_blueprint(admin_blueprint, url_prefix="/api/admins")
server.register_blueprint(dashboard_blueprint, url_prefix="/api/dashboard")
server.register_blueprint(weight_readings_blueprint, url_prefix="/api/weight-readings")


for rule in server.url_map.iter_rules():
    logger.debug(f"Endpoint registered: {rule.endpoint}: {rule}")

    
@server.route("/api")
def index():
    NotificationsManager.push_notification("Someone got sent \"Hello World\"")
    return "Hello, World!"