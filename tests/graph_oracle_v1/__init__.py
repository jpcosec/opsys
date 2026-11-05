"""Test oracle: deskops' own graph extractors as they were at 9ced34e5 (wt/board-perf).

The declared-edge graph is now read by sldb (``sldb.api.edges.project_graph``) with the
desk's configuration (``deskops.graph.desk_graph``). These frozen copies of the full-scan
extractors (every document and file extracted, ``doc_status`` asked once per document,
every document's declarations read) are what the tests compare the new path against.
Nothing in ``deskops`` imports them.
"""
