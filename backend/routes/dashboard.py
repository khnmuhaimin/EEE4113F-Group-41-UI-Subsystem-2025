from http import HTTPStatus
from flask import Blueprint, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import select

from database.models.weight_reading import WeightReading
from database.database import DatabaseEngineProvider
from log.log import logger


dashboard_blueprint = Blueprint("dashboard_blueprint", __name__)


@dashboard_blueprint.route("weight-readings", methods=["GET"], endpoint="get_weight_readings")
def get_weight_readings():
    with Session(DatabaseEngineProvider.get_database_engine()) as session:
        readings = session.scalars(select(WeightReading).order_by(WeightReading.created_at)).all()
        result = []
        for r in readings:
            result.append({
                'id': r.id,
                'node_id': r.node_id,
                'penguin_rfid': r.penguin_rfid,
                'weight': r.weight,
                'created_at': r.created_at,
            })
        return jsonify(result), HTTPStatus.OK