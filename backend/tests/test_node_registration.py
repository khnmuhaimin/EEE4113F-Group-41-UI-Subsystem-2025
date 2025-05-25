from uuid import UUID
from flask.testing import FlaskClient
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from database.models.weighing_node import WeighingNode
from config.config import Config
from tests.utils import client, database_engine, default_admin_client
import pytest


def test_successful_start_node_registration(client: FlaskClient, database_engine: Engine):
    print("")
    node_ids = set()
    node_api_keys = set()

    print("Starting the registration process for 3 weighing nodes.")
    for i in range(3):
        response = client.post(
            "/api/weighing-nodes/registration/start",
        )

        assert response.status_code == 200
        response_body = response.get_data(as_text=True)
        response_body_lines = response_body.split()
        assert len(response_body_lines) == 2
        node_ids.add(response_body_lines[0])
        node_api_keys.add(response_body_lines[1])

    print("Confirming that new unregistered nodes were added to the database.")
    assert len(node_ids) == 3
    assert len(node_api_keys) == 3
    

def test_successful_approval_of_weighing_node_registration(default_admin_client: FlaskClient, database_engine: Engine):
    print("")

    print("Inserting an unregistered node into the database.")
    default_admin_client.post(
        "/api/weighing-nodes/registration/start"
    )

    response = default_admin_client.get("/api/weighing-nodes/registration/in-progress")
    node_in_registration = response.json[0]

    print("Approving the newly created node.")
    response = default_admin_client.post(
        "/api/weighing-nodes/registration/approve",
        json={"weighing_node_id": node_in_registration["id"]}
    )

    assert response.status_code == 204

    print("Confirming the node is marked with registration being complete.")
    with Session(database_engine) as session:
        registered_node = session.scalar(select(WeighingNode).where(WeighingNode.uuid == UUID(node_in_registration["id"])))
        assert registered_node is not None
        assert registered_node.registration_in_progress == False



def test_unsuccessful_approval_of_weighing_node_registration_due_to_missing_id(default_admin_client: FlaskClient, database_engine: Engine):

    response = default_admin_client.post(
        "/api/weighing-nodes/registration/approve",
        json={"wrong key": "wrong value"}
    )

    assert response.status_code == 400
    assert response.json["message"] == "The weighing node's ID is missing."


@pytest.mark.parametrize("weighing_node_id", ["an invalid id", 19387, 348.3, None, ""])
def test_unsuccessful_approval_of_weighing_node_registration_due_to_invalid_id(weighing_node_id, default_admin_client: FlaskClient, database_engine: Engine):
    response = default_admin_client.post(
        "/api/weighing-nodes/registration/approve",
        json={"weighing_node_id": weighing_node_id}
    )
    assert response.status_code == 422
    assert response.json["message"] == "The weighing node's ID is invalid."



