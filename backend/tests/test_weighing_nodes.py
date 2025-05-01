from flask.testing import FlaskClient
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from database.models.weighing_node import WeighingNode
from config.config import Config
from tests.utils import client, database_engine, default_admin_client


def test_get_nodes(default_admin_client: FlaskClient, database_engine: Engine):

    response = default_admin_client.get("/api/weighing-nodes")
    assert response.status_code == 200
    assert response.json == []

    ip_addresses = ["192.168.34.101", "10.0.57.8", "172.16.222.45"]

    for ip_address in ip_addresses:
        default_admin_client.post(
            "/api/weighing-nodes/registration/start",
            environ_base={"REMOTE_ADDR": ip_address},
            headers={"Authorization": Config.PRESHARED_KEY}
        )

    response = default_admin_client.get("/api/weighing-nodes")
    
    assert response.status_code == 200
    assert len(response.json) == 3