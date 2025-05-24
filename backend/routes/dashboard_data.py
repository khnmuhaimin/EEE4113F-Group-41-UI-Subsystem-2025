from flask import Blueprint


admin_blueprint = Blueprint("admin", __name__)


@admin_blueprint.route("/dashboard-data", methods=["GET"], endpoint="get_dashboard_data")
def get_dashboard_data():
    response_body = {
        
    }