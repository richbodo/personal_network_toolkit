// Clean fixture: every egress vector here is either local or allow-listed.
// Used by CI to prove egress-lint does not raise false positives on a
// conformant private-data-sovereignty posture.

// Same-origin / root-relative — local, never flagged.
await fetch("/api/shared-bundle");
await fetch("./manifest.json");

// localhost — local dev, not off-device.
const dev = new WebSocket("ws://localhost:5173");

// The one sanctioned remote origin for this flavor (see egress-allow.json).
await fetch("https://fellows.example.org/auth/session");

// Non-egress schemes — comms transport / inline data, not data egress.
const mail = "mailto:maintainer@fellows.example.org";
const inline = "data:image/svg+xml;base64,PHN2Zz48L3N2Zz4=";

// Relative dynamic import — local.
const mod = await import("./lib/render.js");
