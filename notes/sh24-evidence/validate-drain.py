#!/usr/bin/env python3
"""Follow-up evidence: preserve old CI reds and require complete fixed runs."""
from pathlib import Path
import re
import statistics
import sys

root = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'logs'
def statuses(name, count):
    data=(root/f'{name}.status').read_text()
    assert data.rstrip().endswith('done'), f'{name} unfinished'
    pairs=re.findall(r'^([a-z][-a-z0-9]*)=(\d+)$',data,re.M)
    assert len(pairs)==count,(name,len(pairs))
    assert all(v=='0' for _,v in pairs),[(k,v) for k,v in pairs if v!='0']
statuses('regress-measure',26)
statuses('drain-verify',22)
statuses('post-drain',17)
for tier in ('native','release'):
    for prefix in ('regress-base','regress-head','drain-fixed'):
        vals=[]
        for i in range(1,7):
            text=(root/f'{prefix}-{tier}-{i}.log').read_text()
            assert 'shape-rss: FAIL' not in text
            vals.append(int(re.search(r'\((-?\d+) B a turn\)',text)[1]))
        print(prefix,tier,vals,'median',statistics.median(vals))
    for suffix in ('','-taskset'):
        text=(root/f'drain-diff-{tier}{suffix}.log').read_text()
        assert re.search(r'difftest: total\s+995\s+0\s+28',text)
        text=(root/f'post-drain-sess-{tier}{suffix}.log').read_text()
        assert 'session: pass 290  fail 0  pending 2' in text
    text=(root/f'post-drain-shape-{tier}.log').read_text()
    assert len(re.findall(r'^shape-rss: ok\s+\S+\s+(?:loop|script|typed|jobs|monitor)\s+\d+',text,re.M))==52
    assert 'shape-rss: FAIL' not in text
print('drain follow-up: paired six readings/tier; fixed six readings/tier; corpus995/0/28 x4; sessions290/0/2 x4; full52 shapes x2; checked and compiled units green')
