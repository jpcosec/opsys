"""Package context stays portable without changing local workflow selectors.

Source atom: atom-board-context-uses-portable-document-names.
"""
from pathlib import Path
import shutil

from sldb.api import (
    add_model, edges_from, init_store, link_store, track_document_file,
    unresolved_references,
)
from sldb.api.graph.snapshot import GraphSnapshot

from deskops.cli.main import main
from deskops.graph.snapshot import build_graph_snapshot
from deskops.operations import DeskopsOperations
from deskops.services.retire import _pill_reference_matches

ROOT = Path(__file__).resolve().parents[1]
PILLS = [
    'pill-001-task-closure-commit',
    'pill-005-subagent-execution',
    'pill-007-phase-gated-task-flow',
    'pill-durable-pill-knowledge-graduates-to-atoms-at-closeout',
    'pill-phase-closeout-reconciles-pills-and-surfaces-next-work',
    'pill-ready-phases-prove-dependencies-and-non-overlap',
    'pill-board-routed-pills-stay-minimal-and-reusable',
]
RITUALS = ['ritual-phase', 'ritual-execution', 'ritual-closeout', 'ritual-testing']
CONTEXT = [
    ('PillDoc', name, f'desk/contexts/{name}.md') for name in PILLS
] + [
    ('RitualDoc', name, f'desk/rituals/{name.removeprefix("ritual-")}.md')
    for name in RITUALS
]


def copy_context(root):
    for _, _, relative in CONTEXT + [('BoardDoc', 'Board', 'desk/tasks/Board.md')]:
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, destination)


def test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions(tmp_path):
    provider = tmp_path / 'provider'
    consumer = tmp_path / 'consumer'
    for root in (provider, consumer):
        copy_context(root)
        store = init_store(root).store_path
        for model in ('BoardDoc', 'PillDoc', 'RitualDoc'):
            add_model(store, f'deskops.models:{model}', pythonpath=str(ROOT))
        for model, name, relative in CONTEXT:
            # Consumer has identical paths but deliberately distinct tracked identities.
            track_document_file(store, model, root / relative,
                                name=name if root == provider else f'consumer-{name}',
                                pythonpath=str(ROOT))
    track_document_file(provider / '.sldb', 'BoardDoc', provider / 'desk/tasks/Board.md',
                        name='Board', pythonpath=str(ROOT))
    link_store(consumer / '.sldb', provider / '.sldb', 'provider')
    unresolved = unresolved_references(consumer / '.sldb')
    assert not [ref for ref in unresolved if ref.source == 'provider:BoardDoc:Board'
                and ref.field in {'pills', 'rituals'}]
    edges = edges_from(consumer / '.sldb', 'provider:BoardDoc:Board', relation='contains')
    assert {edge.target for edge in edges} == {
        f'sldb://document/provider:{model}:{name}' for model, name, _ in CONTEXT
    }
    assert len(edges) == 11


def test_local_graph_next_show_and_retirement_accept_portable_context(tmp_path, capsys):
    copy_context(tmp_path)
    assert not (tmp_path / '.sldb').exists()
    graph = GraphSnapshot.model_validate(build_graph_snapshot(tmp_path))
    nodes = {node.identity.node_id: node for node in graph.nodes}
    board = nodes['board:board-001']
    context_paths = {relative for _, _, relative in CONTEXT}
    contained_paths = {
        nodes[edge.target_id].semantics.path for edge in board.edges
        if edge.relation_type in {'pills', 'rituals'} and edge.target_id in nodes
    }
    assert context_paths <= contained_paths
    assert main(['add', 'task', '--root', str(tmp_path), '--title', 'Portable context',
                 '--goal', 'Check selectors', '--scope', 'Disposable fixture']) == 0
    report = DeskopsOperations(tmp_path).next_action_report('task-portable-context')
    assert report['pills'] == PILLS
    for pill in PILLS:
        assert main(['show', 'pill', pill, '--root', str(tmp_path)]) == 0
        assert _pill_reference_matches(pill, f'desk/contexts/{pill}.md', pill)
    capsys.readouterr()
