"""lib_session — what an interactive session case is, shared by
tools/session and tools/session-record.

A session case is a set of files in tests/session/:

  <name>.keys   what is typed, one line per line; a line that is exactly
                `^D` types Ctrl-D (the terminal's end-of-file character)
                and `^C` types Ctrl-C (its interrupt character). Every
                other line is typed followed by a newline.
  <name>.tr     the oracle's transcript (below), written by
                tools/session-record from `dash -i +m`
  <name>.meta   key=value lines:
                  args=…        operands after the oracle's `-i +m`
                                and after pelt's `-i` (split on blanks)
                  pelt_args=…   pelt's whole argument list instead, for
                                cases about how pelt decides to be
                                interactive (`pelt_args=` is none at all)
                  env=K=V …     extra environment, split on blanks; a
                                `$HOME` in a value is left for the shell
                  bash=agree|differs  the second opinion (`bash --posix
                                -i`), on standard output and exit status
                  pending=WHAT  needs a primitive pelt lacks; listed by
                                name in tests/session/PENDING.md
                  why=TEXT      free text
  <name>.files/ optional: copied into the case's scratch directory
                before the shell starts (`home/` is `$HOME`, `w/` the
                working directory)

**How a session runs.** The shell's standard input is the slave side
of a fresh pseudo-terminal, which is also its controlling terminal (so
Ctrl-C is a real SIGINT to its process group); standard output and
standard error are two separate pipes. A line is typed only when the
shell is waiting for one: for the oracle that is decided by quiet (no
byte on either pipe for `SETTLE` seconds); for pelt by the oracle's own
prompt appearing at the end of standard error (or quiet, where the
oracle showed no prompt).

**The transcript.** One step per line typed, plus step 0 (what happens
before anything is typed): the bytes on standard output; whether
anything that is not white space reached standard error other than the
prompt (presence only: pelt's messages are its own, CLAUDE.md); and the
prompt the step ended on — the part of standard error after its last
newline. The last line is `exit N` (`signal N` for a death by signal)
with the step it happened at, or `alive` if the shell outlived what was
typed. Lines are typed until the shell exits; any left over are not.
"""

import json
import os
import pty
import select
import shutil
import signal
import subprocess
import tempfile
import termios
import time
import fcntl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESS = os.environ.get("PELT_SESSION_DIR") or os.path.join(ROOT, "tests", "session")
ORACLE = ["dash", "-i", "+m"]
SECOND = ["bash", "--posix", "-i", "+m"]
SETTLE = 0.6       # quiet that means "waiting for input" (oracle runs)
PROMPT_WAIT = 8.0  # how long pelt may take to show the expected prompt
EXIT_WAIT = 8.0


def read_meta(path):
    meta = {}
    if not os.path.exists(path):
        return meta
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            k, _, v = line.partition("=")
            meta[k.strip()] = v
    return meta


def write_meta(path, meta):
    order = ["args", "pelt_args", "env", "bash", "pending", "why"]
    keys = [k for k in order if k in meta] + sorted(
        k for k in meta if k not in order)
    with open(path, "w", encoding="utf-8") as fh:
        for k in keys:
            fh.write(f"{k}={meta[k]}\n")


def cases(names=None):
    """Every case as (name, keys path), sorted."""
    out = []
    for f in sorted(os.listdir(SESS)):
        if f.endswith(".keys"):
            n = f[:-5]
            if names and n not in names:
                continue
            out.append((n, os.path.join(SESS, f)))
    return out


def keystrokes(path):
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh.read().split("\n")[:-1]:
            if line == "^D":
                out.append(("^D", b"\x04"))
            elif line == "^C":
                out.append(("^C", b"\x03"))
            else:
                out.append((line, line.encode() + b"\n"))
    return out


def argv_for(shell, meta, is_pelt):
    if is_pelt:
        if "pelt_args" in meta:
            return [shell] + meta["pelt_args"].split()
        return [shell, "-i"] + meta.get("args", "").split()
    return list(shell) + meta.get("args", "").split()


def _ctty():
    # the pty slave is already descriptor 0; make it this new session's
    # controlling terminal so the interrupt character reaches us
    fcntl.ioctl(0, termios.TIOCSCTTY, 0)
    # and start the shell as a terminal would: SIGINT and SIGQUIT at
    # their defaults, nothing blocked. A harness launched in the
    # background of a non-interactive shell inherits both IGNORED (XCU
    # 2.11), and dash and its children would then never see Ctrl-C:
    # the first recording of ctrl_c_child showed `sleep 5` outliving
    # its ^C for exactly that reason.
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGQUIT, signal.SIG_DFL)
    signal.pthread_sigmask(signal.SIG_SETMASK, [])


# The shell's signal mask and ignored set as /proc showed them, for a
# case that types ^C (linux only; None elsewhere): the evidence that a
# signal row's answer was not decided by an inherited mask.
last_sig = None


def _sig_state(pid):
    try:
        with open(f"/proc/{pid}/status", encoding="utf-8") as fh:
            rows = [ln.split()[1] for ln in fh if ln.startswith(("SigBlk:", "SigIgn:"))]
        return f"SigBlk {rows[0]} SigIgn {rows[1]}"
    except (OSError, IndexError):
        return None


class Step:
    def __init__(self, typed):
        self.typed = typed
        self.out = b""
        self.err = b""


def split_err(err):
    i = err.rfind(b"\n")
    if i < 0:
        return b"", err
    return err[:i + 1], err[i + 1:]


def run(argv, keys_path, meta, expect=None):
    """Run one session. `expect` (a parsed oracle transcript) switches
    from quiet-based to prompt-based pacing. Answers the transcript as
    a list of lines."""
    holder = tempfile.mkdtemp(prefix="pelt-sess.")
    try:
        home = os.path.join(holder, "home")
        work = os.path.join(holder, "w")
        files = keys_path[:-5] + ".files"
        if os.path.isdir(files):
            shutil.copytree(files, holder, dirs_exist_ok=True)
        os.makedirs(home, exist_ok=True)
        os.makedirs(work, exist_ok=True)
        env = {"PATH": "/usr/bin:/bin", "HOME": home, "LC_ALL": "C"}
        for kv in meta.get("env", "").split():
            k, _, v = kv.partition("=")
            env[k] = v
        return _session(argv, keystrokes(keys_path), env, work, expect)
    finally:
        shutil.rmtree(holder, ignore_errors=True)


def _session(argv, keys, env, cwd, expect):
    master, slave = pty.openpty()
    rout, wout = os.pipe()
    rerr, werr = os.pipe()
    p = subprocess.Popen(argv, stdin=slave, stdout=wout, stderr=werr,
                         env=env, cwd=cwd, start_new_session=True,
                         preexec_fn=_ctty, close_fds=True)
    os.close(slave)
    os.close(wout)
    os.close(werr)
    open_fds = {rout: b"out", rerr: b"err", master: b"tty"}
    steps = []

    def pump(step, timeout):
        """Read whatever arrives within `timeout`; True if anything did."""
        got = False
        r, _, _ = select.select([fd for fd in open_fds], [], [], timeout)
        for fd in r:
            try:
                d = os.read(fd, 65536)
            except OSError:
                d = b""
            if not d:
                if fd != master:
                    del open_fds[fd]
                    os.close(fd)
                else:
                    del open_fds[fd]
                continue
            got = True
            if open_fds.get(fd) == b"out":
                step.out += d
            elif open_fds.get(fd) == b"err":
                step.err += d
        return got

    def settle(step, want_prompt):
        """Wait until the shell waits for input, or exits."""
        start = time.time()
        if want_prompt:
            while time.time() - start < PROMPT_WAIT:
                pump(step, 0.05)
                if split_err(step.err)[1] == want_prompt:
                    # a last look for output that raced the prompt
                    while pump(step, 0.05):
                        pass
                    return
                if p.poll() is not None and not (rout in open_fds or rerr in open_fds):
                    return
            return
        quiet_since = time.time()
        while time.time() - start < 30:
            if pump(step, 0.05):
                quiet_since = time.time()
            elif time.time() - quiet_since >= SETTLE:
                return
            if p.poll() is not None and not (rout in open_fds or rerr in open_fds):
                return

    def want(i):
        if expect is None or i >= len(expect["steps"]):
            return None
        return expect["steps"][i]["prompt"].encode() or None

    s0 = Step(None)
    settle(s0, want(0))
    steps.append(s0)
    global last_sig
    last_sig = None
    if any(label == "^C" for label, _ in keys):
        last_sig = _sig_state(p.pid)
    exit_line = None
    for label, data in keys:
        if p.poll() is not None:
            break
        st = Step(label)
        try:
            os.write(master, data)
        except OSError:
            break
        settle(st, want(len(steps)))
        steps.append(st)
    try:
        rc = p.wait(timeout=EXIT_WAIT if expect is not None else 3)
    except subprocess.TimeoutExpired:
        rc = None
    # whatever is still in flight belongs to the last step
    while (rout in open_fds or rerr in open_fds) and rc is not None:
        if not pump(steps[-1], 0.2):
            break
    if rc is None:
        exit_line = "alive"
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except OSError:
            pass
        p.wait()
    elif rc < 0:
        exit_line = f"signal {-rc}"
    else:
        exit_line = f"exit {rc}"
    for fd in list(open_fds):
        os.close(fd)
    return render(steps, exit_line)


def render(steps, exit_line):
    lines = []
    for i, st in enumerate(steps):
        diag, prompt = split_err(st.err)
        typed = "" if st.typed is None else " " + json.dumps(st.typed)
        lines.append(f"step {i}{typed}")
        if st.out:
            lines.append("out " + json.dumps(st.out.decode("utf-8", "replace")))
        lines.append("err " + ("yes" if diag.strip() else "no"))
        lines.append("prompt " + json.dumps(prompt.decode("utf-8", "replace")))
    lines.append(f"{exit_line} at step {len(steps) - 1}")
    return lines


def parse_tr(lines):
    """A transcript's prompts, for pacing pelt."""
    steps = []
    for ln in lines:
        if ln.startswith("step "):
            steps.append({"prompt": ""})
        elif ln.startswith("prompt "):
            steps[-1]["prompt"] = json.loads(ln[7:])
    return {"steps": steps}


def stdout_and_exit(lines):
    """The second opinion's view: standard output per step and the exit."""
    return [ln for ln in lines if ln.startswith(("step ", "out ", "exit ", "signal ", "alive"))]
