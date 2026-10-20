# SIGNAL-LOST

Browser-based Tactical Command Trainer for DDIL environments. The current foundation connects the five Google Stitch screen exports while preserving their original HTML, inline styles, and design assets.

## Project structure

- `index.html` — root entry point; redirects to the Stitch landing export.
- `navigation.js` — shared route wiring loaded by each exported screen.
- `app.py` — Flask and Socket.IO server with room membership and role-authorized events.
- `simulation/engine.py` — seeded server-authoritative map, reports, disruption controls, and decision snapshots.
- `tests/test_server.py` — HTTP and Socket.IO coverage for room isolation, map filtering, target authorization, and decision data.
- `stitch files/*/code.html` — the five supplied Stitch implementations.
- `stitch files/*/screen.png` — supplied reference screenshots.
- `stitch files/*/DESIGN.md` — supplied design-system documentation.
- `pdf.html` and `26248_overview.pdf` — separate SIH solution-briefing material.

## Run locally

Create the environment once:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

Start the authoritative Flask-SocketIO server:

```powershell
py app.py
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000). Stop the server with `Ctrl+C`.

The exported screens currently load Tailwind CSS, Google Fonts, and Material Symbols from external CDNs, so those visual dependencies require an internet connection. The app itself needs no package installation or build step.

## Verified foundation flow

The local server and browser checks verified these paths:

`Landing → Role selection → Commando dashboard → AAR`

`Landing → Role selection → Disruption operator dashboard → AAR`

The Commando `End Scenario` control also reaches the AAR screen. The checks confirmed the expected page content after each navigation.

## Screens

- Landing page
- Role selection
- Commando dashboard
- Disruption operator dashboard
- After-action review

The current pages remain the original Stitch exports with a small runtime status overlay and an injected minimap panel. The backend provides in-memory rooms, room codes, role assignment, role-filtered state, Socket.IO events, disruption controls, decision records, and an event-backed AAR endpoint. Active rooms disappear when the server restarts.

## Minimap foundation

When the Operator starts a room, the server creates a seeded 12×8 abstract grid with non-overlapping commandos and synthetic hostile contacts. The Operator receives ground-truth positions. A Commando receives only their own position and delivered reports; reports include source, age, confidence, status, and a distance calculated from the reported position. Actual hostile positions are removed before the Commando payload is sent. The Operator can select a commando as the target of fictional delay, packet-loss, or outage controls. These controls affect simulation messages only.

## Test both players locally

1. Open the landing page in one browser window and choose Operational Simulator.
2. Choose Commando. The server creates a six-character room code and opens the Commando dashboard.
3. Open `http://127.0.0.1:8000` in a second private window or separate browser profile.
4. Choose Operational Simulator, choose Disruption Operator, and enter the room code when prompted.
5. The two windows connect to the same in-memory room. The Operator can start the simulation and apply synthetic delay, packet loss, and outage settings; the Commando receives only role-permitted state.

Run automated checks with:

```powershell
py -m pytest -q
```

The tests cover room creation/joining, duplicate-role and cross-room rejection, role-filtered HTTP state, Socket.IO synchronization/permissions, non-overlapping seeded maps, report filtering, target disruption, decision information snapshots, and unauthorized target selection.
