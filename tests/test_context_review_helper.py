import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

P = Path(__file__).resolve().parents[1] / 'desk/drawer/plans/workspace-documental'
spec = importlib.util.spec_from_file_location('context_review', P / 'context_review.py')
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)

FULL = {k: 'x' for k in cr.RECEIPT_FIELDS} | {'technical_failure': False, 'stdin': 'devnull'}


class FakePopen:
    calls = []

    def __init__(self, argv, **kw):
        FakePopen.calls.append(argv)
        self.pid, self.returncode = 42, 0

    def communicate(self, timeout=None):
        return 'respuesta', ''


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setattr(cr, 'ROOT', tmp_path)
    monkeypatch.setattr(cr, 'RUN', tmp_path / 'run')
    monkeypatch.setattr(cr.subprocess, 'Popen', FakePopen)
    monkeypatch.setattr(cr.subprocess, 'run', lambda *a, **k: subprocess.CompletedProcess(a, 0, 'pi 9\n', ''))
    FakePopen.calls = []
    d = yaml.safe_load((P / 'dag.yaml').read_text())
    node = d['tasks'][0]
    sha = cr.sha(cr.bundle(d, node)[0])
    return d, node, sha


def put(sha, node, n, receipt):
    a = cr.RUN / node['id'] / sha / f'attempt-{n}'
    a.mkdir(parents=True)
    (a / 'receipt.json').write_text(json.dumps(receipt))
    return a


def test_incomplete_receipt_does_not_raise_nor_answer(env):
    d, node, sha = env
    put(sha, node, 1, {k: v for k, v in FULL.items() if k != 'technical_failure'})
    assert cr.attempts(node['id'], sha) == (0, None)
    state, missing = cr.receipt_state({'argv': []})
    assert state == 'incomplete' and 'technical_failure' in missing
    assert cr.receipt_state(FULL | {'technical_failure': True})[0] == 'technical_failure'
    assert cr.receipt_state({'technical_failure': True, 'argv': []}) == (
        'technical_failure', [k for k in cr.RECEIPT_FIELDS if k not in ('technical_failure', 'argv')])
    assert cr.receipt_state(FULL) == ('complete', [])


def test_incomplete_receipt_creates_new_attempt(env):
    d, node, sha = env
    put(sha, node, 1, {'argv': []})
    assert cr.review(d, node)['attempt'].endswith('attempt-2')


def test_answered_reused_without_process(env):
    d, node, sha = env
    a = put(sha, node, 1, FULL)
    assert cr.attempts(node['id'], sha) == (0, a)
    assert cr.review(d, node)['ok'] and FakePopen.calls == []


def test_new_attempt_manifest_and_receipt(env):
    d, node, sha = env
    put(sha, node, 1, FULL)
    r = cr.review(d, node, 'rechazo semantico')
    assert r['attempt'].endswith('attempt-2') and len(FakePopen.calls) == 1
    out = cr.ROOT / r['attempt']
    m, rc = (json.loads((out / f).read_text()) for f in ('manifest.json', 'receipt.json'))
    assert m['attempt'] == 2 and m['argv'] == rc['argv'] == FakePopen.calls[0]
    assert m['instruction_version'] == cr.INSTRUCTION_VERSION
    assert m['system_prompt_sha256'] == cr.sha(cr.SYSTEM.encode())
    assert m['retry_reason'] == rc['retry_reason'] == 'rechazo semantico'
    assert m['retry_of'] == rc['retry_of'] == str(Path('run') / node['id'] / sha / 'attempt-1')
    assert cr.receipt_state(rc)[0] == 'complete'


@pytest.mark.parametrize('extra', [['--new-attempt', 'WS01'], ['--new-attempt', 'WS01', '--reason', ' '],
                                   ['--new-attempt', '--reason', 'x'], ['--new-attempt', '--reason', 'x', '--stale'],
                                   ['WS01', '--reason', 'x']])
def test_new_attempt_argument_errors(env, monkeypatch, extra):
    monkeypatch.setattr(sys, 'argv', ['context_review.py', 'run', *extra])
    with pytest.raises(SystemExit) as e:
        cr.main()
    assert e.value.code == 2 and FakePopen.calls == [] and not cr.RUN.exists()


def test_stale_reviews_reports_receipt_incomplete(env, monkeypatch):
    d, node, sha = env
    for n, rec in ((1, {'argv': []}), (2, FULL), (3, FULL | {'technical_failure': True})):
        a = put(sha + str(n), node, 1, rec)
        (a / 'disposition.md').write_text('ok')
        node['context_review'] = {'status': 'done', 'input_sha256': sha, 'contract_sha256': cr.sha(cr.canonical(node).encode()),
                                  'evidence': [str(a.relative_to(cr.ROOT))]}
        monkeypatch.setattr(cr, 'all_nodes', lambda d: [node])
        assert cr.stale_reviews(d) == {1: [f'{node["id"]}: receipt incomplete'], 2: [],
                                       3: [f'{node["id"]}: receipt technical failure']}[n]


def test_system_clause_and_bundle_independent_of_system(env, monkeypatch):
    d, node, sha = env
    assert 'agregado o paquete no ejecutable' in cr.SYSTEM and 'hijos' in cr.SYSTEM
    monkeypatch.setattr(cr, 'SYSTEM', 'otro')
    assert cr.sha(cr.bundle(d, node)[0]) == sha


ROOT_CLAUSE = ('Para ROOT/PK, reformula el RESULTADO SUSTANTIVO del paquete y da DRY-RUN HIPOTETICO de ejecucion de hijos en '
               'orden, entradas/salidas entre ellos e integracion/validacion. No describas solo como revisar '
               'hashes/status/disposition: eso es gate de comprension, no el trabajo del paquete. No ejecutes nada. ')


def test_file_instruccion_text_is_fixed(env):
    d, node, _ = env
    tail = 'Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.\n\n'
    for n, clause in ((node, ''), (d['hierarchy']['root'], ROOT_CLAUSE), (d['hierarchy']['packages'][0], ROOT_CLAUSE)):
        text = cr.bundle(d, n)[0].decode().split('FILE:instruccion\n')[1]
        assert text == f'Revisa el nodo {n["id"]} siguiendo context-review-guide.md. ' + clause + tail


def test_forced_run_marks_every_attempt(env, monkeypatch):
    d, node, sha = env
    put(sha, node, 1, FULL)
    outs = iter([('', ''), ('respuesta', '')])
    monkeypatch.setattr(FakePopen, 'communicate', lambda self, timeout=None: next(outs))
    r = cr.review(d, node, 'otra vez')
    assert r['ok'] and r['attempt'].endswith('attempt-3')
    base = Path('run') / node['id'] / sha
    for n in (2, 3):
        m = json.loads((cr.ROOT / base / f'attempt-{n}/manifest.json').read_text())
        rc = json.loads((cr.ROOT / base / f'attempt-{n}/receipt.json').read_text())
        assert m['retry_reason'] == rc['retry_reason'] == 'otra vez'
        assert m['retry_of'] == rc['retry_of'] == str(base / f'attempt-{n - 1}')
    assert json.loads((cr.ROOT / base / 'attempt-2/receipt.json').read_text())['technical_failure'] is True
