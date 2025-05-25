from flask.testing import FlaskClient
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from database.models.weighing_node import WeighingNode
from config.config import Config
from tests.utils import client, database_engine, default_admin_client


def test_get_nodes(default_admin_client: FlaskClient, database_engine: Engine):

    response = default_admin_client.get("/api/weighing-nodes/all")
    assert response.status_code == 200
    start_num_nodes = len(response.json)

    for i in range(3):
        response = default_admin_client.post(
            "/api/weighing-nodes/registration/start",
        )
        print(response)

    response = default_admin_client.get("/api/weighing-nodes/all")
    
    assert response.status_code == 200
    assert len(response.json) == 3 + start_num_nodes