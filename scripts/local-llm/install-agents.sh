#!/usr/bin/env bash
# Stellt den lokalen Harness fuer den Paperclip-Benutzer "agents" bereit (als Admin ausfuehren).
#   - kopiert scripts/local-llm nach /Users/agents/local-llm (Besitzer agents)
#   - installiert den Paperclip-Wrapper als /Users/agents/bin/claude
#   - legt /Users/agents/work/demo als Uebungs-Repo an (filterProducts v1 + Tests)
# Nutzung: scripts/local-llm/install-agents.sh      (erneut ausfuehren = aktualisieren; demo bleibt)
set -euo pipefail

AGENT_USER="${AGENT_USER:-agents}"
AGENT_HOME="$(dscl . -read "/Users/$AGENT_USER" NFSHomeDirectory | awk '{print $2}')"
SRC="$(cd "$(dirname "$0")" && pwd)"
as_agent() { sudo -u "$AGENT_USER" -H bash -lc "$*"; }

sudo mkdir -p "$AGENT_HOME/local-llm" "$AGENT_HOME/bin" "$AGENT_HOME/work"
sudo rsync -a --delete "$SRC/" "$AGENT_HOME/local-llm/"
sudo install -m 755 "$SRC/paperclip-local-claude.sh" "$AGENT_HOME/bin/claude"
sudo chown -R "$AGENT_USER":staff "$AGENT_HOME/local-llm" "$AGENT_HOME/bin" "$AGENT_HOME/work"

as_agent 'git config --global user.name >/dev/null || git config --global user.name "Klaus & Co Agents"'
as_agent 'git config --global user.email >/dev/null || git config --global user.email "agents@localhost"'

if [[ ! -d "$AGENT_HOME/work/demo/.git" ]]; then
  as_agent 'set -e
    mkdir -p ~/work/demo/src ~/work/demo/test ~/work/demo/.plans && cd ~/work/demo
    git init -q
    printf "node_modules/\n.plans/logs/\n" > .gitignore
    cat > package.json <<JSON
{ "name": "demo", "version": "1.0.0", "private": true, "scripts": { "test": "node --test" } }
JSON
    cat > src/filter.js <<JS
"use strict";
function filterProducts(products, { minPrice, maxPrice, minStock }) {
  return products.filter(p =>
    (minPrice == null || p.price >= minPrice) &&
    (maxPrice == null || p.price <= maxPrice) &&
    (minStock == null || p.inventory >= minStock)
  );
}
module.exports = { filterProducts };
JS
    cat > test/filter.test.js <<JS
const test = require("node:test");
const assert = require("node:assert");
const { filterProducts } = require("../src/filter");
const P = [{ id: 1, price: 5, inventory: 2 }, { id: 2, price: 20, inventory: 0 }];
test("minPrice", () => assert.deepStrictEqual(filterProducts(P, { minPrice: 10 }).map(p => p.id), [2]));
test("minStock", () => assert.deepStrictEqual(filterProducts(P, { minStock: 1 }).map(p => p.id), [1]));
JS
    git add -A && git commit -qm "init: filterProducts v1"'
fi

echo "Fertig:"
echo "  Harness:  $AGENT_HOME/local-llm   (pipeline.sh, execute.sh, critic.sh, accept.sh)"
echo "  Wrapper:  $AGENT_HOME/bin/claude"
echo "  Demo:     $AGENT_HOME/work/demo"
