"""Pin pelt screens, retaining and checking independently measured bash answers."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
import lib_session as ls
oracle = ROOT/'notes/sh28-evidence/oracle-transcripts'
oracle.mkdir(exist_ok=True)
pelt = str(ROOT/'target/native/pelt')
for name, keys in ls.cases(sys.argv[1:] or [p.stem for p in (ROOT/'tests/session').glob('sh28_*.keys')]):
    if name.startswith(('sh28_arg_', 'sh28_bindings_')) or name == 'sh28_kill_ring_cap':
        print('use numeric-regressions.py / extensions.py for', name, flush=True)
        continue
    meta = ls.read_meta(keys[:-5] + '.meta')
    tr = Path(keys[:-5]+'.tr')
    saved = oracle/(name+'.tr')
    if not saved.exists():
        saved.write_text(tr.read_text())
    a = ls.run(ls.argv_for(pelt, meta, True), keys, meta)
    screen = ls.last_screens
    mode = ls.last_mode
    b = ls.run(ls.argv_for(pelt, meta, True), keys, meta)
    if a != b or screen != ls.last_screens or mode is not True or ls.last_mode is not True:
        raise SystemExit('UNSTABLE or MODES ' + name)
    expected = saved.read_text().splitlines()
    if name == 'sh28_mark_exchange':
        # R-sh28-4: C-@ sets mark as the manual specifies; bash's
        # measured NUL non-effect is retained as an observation only.
        if 'out "abcdX\\n"' not in a or a[-1] != 'exit 0 at step 3':
            raise SystemExit('C-@ does not set mark: ' + str(a))
        meta['why'] += '; R-sh28-4: C-@ sets mark per documented intent; bash NUL non-effect retained in oracle-transcripts'
    elif name == 'sh28_quit_status':
        if 'out "status:1:end\\n"' not in a or any('trapped' in line for line in a if line.startswith('out ')):
            raise SystemExit('QUIT changed status or ran a trap: '+str(a))
        meta['why'] += '; R-sh28-5: editor-only quit flush, no signal or trap; bash actual tty QUIT trap output retained in oracle-transcripts'
    elif ls.stdout_and_exit(a) != ls.stdout_and_exit(expected):
        raise SystemExit('BASH DISAGREEMENT ' + name + ': ' + str(ls.stdout_and_exit(a)))
    tr.write_text('\n'.join(a)+'\n')
    meta.update(tr_by='hand', screen='2', screen_by='hand')
    meta['why'] += '; pelt-owned screen and transcript pinned by record-pelt.py, checked against separately retained bash stdout/status'
    ls.write_meta(keys[:-5]+'.meta', meta)
    ls.write_screen(keys[:-5]+'.screen', screen, '2')
    print('pinned', name, flush=True)
