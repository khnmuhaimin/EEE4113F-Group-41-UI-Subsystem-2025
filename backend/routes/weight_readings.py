
from http import HTTPStatus
from uuid import UUID
from flask import Blueprint, request
from flask import Blueprint
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.utils.utils import utc_timestamp
from database.models.weighing_node import WeighingNode
from database.models.weight_reading import WeightReading
from database.database import DatabaseEngineProvider
from routes.auth import authenticate_weighing_node, enforce_registration_complete
from log.log import logger


weight_readings_blueprint = Blueprint("weight_readings_blueprint", __name__)


def validate_raw_weight_reading(line: str):
    logger.debug(line)
    try:
        first_comma = line.find(',')
        last_comma = line.rfind(',')

        first = line[:first_comma]
        middle = line[first_comma+1:last_comma]
        last = line[last_comma+1:]
        parts = [first, middle, last]
        if len(parts) != 3:
            logger.warning("Incorrect number of parts")
            return False

        rfid = parts[0].strip()
        if len(rfid) < 1:
            logger.warning("No RFID")
            return False

        weight_part = parts[1].strip()
        if not (weight_part.startswith('[') and weight_part.endswith(']')):
            logger.warning("No brackets")
            return False
        weight_strs = weight_part[1:-1].split(',')
        weights = [float(w.strip()) for w in weight_strs]
        if len(weights) == 0:
            logger.warning("No weights")
            return False

        age = int(parts[2].strip())

        return True
    except Exception as e:
        logger.error(e)
        return False
    

def parse_raw_weight_reading(line: str):
    first_comma = line.find(',')
    last_comma = line.rfind(',')

    first = line[:first_comma]
    middle = line[first_comma+1:last_comma]
    last = line[last_comma+1:]
    parts = [first, middle, last]
    rfid = parts[0]
    weight_part = parts[1].strip()
    weight_strs = weight_part[1:-1].split(',')
    weights = [float(w.strip()) for w in weight_strs]
    age = int(parts[2].strip())
    return (rfid, weights, age)


@weight_readings_blueprint.route("", methods=["POST"], endpoint="create_weight_reading")
def create_weight_reading():
    # get plain text body
    content = request.get_data(as_text=True)
    lines = content.strip().split('\n')
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line != ""]
    if len(lines) == 0:
        return "", HTTPStatus.NO_CONTENT
    
    for line in lines:
        if not validate_raw_weight_reading(line):
            return "Invalid request body.", HTTPStatus.BAD_REQUEST
        
    new_readings = [parse_raw_weight_reading(line) for line in lines]

    with Session(DatabaseEngineProvider.get_database_engine()) as session:
        node_id = request.headers.get("Node-ID")
        node = session.scalars(select(WeighingNode).where(WeighingNode.uuid == UUID(node_id))).one()
        for rfid, weights, age in new_readings:
            session.add(
                WeightReading(
                    node_id=node.id,
                    penguin_rfid=rfid,
                    weight=sum(weights)/len(weights),
                    created_at=utc_timestamp(-age)
                )
            )
        session.commit()
    return HTTPStatus.NO_CONTENT