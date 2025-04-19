from flask.testing import FlaskClient
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from database.models.weighing_node import WeighingNode
from config.config import Config
from tests.utils import client, database_engine, default_admin_client


def test_successful_start_node_registration(client: FlaskClient, database_engine: Engine):
    ip_addresses = set(["192.168.34.101", "10.0.57.8", "172.16.222.45"])
    node_ids = set()
    node_api_keys = set()

    for ip_address in ip_addresses:
        response = client.post(
            "/weighing-nodes/registration/start",
            environ_base={"REMOTE_ADDR": ip_address},
            headers={"Authorization": Config.PRESHARED_KEY}
        )

        assert response.status_code == 200
        response_body = response.get_data(as_text=True)
        response_body_lines = response_body.split()
        assert len(response_body_lines) == 2
        node_ids.add(response_body_lines[0])
        node_api_keys.add(response_body_lines[1])

    assert len(node_ids) == len(ip_addresses)
    assert len(node_api_keys) == len(ip_addresses)

    with Session(database_engine) as session:
        nodes = session.scalars(select(WeighingNode)).all()
        assert len(nodes) == len(ip_addresses)


def test_unsuccessful_start_node_registration_due_missing_preshared_key(client: FlaskClient):
    ip_address = "192.168.34.101"

    response = client.post(
        "/weighing-nodes/registration/start",
        environ_base={"REMOTE_ADDR": ip_address}
    )

    assert response.status_code == 401
    assert response.get_data(as_text=True) == "Authorization header is missing."


def test_unsuccessful_start_node_registration_due_invalid_preshared_key(client: FlaskClient):
    ip_address = "192.168.34.101"

    response = client.post(
        "/weighing-nodes/registration/start",
        environ_base={"REMOTE_ADDR": ip_address},
        headers={"Authorization": "Incorrect preshared key"}
    )

    assert response.status_code == 401
    assert response.get_data(as_text=True) == "Invalid key."


def test_unsuccessful_start_node_registration_due_to_invalid_ip_address(client: FlaskClient):
    ip_address = "an invalid ip address"

    response = client.post(
        "/weighing-nodes/registration/start",
        environ_base={"REMOTE_ADDR": ip_address},
        headers={"Authorization": Config.PRESHARED_KEY}
    )

    assert response.status_code == 422
    assert response.get_data(as_text=True) == "IP Address is invalid."


def test_unsuccessful_start_node_registration_due_ip_address_already_in_use(client: FlaskClient):
    ip_address = "192.168.34.101"

    client.post(
        "/weighing-nodes/registration/start",
        environ_base={"REMOTE_ADDR": ip_address},
        headers={"Authorization": Config.PRESHARED_KEY}
    )

    response = client.post(
        "/weighing-nodes/registration/start",
        environ_base={"REMOTE_ADDR": ip_address},
        headers={"Authorization": Config.PRESHARED_KEY}
    )

    assert response.status_code == 409
    assert response.get_data(as_text=True) == "The IP address is already in use."
        

def test_get_nodes_where_registration_is_in_progress(default_admin_client: FlaskClient, database_engine: Engine):

    response = default_admin_client.get("/weighing-nodes/registration/in-progress")
    assert response.status_code == 200
    assert response.json == []

    ip_addresses = ["192.168.34.101", "10.0.57.8", "172.16.222.45"]

    for ip_address in ip_addresses:
        default_admin_client.post(
            "/weighing-nodes/registration/start",
            environ_base={"REMOTE_ADDR": ip_address},
            headers={"Authorization": Config.PRESHARED_KEY}
        )

    with Session(database_engine) as session:
        registered_node = session.scalar(select(WeighingNode).where(WeighingNode.ip_address == ip_addresses[0]))
        registered_node.registration_in_progress = False
        session.commit()

    response = default_admin_client.get("/weighing-nodes/registration/in-progress")
    
    assert response.status_code == 200
    assert len(response.json) == 2

    

    