
from datetime import datetime, timezone
from http import HTTPStatus
import struct
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
from websockets.notifications_manager import NotificationsManager


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


def parse_payload(data_str: str):
    # First, recover the original bytes from Flask's string conversion
    try:
        # This assumes Flask used UTF-8 to decode the original bytes
        original_bytes = data_str.encode('utf-8')
    except UnicodeError:
        raise ValueError("Invalid UTF-8 data")
    
    if len(original_bytes) < 10:
        raise ValueError("Payload too short (needs at least 10 bytes)")
    
    # Extract first 10 bytes as ASCII
    try:
        prefix = original_bytes[:10].decode('ascii')
    except UnicodeDecodeError:
        raise ValueError("Prefix contains non-ASCII characters")
    
    # Process remaining bytes as big-endian integers (most significant byte first)
    remaining_bytes = original_bytes[10:]
    if len(remaining_bytes) % 4 != 0:
        raise ValueError("Remaining data length must be divisible by 4 for 32-bit integers")
    
    ints = []
    for i in range(0, len(remaining_bytes), 4):
        chunk = remaining_bytes[i:i+4]
        # '>' means big-endian (most significant byte first)
        value = struct.unpack('>i', chunk)[0]
        ints.append(value)
    
    return prefix, ints


def get_rfid(content: str):
    try:
        valid = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
        is_valid = [i in valid for i in content]
        start = 1
        while start < len(is_valid):
            if is_valid[start] and not is_valid[start - 1]:
                break
            start += 1
        rfid = content[start:start+12]
        return rfid
    except Exception as e:
        logger.error(e)


last_rfid = None
time_of_last_rfid = None
@weight_readings_blueprint.route("", methods=["POST"], endpoint="create_weight_reading")
def create_weight_reading():
    global last_rfid
    global time_of_last_rfid
    # get plain text body
    content = request.get_data(as_text=True)
    dot_index = content.rfind(".")
    rfid = get_rfid(content)
    if last_rfid is None:
        last_rfid = rfid
        time_of_last_rfid = datetime.now(tz=timezone.utc).timestamp()
    elif rfid == last_rfid and (datetime.now(tz=timezone.utc).timestamp() - time_of_last_rfid) < 3:
        time_of_last_rfid = datetime.now(tz=timezone.utc).timestamp()
        return "", HTTPStatus.NO_CONTENT

    weights = [float(content[dot_index-1:]) * 1000]

    logger.debug(f"Content: {content}")
    # rfid, weights = parse_payload(content)
    logger.debug(f"RFID: {rfid}")
    logger.debug(f"Weights: {weights}")
    with Session(DatabaseEngineProvider.get_database_engine()) as session:
        node_id = request.headers.get("Node-ID")
        logger.debug(f"Node ID: {node_id}")
        node = session.scalars(select(WeighingNode).where(WeighingNode.uuid == UUID(node_id))).one()
        logger.debug(f"Node ID found: {node.uuid}")
        session.add(
            WeightReading(
                node_id=node.id,
                penguin_rfid=rfid,
                weight=sum(weights)/len(weights)
            )
        )
        session.commit()
    NotificationsManager.push_notification("FETCH_WEIGHT_READINGS")
    return "", HTTPStatus.NO_CONTENT