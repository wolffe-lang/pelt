"""Record bash keys with pelt's existing typed-session harness, twice."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import lib_session as ls
for name, keys in ls.cases(sys.argv[1:] or [p.stem for p in (ROOT/'tests/session').glob('sh28_*.keys')]):
    meta = ls.read_meta(keys[:-5] + '.meta')
    a = ls.run(ls.argv_for(ls.SECOND, meta, False), keys, meta)
    b = ls.run(ls.argv_for(ls.SECOND, meta, False), keys, meta)
    if ls.stdout_and_exit(a) != ls.stdout_and_exit(b):
        raise SystemExit('UNSTABLE ' + name)
    Path(keys[:-5] + '.tr').write_text('\n'.join(a) + '\n')
    print(name, ls.stdout_and_exit(a), flush=True)
