#!/bin/bash
set -u
. /tmp/venv/bin/activate
H=${1:?layout}; RUNS=${2:-3}; LABEL=${3:-run}
export PYTHONPATH=$H/deskops:$H/sldb/src XDG_CACHE_HOME=$H/xdg
cd "$H/deskops"
warm_wipe() { for r in deskops sldb spec2viz pron scion; do rm -rf "$H/$r/.sldb_cache"; done; rm -rf "$XDG_CACHE_HOME"; mkdir -p "$XDG_CACHE_HOME"; }
t() { local s=$(date +%s.%N); "$@" >/tmp/${LABEL}-out.txt 2>/tmp/${LABEL}-err.txt; local rc=$?; local e=$(date +%s.%N); echo "$e - $s" | bc; echo "rc=$rc" >&2; }
median() { sort -n | awk '{a[NR]=$1} END{print a[int((NR+1)/2)]}'; }
build() { for r in spec2viz scion deskops; do (cd "$H/$r" && python -m sldb stores build --store .sldb >>/tmp/${LABEL}-build.log 2>&1); done; }
cold=(); hot=()
for i in $(seq "$RUNS"); do warm_wipe; cold+=("$(t python -m deskops view board --root . 2>/tmp/measure-rc)") ; cat /tmp/measure-rc >&2; done
build >/dev/null
python -m deskops view board --root . >/dev/null 2>&1
for i in $(seq "$RUNS"); do hot+=("$(t python -m deskops view board --root . 2>/tmp/measure-rc)"); cat /tmp/measure-rc >&2; done
echo "$LABEL cold: ${cold[*]} median $(printf '%s\n' "${cold[@]}" | median)"
echo "$LABEL hot: ${hot[*]} median $(printf '%s\n' "${hot[@]}" | median)"
