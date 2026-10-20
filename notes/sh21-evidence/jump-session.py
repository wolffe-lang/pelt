#!/usr/bin/env python3
"""sh21: the contract's session, typed on a PTY: `lope init pelt` sourced from
pelt's ENV file, then the bare word `projects` lands in the directory and
`g -` goes back. Uses lope 5ac37df's own tools/hook-sessions (its Session
class and where(), loaded from the lope tree, not copied) with a scratch
HOME, XDG_* and PATH, as that tool builds them.

usage: jump-session.py LOPE_TREE LOPE_BIN PELT [PELT...]   (one row block a pelt)
"""
import importlib.machinery
import importlib.util
import os
import shutil
import sys
import tempfile

tree, lope = sys.argv[1], os.path.abspath(sys.argv[2])
loader = importlib.machinery.SourceFileLoader("hs", os.path.join(tree, "tools", "hook-sessions"))
spec = importlib.util.spec_from_loader("hs", loader)
hs = importlib.util.module_from_spec(spec)
loader.exec_module(hs)

for pelt in sys.argv[3:]:
    pelt = os.path.abspath(pelt)
    root = os.path.realpath(tempfile.mkdtemp(prefix="sh21-jump-"))
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
    log = open(os.path.join(os.environ.get("JUMP_LOGS", root), "jump-%s.log" % os.path.basename(os.path.dirname(pelt))), "wb")
    s = hs.Session([pelt, "-i"], env, home, log)
    rows = []
    try:
        s.wait_prompt(30)
        for d in ("projects", "alpha", "beta"):
            s.line("cd %s/%s" % (t, d))
        s.line("cd %s" % home)
        rows.append(("start", hs.where(s, root, "pelt")[0]))
        s.line("projects")
        rows.append(("projects", "%s status %s" % hs.where(s, root, "pelt")))
        s.line("g -")
        rows.append(("g -", "%s status %s" % hs.where(s, root, "pelt")))
        s.line("cd %s" % t)
        s.line("alpha")
        rows.append(("alpha (in t)", hs.where(s, root, "pelt")[0]))
        out = s.line("zzqqxx")
        rows.append(("zzqqxx", "status %s%s" % (hs.status(s, "pelt"), ", said not found" if "not found" in out else ", SILENT")))
    except TimeoutError as e:
        rows.append(("ERROR", str(e)[:200]))
    finally:
        s.close()
        log.close()
        shutil.rmtree(root, ignore_errors=True)
    print("pelt %s" % pelt)
    for step, ans in rows:
        print("  %-14s %s" % (step, ans))
