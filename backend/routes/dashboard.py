from http import HTTPStatus
from flask import Blueprint, jsonify, make_response, send_file
from sqlalchemy.orm import Session
from sqlalchemy import select

from database.database import DefaultDataProvider, DatabaseEngineProvider
from routes.auth import authenticate_with_session_id
from database.models.weight_reading import WeightReading
from database.database import DatabaseEngineProvider
from log.log import logger


dashboard_blueprint = Blueprint("dashboard_blueprint", __name__)


@dashboard_blueprint.route('weight-readings/csv', methods=["GET"], endpoint="download_csv_data")
@authenticate_with_session_id
def download_csv_data():
    file_path = '/home/khnmuhaimin/EEE4113F/EEE4113F-Group-41-UI-Subsystem-2025/weight-readings.csv'  # replace with your actual file path
    DefaultDataProvider.export_weight_readings_to_csv(DatabaseEngineProvider.get_database_engine(), file_path)
    response = make_response(send_file
        (
            file_path,
            mimetype='text/csv',
            as_attachment=True,
            download_name='weight-readings.csv'  # filename for the download prompt
        )
    )
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


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
    

