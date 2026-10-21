#!/usr/bin/env python3
"""sh23: lope's hook beside `set -o autocd`, typed on a PTY: `lope init
pelt` sourced from pelt's ENV file (lope 5ac37df's `shell/pelt/*.sh`: its
`cd` function records a visit, its `command_not_found_handle` jumps), then
paths jump by the option and a fuzzy word still jumps by the hook. Uses
lope's own tools/hook-sessions (its Session class, rc_for and where(),
loaded from the lope tree, not copied) with a scratch HOME, XDG_* and PATH
as that tool builds them (sh21's jump-session.py, the option added).

usage: autocd-jump.py LOPE_TREE LOPE_BIN on|off PELT [PELT...]
  on: `set -o autocd` is typed after the rc; off: it is not (the default)
"""
import importlib.machinery
import importlib.util
import os
import shutil
import sys
import tempfile

tree, lope, mode = sys.argv[1], os.path.abspath(sys.argv[2]), sys.argv[3]
loader = importlib.machinery.SourceFileLoader("hs", os.path.join(tree, "tools", "hook-sessions"))
spec = importlib.util.spec_from_loader("hs", loader)
hs = importlib.util.module_from_spec(spec)
loader.exec_module(hs)

for pelt in sys.argv[4:]:
    pelt = os.path.abspath(pelt)
    root = os.path.realpath(tempfile.mkdtemp(prefix="sh23-jump-"))
    home, cfg, t, bin_ = (os.path.join(root, d) for d in ("home", "home/.config", "t", "bin"))
    for d in ("projects/myapp", "alpha", "beta"):
        os.makedirs(os.path.join(t, d))
    os.makedirs(cfg)
    os.makedirs(bin_)
    os.symlink(lope, os.path.join(bin_, "lope"))
    for exe in ("ls", "cat", "env", "true", "false", "head", "sed"):
        p = shutil.which(exe)
        if p:
            os.symlink(p, os.path.join(bin_, exe))
    hs.rc_for("pelt", "lope", home, cfg)
    env = {"HOME": home, "XDG_DATA_HOME": os.path.join(root, "data"), "XDG_CONFIG_HOME": cfg,
           "XDG_CACHE_HOME": os.path.join(root, "cache"), "XDG_STATE_HOME": os.path.join(root, "state"),
           "XDG_RUNTIME_DIR": os.path.join(root, "run"), "ENV": os.path.join(home, ".shrc"),
           "PATH": bin_, "TERM": "xterm", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "SHELL": pelt,
           "TMPDIR": os.path.join(root, "tmp")}
    os.makedirs(env["TMPDIR"])
    os.makedirs(env["XDG_RUNTIME_DIR"], mode=0o700)
    tag = os.path.basename(os.path.dirname(pelt))
    log = open(os.path.join(os.environ.get("JUMP_LOGS", root), "jump-%s-%s.log" % (tag, mode)), "wb")
    s = hs.Session([pelt, "-i"], env, home, log)
    rows = []

    def at(label, cmd):
        out = s.line(cmd)
        d, st = hs.where(s, root, "pelt")
        said = ", said %s" % ("not found" if "not found" in out else "cannot be run") \
            if ("not found" in out or "cannot be run" in out) else ""
        rows.append((label, "%s status %s%s" % (d, st, said)))

    try:
        s.wait_prompt(30)
        for d in ("projects", "alpha", "beta"):
            s.line("cd %s/%s" % (t, d))
        s.line("cd %s" % root)
        if mode == "on":
            out = s.line("set -o autocd")
            rows.append(("set -o autocd", "refused" if "no such option" in out else "ok"))
        at("t/alpha", "t/alpha")
        at("ROOT/t/projects/", "%s/t/projects/" % root)
        at("..", "..")
        at("beta (in t)", "beta")
        s.line("cd %s" % home)
        at("proj (fuzzy)", "proj")
        s.line("cd %s" % root)
        at("t/projects/myapp", "t/projects/myapp")
        s.line("cd %s" % home)
        at("myapp (fuzzy)", "myapp")
        at("zzqqxx", "zzqqxx")
    except TimeoutError as e:
        rows.append(("ERROR", str(e)[:200]))
    finally:
        s.close()
        log.close()
        shutil.rmtree(root, ignore_errors=True)
    print("pelt %s (%s), option %s" % (pelt, tag, mode))
    for step, ans in rows:
        print("  %-18s %s" % (step, ans))
