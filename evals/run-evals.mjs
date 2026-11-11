#!/usr/bin/env node
// Wave 1 retrieval evals against the local MCP door (npm run serve, 127.0.0.1:8080).
// In-scope: PASS when the expected stable_id is among the returned hits and the
// search did not abstain. Out-of-scope: PASS when the search abstains.
// Plain Node, no dependencies. Usage: node evals/run-evals.mjs [url]
import { readFileSync } from "node:fs";

const URL_ = process.argv[2] ?? "http://127.0.0.1:8080/mcp";
const K = 5;
let id = 0;

async function rpc(method, params) {
  const res = await fetch(URL_, {
    method: "POST",
    headers: { "content-type": "application/json", accept: "application/json, text/event-stream" },
    body: JSON.stringify({ jsonrpc: "2.0", id: ++id, method, params }),
  });
  const text = await res.text();
  const json = text.startsWith("{") ? JSON.parse(text)
    : JSON.parse(text.split("\n").filter((l) => l.startsWith("data:")).map((l) => l.slice(5)).join(""));
  if (json.error) throw new Error(`${method}: ${JSON.stringify(json.error)}`);
  return json.result;
}

async function search(query) {
  const r = await rpc("tools/call", { name: "search", arguments: { query, k: K } });
  return r.structuredContent ?? JSON.parse(r.content?.[0]?.text ?? "{}");
}

const lines = (f) => readFileSync(f, "utf8").split("\n").map((l) => l.trim()).filter((l) => l && !l.startsWith("#"));

await rpc("initialize", { protocolVersion: "2025-06-18", capabilities: {}, clientInfo: { name: "soc-handbook-evals", version: "1" } });

let pass = 0, total = 0;
console.log(`== in-scope (expected document in top ${K}, not abstained)`);
for (const line of ["evals/wave1-in-scope.tsv", "evals/wave2-in-scope.tsv", "evals/wave3-in-scope.tsv"].flatMap(lines)) {
  const [q, expected] = line.split("\t");
  const out = await search(q);
  const ids = (out.hits ?? []).map((h) => h.provenance?.stable_id ?? h.stable_id ?? h.slug);
  const ok = !out.abstained && ids.includes(expected);
  total++; if (ok) pass++;
  console.log(`${ok ? "PASS" : "FAIL"}  ${q}  -> ${ids.slice(0, 3).join(", ") || "(abstained)"}`);
}
const inPass = pass, inTotal = total;
pass = 0; total = 0;
console.log("== out-of-scope (must abstain)");
for (const q of lines("evals/wave1-out-of-scope.txt")) {
  const out = await search(q);
  const ok = out.abstained === true || (out.hits ?? []).length === 0;
  total++; if (ok) pass++;
  console.log(`${ok ? "PASS" : "FAIL"}  ${q}`);
}
console.log(`\nin-scope ${inPass}/${inTotal} (${Math.round((100 * inPass) / inTotal)}%) · out-of-scope ${pass}/${total} (${Math.round((100 * pass) / total)}%)`);
