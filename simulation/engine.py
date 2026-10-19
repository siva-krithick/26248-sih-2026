from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import math
import random
import secrets
import string
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def make_room_code() -> str:
    return "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))


@dataclass
class Player:
    token: str
    role: str
    connected: bool = False


@dataclass
class SimulationRoom:
    code: str
    seed: int
    created_at: str = field(default_factory=utc_now)
    status: str = "waiting"
    players: dict[str, Player] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    decisions: list[dict[str, Any]] = field(default_factory=list)
    controls: dict[str, Any] = field(
        default_factory=lambda: {"delay_ms": 0, "packet_loss": 0, "outage": False, "target_commando_id": None}
    )
    map_dimensions: dict[str, int] = field(default_factory=lambda: {"width": 12, "height": 8})
    commandos: dict[str, dict[str, Any]] = field(default_factory=dict)
    hostiles: list[dict[str, Any]] = field(default_factory=list)
    reports: list[dict[str, Any]] = field(default_factory=list)
    rng: random.Random = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.rng = random.Random(self.seed)

    def add_event(self, event_type: str, **details: Any) -> dict[str, Any]:
        event = {"id": len(self.events) + 1, "at": utc_now(), "type": event_type, **details}
        self.events.append(event)
        return event

    def role_for_token(self, token: str | None) -> str | None:
        for player in self.players.values():
            if player.token == token:
                return player.role
        return None

    def _report_for_commando(self, report: dict[str, Any], own_position: dict[str, int]) -> dict[str, Any]:
        projected = {key: value for key, value in report.items() if key != "actual_position"}
        projected["reported_distance"] = round(
            math.hypot(
                report["reported_position"]["x"] - own_position["x"],
                report["reported_position"]["y"] - own_position["y"],
            ),
            2,
        )
        return projected

    def operator_map(self) -> dict[str, Any]:
        return {
            "dimensions": dict(self.map_dimensions),
            "commandos": [dict(item) for item in self.commandos.values()],
            "hostiles": [dict(item) for item in self.hostiles],
            "reports": [dict(item) for item in self.reports],
            "selected_target": self.controls.get("target_commando_id"),
        }

    def public_state(self, role: str, token: str) -> dict[str, Any]:
        player = self.players.get(role)
        if not player or player.token != token:
            raise PermissionError("Invalid room membership")
        base = {
            "room_code": self.code,
            "status": self.status,
            "role": role,
            "players": {
                key: {"connected": value.connected}
                for key, value in self.players.items()
            },
        }
        if role == "operator":
            base.update(
                {
                    "controls": dict(self.controls),
                    "events": list(self.events),
                    "decisions": list(self.decisions),
                    "map": self.operator_map(),
                }
            )
        else:
            own = self.commandos.get("CMD-01", {"actual_position": {"x": 0, "y": 0}})
            delivered = [self._report_for_commando(report, own["actual_position"]) for report in self.reports if report["delivered"]]
            base.update(
                {
                    "messages": delivered,
                    "map": {
                        "dimensions": dict(self.map_dimensions),
                        "self": {"id": "CMD-01", "position": dict(own["actual_position"])},
                        "reports": delivered,
                    },
                    "decisions": [d for d in self.decisions if d.get("role") == "commando"],
                    "communication": {
                        "delay_ms": self.controls["delay_ms"],
                        "packet_loss": self.controls["packet_loss"],
                        "outage": self.controls["outage"],
                    },
                }
            )
        return base

    def start(self) -> dict[str, Any]:
        if not {"commando", "operator"}.issubset(self.players):
            raise ValueError("Both roles must join before starting")
        self.generate_map()
        self.status = "running"
        return self.add_event("simulation_started", seed=self.seed, map_dimensions=self.map_dimensions)

    def _position(self, occupied: set[tuple[int, int]]) -> dict[str, int]:
        available = [
            (x, y)
            for y in range(self.map_dimensions["height"])
            for x in range(self.map_dimensions["width"])
            if (x, y) not in occupied
        ]
        if not available:
            raise ValueError("Map has no unoccupied cells")
        x, y = self.rng.choice(available)
        occupied.add((x, y))
        return {"x": x, "y": y}

    def generate_map(self) -> None:
        """Create a deterministic, non-overlapping abstract scenario map."""
        occupied: set[tuple[int, int]] = set()
        self.commandos = {"CMD-01": {"id": "CMD-01", "role": "commando", "actual_position": self._position(occupied)}}
        self.hostiles = [
            {"id": f"HST-{index:02d}", "label": label, "actual_position": self._position(occupied)}
            for index, label in enumerate(("ECHO", "GHOST", "SPECTER", "DECOY"), start=1)
        ]
        self.reports = []
        statuses = ("fresh", "stale", "conflicting", "missing")
        sources = ("RECON-1", "SENSOR-S3", "UAV-09", "SQUAD-BRAVO")
        for index, hostile in enumerate(self.hostiles):
            actual = hostile["actual_position"]
            reported = {
                "x": max(0, min(self.map_dimensions["width"] - 1, actual["x"] + (index % 3) - 1)),
                "y": max(0, min(self.map_dimensions["height"] - 1, actual["y"] + (index % 2))),
            }
            self.reports.append({
                "id": f"RPT-{index + 1:02d}", "contact_id": hostile["id"], "source": sources[index],
                "reported_position": reported, "actual_position": dict(actual), "created_at": utc_now(),
                "age_seconds": (2, 34, 8, 0)[index], "confidence": (0.92, 0.48, 0.61, 0.25)[index],
                "status": statuses[index], "delivered": statuses[index] != "missing",
            })
        conflict = dict(self.reports[2])
        conflict["id"], conflict["source"], conflict["reported_position"] = "RPT-05", "PASSIVE-ARRAY", self._position(set())
        self.reports.append(conflict)
        self.add_event("map_generated", commandos=list(self.commandos), hostiles=[h["id"] for h in self.hostiles])

    def select_target(self, commando_id: str) -> dict[str, Any]:
        if commando_id not in self.commandos:
            raise ValueError("Unknown disruption target")
        self.controls["target_commando_id"] = commando_id
        return self.add_event("disruption_target_selected", target_commando_id=commando_id)

    def apply_controls(self, delay_ms: int, packet_loss: int, outage: bool, target_commando_id: str | None = None) -> dict[str, Any]:
        target = target_commando_id or self.controls.get("target_commando_id")
        if target is not None and target not in self.commandos:
            raise ValueError("Unknown disruption target")
        self.controls = {
            "delay_ms": max(0, min(int(delay_ms), 120000)),
            "packet_loss": max(0, min(int(packet_loss), 100)),
            "outage": bool(outage),
            "target_commando_id": target,
        }
        return self.add_event("disruption_updated", controls=dict(self.controls))

    def queue_message(self, source: str, content: str, target_commando_id: str = "CMD-01") -> dict[str, Any]:
        targeted = self.controls.get("target_commando_id") in (None, target_commando_id)
        lost = targeted and self.rng.random() < self.controls["packet_loss"] / 100
        outage = targeted and self.controls["outage"]
        event = self.add_event(
            "message",
            source=source,
            content=content,
            target_commando_id=target_commando_id,
            delivered=not lost and not outage,
            delay_ms=self.controls["delay_ms"] if targeted else 0,
            delivery_status="dropped" if lost else ("held" if outage else "delivered"),
        )
        return event

    def submit_decision(self, option: str, rationale: str) -> dict[str, Any]:
        own = self.commandos.get("CMD-01", {"actual_position": {"x": 0, "y": 0}})
        visible_reports = [self._report_for_commando(report, own["actual_position"]) for report in self.reports if report["delivered"]]
        decision = {
            "id": len(self.decisions) + 1,
            "at": utc_now(),
            "role": "commando",
            "option": option,
            "rationale": rationale[:180],
            "available_message_ids": [
                event["id"]
                for event in self.events
                if event.get("type") == "message" and event.get("delivered")
            ],
            "available_information": {
                "own_position": dict(own["actual_position"]),
                "reports": visible_reports,
            },
        }
        self.decisions.append(decision)
        self.add_event("decision_submitted", decision_id=decision["id"], option=option)
        return decision

    def finish(self) -> dict[str, Any]:
        self.status = "ended"
        return self.add_event("simulation_finished")

    def aar(self, token: str) -> dict[str, Any]:
        if self.role_for_token(token) is None:
            raise PermissionError("Invalid room membership")
        messages = [event for event in self.events if event.get("type") == "message"]
        delivered = [event for event in messages if event.get("delivered")]
        return {
            "room_code": self.code,
            "status": self.status,
            "seed": self.seed,
            "events": list(self.events),
            "decisions": list(self.decisions),
            "metrics": {
                "messages_total": len(messages),
                "messages_delivered": len(delivered),
                "messages_dropped": len(messages) - len(delivered),
                "observed_delay_ms": [event.get("delay_ms", 0) for event in messages],
            },
        }


class RoomStore:
    def __init__(self) -> None:
        self.rooms: dict[str, SimulationRoom] = {}

    def create(self, role: str) -> tuple[SimulationRoom, Player]:
        if role not in {"commando", "operator"}:
            raise ValueError("Unsupported role")
        while True:
            code = make_room_code()
            if code not in self.rooms:
                break
        room = SimulationRoom(code=code, seed=secrets.randbelow(2**31))
        player = Player(token=secrets.token_urlsafe(18), role=role)
        room.players[role] = player
        room.add_event("room_created", role=role)
        self.rooms[code] = room
        return room, player

    def join(self, code: str, role: str) -> tuple[SimulationRoom, Player]:
        room = self.rooms.get(code.upper())
        if not room:
            raise LookupError("Room not found")
        if room.status == "ended":
            raise ValueError("Room has ended")
        if role not in {"commando", "operator"}:
            raise ValueError("Unsupported role")
        if role in room.players:
            raise PermissionError("Role is already occupied")
        player = Player(token=secrets.token_urlsafe(18), role=role)
        room.players[role] = player
        room.add_event("player_joined", role=role)
        return room, player

