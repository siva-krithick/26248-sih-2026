from app import app, socketio, store, socket_memberships


def setup_function():
    store.rooms.clear()
    socket_memberships.clear()


def test_create_join_role_filtered_state_and_aar():
    client = app.test_client()
    created = client.post("/api/rooms", json={"role": "commando"}).get_json()
    joined = client.post(f"/api/rooms/{created['room_code']}/join", json={"role": "operator"}).get_json()

    commando = client.get(
        f"/api/rooms/{created['room_code']}/state?role=commando&player_token={created['player_token']}"
    )
    operator = client.get(
        f"/api/rooms/{created['room_code']}/state?role=operator&player_token={joined['player_token']}"
    )

    assert commando.status_code == 200
    assert operator.status_code == 200
    assert "events" not in commando.get_json()
    assert "events" in operator.get_json()


def test_duplicate_role_and_cross_room_are_denied():
    client = app.test_client()
    first = client.post("/api/rooms", json={"role": "operator"}).get_json()
    duplicate = client.post(f"/api/rooms/{first['room_code']}/join", json={"role": "operator"})
    forbidden = client.get(
        f"/api/rooms/{first['room_code']}/state?role=operator&player_token=wrong-token"
    )
    missing = client.get("/api/rooms/ZZZZZZ/state?role=commando&player_token=wrong-token")

    assert duplicate.status_code == 409
    assert forbidden.status_code == 403
    assert missing.status_code == 404


def test_socketio_sync_and_role_permissions():
    room, commando = store.create("commando")
    _, operator = store.join(room.code, "operator")
    commando_client = socketio.test_client(app)
    operator_client = socketio.test_client(app)

    commando_client.emit(
        "join_simulation",
        {"room_code": room.code, "role": "commando", "player_token": commando.token},
    )
    operator_client.emit(
        "join_simulation",
        {"room_code": room.code, "role": "operator", "player_token": operator.token},
    )
    operator_client.emit("start_simulation")

    commando_messages = commando_client.get_received()
    assert any(message["name"] == "session_state" and message["args"][0]["status"] == "running" for message in commando_messages)

    commando_client.emit("apply_disruption", {"delay_ms": 900, "packet_loss": 20, "outage": False})
    assert any(message["name"] == "session_error" for message in commando_client.get_received())

    operator_client.emit("apply_disruption", {"delay_ms": 900, "packet_loss": 20, "outage": False})
    assert any(
        message["name"] == "session_state"
        and message["args"][0]["communication"]["delay_ms"] == 900
        for message in commando_client.get_received()
    )


def test_seeded_map_is_non_overlapping_and_role_filtered():
    room, commando = store.create("commando")
    _, operator = store.join(room.code, "operator")
    room.start()

    operator_state = room.public_state("operator", operator.token)
    commando_state = room.public_state("commando", commando.token)
    map_state = operator_state["map"]
    positions = [tuple(item["actual_position"].values()) for item in map_state["commandos"]]
    positions += [tuple(item["actual_position"].values()) for item in map_state["hostiles"]]
    assert len(positions) == len(set(positions))
    assert all("actual_position" in item for item in map_state["hostiles"])
    assert all("actual_position" not in item for item in commando_state["map"]["reports"])
    assert any(item["status"] == "stale" for item in commando_state["map"]["reports"])
    assert all(item["status"] != "missing" for item in commando_state["map"]["reports"])
    assert all("reported_distance" in item for item in commando_state["map"]["reports"])


def test_target_disruption_and_decision_snapshot_use_server_data():
    room, commando = store.create("commando")
    store.join(room.code, "operator")
    room.start()
    room.select_target("CMD-01")
    room.apply_controls(800, 100, False, "CMD-01")
    dropped = room.queue_message("OPERATOR", "Synthetic test message")
    assert dropped["delivered"] is False
    decision = room.submit_decision("C", "Hold and request confirmation")
    assert decision["available_information"]["reports"]
    assert all("actual_position" not in report for report in decision["available_information"]["reports"])


def test_unauthorized_target_selection_is_rejected():
    room, commando = store.create("commando")
    _, operator = store.join(room.code, "operator")
    commando_client = socketio.test_client(app)
    operator_client = socketio.test_client(app)
    commando_client.emit("join_simulation", {"room_code": room.code, "player_token": commando.token})
    operator_client.emit("join_simulation", {"room_code": room.code, "player_token": operator.token})
    operator_client.emit("start_simulation")
    commando_client.emit("select_disruption_target", {"commando_id": "CMD-01"})
    assert any(message["name"] == "session_error" for message in commando_client.get_received())
