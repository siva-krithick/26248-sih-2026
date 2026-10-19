(() => {
  // Each export lives two directories below the server root:
  // /stitch files/<screen>/code.html -> ../../../ reaches /
  const root = new URL("../../../", window.location.href);
  const screens = {
    landing: "stitch files/stitch_signal_lost_command_trainer_landing/code.html",
    choosing: "stitch files/stitch_signal_lost_command_trainer_choosing/code.html",
    commando: "stitch files/stitch_signal_lost_command_trainer_commando/code.html",
    disop: "stitch files/stitch_signal_lost_command_trainer_disop/code.html",
    aar: "stitch files/stitch_signal_lost_command_trainer_aar/code.html",
  };
  const route = (screen) => new URL(screens[screen], root).href;
  const current = window.location.pathname;
  const isLanding = current.includes("_landing/");
  const isChoosing = current.includes("_choosing/");
  const isAar = current.includes("_aar/");
  const sessionKey = "signalLostSession";

  const currentSession = () => {
    const params = new URLSearchParams(window.location.search);
    const stored = JSON.parse(sessionStorage.getItem(sessionKey) || "null");
    return {
      room_code: params.get("room") || stored?.room_code,
      role: params.get("role") || stored?.role,
      player_token: params.get("player_token") || stored?.player_token,
    };
  };

  const withSession = (screen) => {
    const session = currentSession();
    if (!session.room_code || !session.player_token) return route(screen);
    const query = new URLSearchParams({
      room: session.room_code,
      role: session.role || "",
      player_token: session.player_token,
    });
    return `${route(screen)}?${query}`;
  };

  const showRuntimeStatus = (message, kind = "info") => {
    let status = document.getElementById("signal-lost-runtime-status");
    if (!status) {
      status = document.createElement("div");
      status.id = "signal-lost-runtime-status";
      status.className = "fixed bottom-4 right-4 z-[100] max-w-sm rounded bg-surface-container-lowest px-4 py-3 font-label-sm text-label-sm shadow-lg border border-outline-variant";
      document.body.appendChild(status);
    }
    status.dataset.kind = kind;
    status.textContent = message;
  };

  const renderMinimap = (state) => {
    if (isAar) return;
    const map = state?.map || { dimensions: { width: 12, height: 8 }, commandos: [], hostiles: [], reports: [] };
    let panel = document.getElementById("signal-lost-minimap");
    if (!panel) {
      panel = document.createElement("section");
      panel.id = "signal-lost-minimap";
      panel.className = "mx-margin my-space-md bg-surface-container-lowest border border-outline-variant/40 rounded-lg p-space-md shadow-sm";
      const main = document.querySelector("main");
      if (main) main.prepend(panel);
    }
    const width = map.dimensions.width;
    const height = map.dimensions.height;
    const scale = 28;
    const point = (position, color, label, extra = "") => {
      if (!position) return "";
      const x = (position.x + 0.5) * scale;
      const y = (position.y + 0.5) * scale;
      return `<g><circle cx="${x}" cy="${y}" r="7" fill="${color}" stroke="#ffffff" stroke-width="2"><title>${label}</title></circle>${extra}</g>`;
    };
    const grid = Array.from({ length: width + 1 }, (_, x) => `<line x1="${x * scale}" y1="0" x2="${x * scale}" y2="${height * scale}"/>`).join("")
      + Array.from({ length: height + 1 }, (_, y) => `<line x1="0" y1="${y * scale}" x2="${width * scale}" y2="${y * scale}"/>`).join("");
    let marks = "";
    if (state.role === "operator") {
      (map.commandos || []).forEach((item) => { marks += point(item.actual_position, "#00685f", item.id); });
      (map.hostiles || []).forEach((item) => { marks += point(item.actual_position, "#ba1a1a", item.id); });
    } else {
      marks += point(map.self?.position, "#00685f", "YOUR POSITION");
      (map.reports || []).forEach((report) => {
        const color = report.status === "stale" ? "#b15f00" : report.status === "conflicting" ? "#ba1a1a" : "#00687a";
        marks += point(report.reported_position, color, `${report.source} // ${report.status}`);
      });
    }
    const targetControls = state.role === "operator"
      ? `<div class="flex items-center gap-2 mt-2 font-label-sm text-label-sm"><span>DISRUPTION TARGET:</span>${(map.commandos || []).map((item) => `<button type="button" data-minimap-target="${item.id}" class="px-2 py-1 rounded bg-surface-container hover:bg-primary hover:text-on-primary">${item.id}${map.selected_target === item.id ? " // SELECTED" : ""}</button>`).join("")}</div>`
      : "";
    const role = state?.role || "commando";
    const status = state?.status || "waiting";
    panel.innerHTML = `<div class="flex items-center justify-between gap-2"><div><div class="font-label-sm text-label-sm text-primary uppercase">SHARED SYNTHETIC MINIMAP // ${role.toUpperCase()}</div><div class="font-title-sm text-title-sm">${status.toUpperCase()} // GRID ${width}×${height}</div></div><div class="font-label-sm text-on-surface-variant">${map.commandos?.length || map.self ? (role === "operator" ? "GROUND TRUTH VIEW" : "DELIVERED REPORT VIEW") : "AWAITING MAP INITIALIZATION"}</div></div><div class="mt-2 overflow-x-auto"><svg viewBox="0 0 ${width * scale} ${height * scale}" class="w-full min-w-[420px] max-h-64 bg-surface-container-low" role="img" aria-label="Synthetic grid minimap"><g stroke="#bcc9c6" stroke-width="1" opacity="0.65">${grid}</g>${marks}</svg></div><div class="flex flex-wrap gap-3 mt-2 font-label-sm text-label-sm text-on-surface-variant"><span><i class="inline-block w-2 h-2 rounded-full bg-primary mr-1"></i>FRIENDLY / SELF</span><span><i class="inline-block w-2 h-2 rounded-full bg-error mr-1"></i>SYNTHETIC HOSTILE</span><span><i class="inline-block w-2 h-2 rounded-full bg-tertiary mr-1"></i>STALE REPORT</span><span><i class="inline-block w-2 h-2 rounded-full bg-secondary mr-1"></i>DELIVERED / UNCERTAINTY</span></div>${targetControls}`;
    panel.querySelectorAll("[data-minimap-target]").forEach((button) => {
      button.addEventListener("click", () => window.signalLostSocket?.emit("select_disruption_target", { commando_id: button.dataset.minimapTarget }));
    });
  };

  const api = async (path, options = {}) => {
    const response = await fetch(path, {
      headers: { "Content-Type": "application/json", ...(options.headers || {}) },
      ...options,
    });
    const body = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(body.error || `Request failed (${response.status})`);
    return body;
  };

  const enterRole = async (role) => {
    try {
      let result;
      if (role === "commando") {
        result = await api("/api/rooms", { method: "POST", body: JSON.stringify({ role }) });
      } else {
        const roomCode = window.prompt("Enter the six-character room code created by the Commando:");
        if (!roomCode) return;
        result = await api(`/api/rooms/${encodeURIComponent(roomCode.trim())}/join`, {
          method: "POST",
          body: JSON.stringify({ role }),
        });
      }
      sessionStorage.setItem(sessionKey, JSON.stringify(result));
      window.location.assign(withSession(role === "commando" ? "commando" : "disop"));
    } catch (error) {
      showRuntimeStatus(error.message, "error");
    }
  };

  const loadSocketClient = () => new Promise((resolve, reject) => {
    if (window.io) return resolve(window.io);
    const script = document.createElement("script");
    // The Python Socket.IO server speaks the standard v4 browser protocol.
    // Stitch already depends on CDN-hosted UI assets, so reuse that dependency
    // boundary instead of adding a generated vendor bundle to the exports.
    script.src = "https://cdn.socket.io/4.8.1/socket.io.min.js";
    script.onload = () => resolve(window.io);
    script.onerror = reject;
    document.head.appendChild(script);
  });

  const startRuntime = async () => {
    const session = currentSession();
    if (!session.room_code || !session.player_token || !session.role) {
      showRuntimeStatus("STATIC DESIGN PREVIEW — return to Role Selection to join a room.");
      return;
    }
    try {
      const state = await api(`/api/rooms/${encodeURIComponent(session.room_code)}/state?role=${encodeURIComponent(session.role)}&player_token=${encodeURIComponent(session.player_token)}`);
      showRuntimeStatus(`ROOM ${session.room_code} // ${session.role.toUpperCase()} // ${state.status.toUpperCase()}`);
      renderMinimap(state);
      const io = await loadSocketClient();
      const socket = io();
      window.signalLostSocket = socket;
      window.signalLostState = state;
      renderMinimap(state);
      socket.on("connect", () => socket.emit("join_simulation", session));
      socket.on("session_state", (nextState) => {
        window.signalLostState = nextState;
        renderMinimap(nextState);
        document.dispatchEvent(new CustomEvent("signal-lost-state", { detail: nextState }));
        showRuntimeStatus(`ROOM ${session.room_code} // ${nextState.status.toUpperCase()} // LIVE`);
      });
      socket.on("session_error", (event) => showRuntimeStatus(event.error, "error"));
      socket.on("disconnect", () => showRuntimeStatus("SIMULATION CONNECTION LOST — attempting to reconnect…", "error"));

      if (session.role === "operator") {
        document.querySelector('[title="Start Scenario"]')?.addEventListener("click", () => socket.emit("start_simulation"));
        document.querySelector('[title="Pause Simulation"]')?.addEventListener("click", () => socket.emit("pause_simulation"));
        document.querySelector('[title="Reset Exercise"]')?.addEventListener("click", () => socket.emit("reset_simulation"));
        document.getElementById("applyInjectBtn")?.addEventListener("click", () => {
          socket.emit("apply_disruption", {
            delay_ms: Number(document.getElementById("delaySlider")?.value || 0) * 1000,
            packet_loss: Number(document.getElementById("lossSlider")?.value || 0),
            outage: false,
            target_commando_id: window.signalLostState?.map?.selected_target || null,
          });
        });
      }

      if (session.role === "commando") {
        document.getElementById("decision-form")?.addEventListener("submit", (event) => {
          event.preventDefault();
          const selected = document.querySelector('input[name="tactical-option"]:checked');
          if (!selected) return;
          socket.emit("submit_decision", {
            option: selected.value,
            rationale: document.getElementById("rationale")?.value || "",
          });
          const toast = document.getElementById("action-toast");
          if (toast) toast.classList.remove("hidden");
        });
      }

      if (isAar) {
        const aar = await api(`/api/rooms/${encodeURIComponent(session.room_code)}/aar?player_token=${encodeURIComponent(session.player_token)}`);
        window.signalLostAar = aar;
        showRuntimeStatus(`AAR LOADED // ${aar.metrics.messages_total} RECORDED MESSAGES`);
      }
    } catch (error) {
      showRuntimeStatus(error.message, "error");
    }
  };

  const destinations = {
    "commando-terminal": "commando",
    "disruption-terminal": "disop",
    "operational-simulator": "choosing",
    "after-action-review": "aar",
    "run-again": "choosing",
    "home": "landing",
    "overview": isChoosing ? "landing" : isLanding ? "landing" : null,
    "role-selection": "choosing",
  };

  document.querySelectorAll("[data-path]").forEach((element) => {
    const path = element.getAttribute("data-path");
    let screen = destinations[path];

    if (path === "scenarios") {
      element.href = route("landing") + "#featured-scenarios";
      return;
    }
    if (path === "tactical-doctrine") {
      element.href = new URL("pdf.html", root).href;
      return;
    }
    if (path === "overview" && (isLanding || isAar)) {
      element.href = "#";
      return;
    }
    if (path === "aar-engine") screen = "aar";
    if (path === "overview" && !screen) screen = "landing";
    if (screen) element.href = withSession(screen);
  });

  document.addEventListener("click", (event) => {
    const link = event.target.closest("[data-path]");
    if (!link) {
      const button = event.target.closest("button");
      if (button && button.textContent.includes("End Scenario")) {
        event.preventDefault();
        event.stopImmediatePropagation();
        window.location.assign(withSession("aar"));
      }
      return;
    }
    const path = link.getAttribute("data-path");
    if (isChoosing && (path === "commando-terminal" || path === "disruption-terminal")) {
      event.preventDefault();
      event.stopImmediatePropagation();
      enterRole(path === "commando-terminal" ? "commando" : "operator");
      return;
    }
    const destination = link.getAttribute("href");
    if (!destination || destination === "#") return;
    event.preventDefault();
    event.stopImmediatePropagation();
    if (path === "after-action-review" && window.signalLostSocket && currentSession().role === "operator") {
      window.signalLostSocket.emit("finish_simulation");
      window.setTimeout(() => window.location.assign(destination), 150);
      return;
    }
    window.location.assign(destination);
  }, true);

  if (!isChoosing && !isLanding) startRuntime();
})();
