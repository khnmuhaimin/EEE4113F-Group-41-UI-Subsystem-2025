from flask import Blueprint, jsonify, request
from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.auth import generate_secret, hash_secret, verify_preshared_key
from database.models.registration_task import RegistrationTask
from database.database import database_engine


weighing_node_blueprint = Blueprint("weighing_node", __name__, url_prefix='/weighing-nodes')


@weighing_node_blueprint.route("/registration/start", methods=["POST"])
def start_registration():
    # authenticate node
    auth_header = request.headers.get("Authorization")
    correct_key = verify_preshared_key(auth_header)
    if not correct_key:
        return ("Invalid key.", 401)
    # add new registration task to database
    with Session(database_engine) as session:
        client_ip_address = request.remote_addr
        task = RegistrationTask(ip_address=client_ip_address)
        task.api_key = generate_secret()
        task.hashed_api_key = hash_secret(task.api_key)
        session.add(task)
        session.commit()
        uuid = task.task_id
        api_key = task.api_key
    # TODO: alert admin
    return (f"{uuid}\n{api_key}\n", 200)


@weighing_node_blueprint.route("/registration/tasks")
def get_registration_tasks():
    
    with Session(database_engine) as session:
        tasks = session.scalars(select(RegistrationTask)).all()
    tasks = list(map(lambda t: t.admin_view(), tasks))
    tasks.sort(key=lambda t: t["created_at"])
    return jsonify(tasks)


    