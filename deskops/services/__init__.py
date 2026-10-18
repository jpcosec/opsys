"""Domain services constructed with a repository ``root``.

Each service owns one domain and uses ``deskops.desk_paths`` and
``deskops.doc_io`` for path and store work. Callers (``DeskopsOperations`` and
the CLI commands) delegate to them instead of implementing the domain inline.
"""
