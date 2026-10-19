#!/usr/bin/env bash
# Knowledge-integrity checks for a desk, run by CI after pytest.
# usage: scripts/ci-knowledge-check.sh [root]
#
# doctor, the sldb store check and graph missing gate: the first non-zero exit
# fails the script. drift check is reported but does not gate, because its
# findings are review items, not integrity failures.
set -u

root="${1:-.}"

gate() {
  echo "== $*"
  "$@" || { echo "FAILED: $*" >&2; exit 1; }
}

gate python -m deskops doctor --root "$root"
gate python -m sldb stores check --store "$root/.sldb"
gate python -m deskops graph missing --root "$root"

agents_out="$(mktemp -d)"
trap 'rm -rf "$agents_out"' EXIT
echo "== python -m deskops drift check --root $root (advisory)"
python -m deskops drift check --root "$root" --out "$agents_out" \
  || echo "drift check reported findings; review them, they do not fail CI"
