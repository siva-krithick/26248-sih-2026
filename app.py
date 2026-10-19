from __future__ import annotations

from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit, join_room as socket_join_room

from simulation.engine import RoomStore


ROOT = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=str(ROOT), static_url_path="")
app.config["SECRET_KEY"] = "signal-lost-prototype"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
store = RoomStore()
socket_memberships: dict[str, tuple[str, str]] = {}


def get_room(code: str):
    room = store.rooms.get(code.upper())
    if room is None:
        return None, (jsonify({"error": "Room not found"}), 404)
    return room, None


def require_member(room, role: str, token: str | None):
    player = room.players.get(role)
    if not player or player.token != token:
        return jsonify({"error": "Forbidden"}), 403
    return None


@app.get("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.post("/api/rooms")
def create_room():
    payload = request.get_json(silent=True) or {}
    try:
        room, player = store.create(payload.get("role", ""))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"room_code": room.code, "role": player.role, "player_token": player.token})


@app.post("/api/rooms/<code>/join")
def join_room(code: str):
    payload = request.get_json(silent=True) or {}
    try:
        room, player = store.join(code, payload.get("role", ""))
    except LookupError as error:
        return jsonify({"error": str(error)}), 404
    except (PermissionError, ValueError) as error:
        return jsonify({"error": str(error)}), 409
    return jsonify({"room_code": room.code, "role": player.role, "player_token": player.token})


@app.get("/api/rooms/<code>/state")
def room_state(code: str):
    room, error = get_room(code)
    if error:
        return error
    role = request.args.get("role", "")
    token = request.args.get("player_token")
    denied = require_member(room, role, token)
    if denied:
        return denied
    return jsonify(room.public_state(role, token))


@app.get("/api/rooms/<code>/aar")
def room_aar(code: str):
    room, error = get_room(code)
    if error:
        return error
    token = request.args.get("player_token")
    if room.role_for_token(token) is None:
        return jsonify({"error": "Forbidden"}), 403
    return jsonify(room.aar(token))


@socketio.on("connect")
def handle_connect():
    emit("connected", {"transport": "socketio"})


@socketio.on("join_simulation")
def handle_join(data):
    code = str(data.get("room_code", "")).upper()
    token = data.get("player_token")
    room = store.rooms.get(code)
    role = room.role_for_token(token) if room else None
    if not room or not role:
        emit("session_error", {"error": "Invalid room membership"})
        return
    socket_memberships[request.sid] = (code, role)
    room.players[role].connected = True
    socket_join_room(code)
    emit("session_state", room.public_state(role, token))
    socketio.emit("participant_status", {"role": role, "connected": True}, to=code)


@socketio.on("start_simulation")
def handle_start(data=None):
    membership = socket_memberships.get(request.sid)
    room = store.rooms.get(membership[0]) if membership else None
    if not room or membership[1] != "operator":
        emit("session_error", {"error": "Operator role required"})
        return
    try:
        if room.status == "paused":
            room.status = "running"
            room.add_event("simulation_resumed")
        else:
            room.start()
    except ValueError as error:
        emit("session_error", {"error": str(error)})
        return
    broadcast_state(room)


@socketio.on("pause_simulation")
def handle_pause():
    membership = socket_memberships.get(request.sid)
    room = store.rooms.get(membership[0]) if membership else None
    if not room or membership[1] != "operator":
        emit("session_error", {"error": "Operator role required"})
        return
    if room.status == "running":
        room.status = "paused"
        room.add_event("simulation_paused")
    broadcast_state(room)


@socketio.on("reset_simulation")
def handle_reset():
    membership = socket_memberships.get(request.sid)
    room = store.rooms.get(membership[0]) if membership else None
    if not room or membership[1] != "operator":
        emit("session_error", {"error": "Operator role required"})
        return
    room.status = "waiting"
    room.controls = {"delay_ms": 0, "packet_loss": 0, "outage": False, "target_commando_id": None}
    room.commandos = {}
    room.hostiles = []
    room.reports = []
    room.add_event("simulation_reset")
    broadcast_state(room)


@socketio.on("apply_disruption")
def handle_disruption(data):
    membership = socket_memberships.get(request.sid)
    room = store.rooms.get(membership[0]) if membership else None
    if not room or membership[1] != "operator":
        emit("session_error", {"error": "Operator role required"})
        return
    try:
        room.apply_controls(
            data.get("delay_ms", 0), data.get("packet_loss", 0), data.get("outage", False),
            data.get("target_commando_id"),
        )
    except ValueError as error:
        emit("session_error", {"error": str(error)})
        return
    broadcast_state(room)


@socketio.on("select_disruption_target")
def handle_target_selection(data):
    membership = socket_memberships.get(request.sid)
    room = store.rooms.get(membership[0]) if membership else None
    if not room or membership[1] != "operator":
        emit("session_error", {"error": "Operator role required"})
        return
    try:
        room.select_target(str(data.get("commando_id", "")))
    except ValueError as error:
        emit("session_error", {"error": str(error)})
        return
    broadcast_state(room)


@socketio.on("submit_decision")
def handle_decision(data):
    membership = socket_memberships.get(request.sid)
    room = store.rooms.get(membership[0]) if membership else None
    if not room or membership[1] != "commando":
        emit("session_error", {"error": "Commando role required"})
        return
    room.submit_decision(str(data.get("option", "")), str(data.get("rationale", "")))
    broadcast_state(room)


@socketio.on("finish_simulation")
def handle_finish():
    membership = socket_memberships.get(request.sid)
    room = store.rooms.get(membership[0]) if membership else None
    if not room or membership[1] != "operator":
        emit("session_error", {"error": "Operator role required"})
        return
    room.finish()
    broadcast_state(room)


@socketio.on("disconnect")
def handle_disconnect():
    membership = socket_memberships.pop(request.sid, None)
    if not membership:
        return
    room = store.rooms.get(membership[0])
    if room and membership[1] in room.players:
        room.players[membership[1]].connected = False
        socketio.emit("participant_status", {"role": membership[1], "connected": False}, to=room.code)


def broadcast_state(room) -> None:
    for role, player in room.players.items():
        if player.connected:
            socketio.emit("session_state", room.public_state(role, player.token), to=room.code)


if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=8000, debug=False)
