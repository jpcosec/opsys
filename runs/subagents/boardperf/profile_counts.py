"""Counts of the calls the board run repeats per task, from a cProfile dump."""
import sys
import pstats

TARGETS = ("open_store", "desk_graph", "build_closeout_graph_context", "load_edge_index", "select_documents", "transition_findings", "doc_status")
for path in sys.argv[1:]:
    stats = pstats.Stats(path)
    print(f"## {path}")
    for target in TARGETS:
        rows = [(key, value) for key, value in stats.stats.items() if key[2] == target]
        print(f"{target}: calls={sum(value[0] for _, value in rows)} cumulative={sum(value[3] for _, value in rows):.3f}s")
