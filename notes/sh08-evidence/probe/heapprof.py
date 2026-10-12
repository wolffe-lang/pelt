#!/usr/bin/env python3
"""heapprof — lane-local (sh08): where pelt's root arena grows.

The wolf runtime's process root is a bump arena over 64 KiB chunks from
malloc that is never freed (wolf_rt str.rs `ambient_alloc`), and a
region's chunks are pooled once warm. So after warm-up, every malloc of
>= 64 KiB is the root arena growing, and the allocation that overflowed
the chunk is a byte-proportional sample of who allocates in the root.
This runs SHELL on SCRIPT under gdb with a breakpoint on such mallocs,
records the backtrace's pelt frames (`sh.…`, from the DWARF) and the
runtime entry they called, and prints, per innermost
pelt frame chain, the share of chunk grabs.
usage: heapprof.py SHELL SCRIPT [skip]
"""
import collections, re, subprocess, sys, os
shell, script = sys.argv[1], sys.argv[2]
skip = int(sys.argv[3]) if len(sys.argv) > 3 else 20
gdbcmds = f"""set pagination off
set confirm off
set breakpoint pending on
set print frame-arguments none
break malloc if $rdi >= 65536
commands
silent
printf "HIT %d\\n", $rdi
bt 40
continue
end
run {script} > /dev/null
quit
"""
cf = os.path.join(os.environ.get("TMPDIR", "."), f"heapprof.{os.getpid()}.gdb")
open(cf, "w").write(gdbcmds)
r = subprocess.run(["gdb", "-q", "-batch", "-x", cf, shell], capture_output=True, text=True)
os.remove(cf)
hits = []
cur = None
for ln in r.stdout.splitlines():
    if ln.startswith("HIT "):
        cur = []
        hits.append(cur)
    elif cur is not None and ln.startswith("#"):
        m = re.search(r"(?:in |#\d+\s+)(sh\.\w+) \(", ln)
        if m:
            cur.append(m.group(1)[3:])
        elif not cur:
            m = re.search(r"(__wolf_rt_\w+)", ln)
            if m:
                cur.append("[" + m.group(1)[10:] + "]")
hits = hits[skip:]
by_leaf = collections.Counter()
by_chain = collections.Counter()
by_any = collections.Counter()
for h in hits:
    if not h:
        by_leaf["<no wolf frame>"] += 1
        continue
    by_leaf[h[0]] += 1
    by_chain[" < ".join(h[:4])] += 1
    for f in set(h):
        by_any[f] += 1
n = len(hits)
print(f"heapprof: {shell} {script}: {n} chunk grabs after the first {skip} (~{n*64} KiB)")
print("-- innermost wolf frame")
for k, v in by_leaf.most_common(15):
    print(f"{v:6} {100*v/n:5.1f}%  {k}")
print("-- innermost four frames")
for k, v in by_chain.most_common(15):
    print(f"{v:6} {100*v/n:5.1f}%  {k}")
print("-- on the stack at all")
for k, v in by_any.most_common(30):
    print(f"{v:6} {100*v/n:5.1f}%  {k}")
