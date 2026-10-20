"""lib_session — what an interactive session case is, shared by
tools/session and tools/session-record.

A session case is a set of files in tests/session/:

  <name>.keys   what is typed, one line per line; a line that is exactly
                `^D` types Ctrl-D (the terminal's end-of-file character)
                and `^C` types Ctrl-C (its interrupt character); `^Z`
                types Ctrl-Z (its suspend character). A line that
                starts with a backslash, `k` and a space types the rest
                as raw keys with no newline after them: backslash-e is
                ESC, backslash-xNN a byte, and backslash-r, -n, -t and
                a doubled backslash as in C (an arrow key is ESC `[D`).
                A line `\\size COLS ROWS` types nothing: it resizes the
                terminal (`TIOCSWINSZ`, so the kernel sends `SIGWINCH`
                to its foreground group) and the screen with it (sh15).
                Every other line is typed followed by a newline.
  <name>.tr     the oracle's transcript (below), written by
                tools/session-record from `dash -i +m`
  <name>.meta   key=value lines:
                  args=…        operands after the oracle's `-i +m`
                                and after pelt's `-i` (split on blanks)
                  pelt_args=…   pelt's whole argument list instead, for
                                cases about how pelt decides to be
                                interactive (`pelt_args=` is none at all)
                  oracle_args=… the oracle's whole argument list after
                                its name, instead of `-i +m` and `args`:
                                for such a case the oracle must decide
                                for itself too (`oracle_args=+m`)
                  env=K=V …     extra environment, split on blanks; a
                                `$HOME` in a value is left for the shell,
                                and `\\s` in a value is a space
                                (`PS1=$\\s`: bash's first prompt is then
                                pelt's, so a bash-recorded case paces
                                pelt from its first step)
                  bash=agree|differs  the second opinion (`bash --posix
                                -i`), on standard output and exit status
                  oracle=bash   the transcript is `bash --posix -i`'s:
                                for behaviour dash does not have (the
                                line editor's keys) or where POSIX and
                                dash part; `dash=agree|differs` is then
                                the second opinion
                  compare=stdout  compare standard output per step and
                                the exit only, not the prompt or the
                                presence of diagnostics: for a case
                                whose oracle draws its own line (an
                                editor echoes through standard error)
                  pending=WHAT  needs a primitive pelt lacks; listed by
                                name in tests/session/PENDING.md
                  why=TEXT      free text
                  tr_by=hand    the transcript was written by hand,
                                where pelt chose otherwise than both
                                oracles (said in `why=`):
                                tools/session-record leaves it alone
                  screen=N[-M]  judge the screen of steps N through M
                                (or N to the end) against
                                <name>.screen (below)
                  cols=N rows=N the terminal's size (80 by 24): the
                                pty's window size, which bash reads,
                                and the screen's, whose cursor report
                                pelt reads
  <name>.screen the oracle's screen at the end of each step from
                `screen=` on, written by tools/session-record (or by
                hand, said so in `why=`): the rows the step drew, from
                the row its first byte landed on, as `| text` lines,
                then `cursor ROW COL` relative to that row
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

**The screen.** Beside the transcript a small terminal (`Screen`,
ECMA-48's controls and the CSI sequences an editor uses, auto-wrap with
xterm's pending-wrap rule, wide characters by Unicode's East Asian
Width) is fed what a real terminal would show of the line being edited:
the pty's own output and standard error, in the order they arrive (the
pty's first when both are ready; standard output, the commands' output,
is left out so the order cannot race). It answers a cursor-position
report (`ESC[6n`) on the pty, as a terminal does. `last_screens` holds
one snapshot per step.

**The mode.** `last_mode` is whether the pty's modes (ICANON, ECHO,
ISIG, IEXTEN, and IXON since sh15, when the editor turns the last two
off) were what they were before the shell started when it ended (None
when it was killed): a shell that leaves its terminal raw fails.

**A resize** (`\\size`) changes the window as an emulator does and the
screen keeps its rows, cut at the new margin or widened with blanks
(xterm's way: no reflow); the cursor keeps its row and is held inside
the new margin.
"""

import codecs
import struct
import unicodedata

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
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_reap as lr  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESS = os.environ.get("PELT_SESSION_DIR") or os.path.join(ROOT, "tests", "session")
ORACLE = ["dash", "-i", "+m"]
SECOND = ["bash", "--posix", "-i", "+m"]
SETTLE = 0.6       # quiet that means "waiting for input" (oracle runs)
PROMPT_WAIT = 8.0  # how long pelt may take to show the expected prompt
EXIT_WAIT = 8.0
# $PELT_SESSION_SLOW=seconds types every byte on its own with that gap
# (0.02 is about a 500-baud line); the transcripts must not change.
SLOW = float(os.environ.get("PELT_SESSION_SLOW") or 0)


class Screen:
    """A terminal small enough to read: COLS by ROWS cells over a grid
    that only grows (the rows above the window are kept), a cursor, and
    xterm's pending wrap. `reply` collects what the terminal answers."""

    def __init__(self, cols=80, rows=24):
        self.cols, self.rows = cols, rows
        self.grid = [[" "] * cols for _ in range(rows)]
        self.top = 0
        self.r = 0
        self.c = 0
        self.pend = False
        self.saved = (0, 0, False)
        self.dec = codecs.getincrementaldecoder("utf-8")("replace")
        self.state = 0
        self.seq = ""
        self.reply = b""

    @staticmethod
    def width(ch):
        cp = ord(ch)
        if 0x1160 <= cp <= 0x11FF or 0xD7B0 <= cp <= 0xD7FF:
            return 0
        cat = unicodedata.category(ch)
        if cat in ("Mn", "Me") or (cat == "Cf" and cp != 0xAD):
            return 0
        if unicodedata.east_asian_width(ch) in ("W", "F") or 0x20000 <= cp <= 0x3FFFD:
            return 2
        return 1

    def resize(self, cols, rows):
        """The window changes size: rows are kept (no reflow), cut at
        the new margin or widened; the cursor stays inside it."""
        for i, row in enumerate(self.grid):
            if len(row) > cols:
                # a wide character cut in half leaves a blank
                cut = row[:cols]
                if cut and cut[-1] != "" and self.width(cut[-1][0]) == 2:
                    cut[-1] = " "
                self.grid[i] = cut
            else:
                self.grid[i] = row + [" "] * (cols - len(row))
        self.cols = cols
        while len(self.grid) < self.top + rows:
            self.grid.append([" "] * cols)
        self.rows = rows
        if self.r > self.top + rows - 1:
            self.top = self.r - rows + 1
        self.c = min(self.c, cols - 1)
        self.pend = False

    def _row(self, r):
        while r >= len(self.grid):
            self.grid.append([" "] * self.cols)
        return self.grid[r]

    def _lf(self):
        self.pend = False
        if self.r == self.top + self.rows - 1:
            self.top += 1
            self._row(self.top + self.rows - 1)
        self.r += 1
        self._row(self.r)

    def _put(self, ch):
        w = self.width(ch)
        if w == 0:
            row = self._row(self.r)
            col = self.c if self.pend else self.c - 1
            while col > 0 and row[col] == "":
                col -= 1
            if col >= 0:
                row[col] += ch
            return
        if self.pend or (w == 2 and self.c == self.cols - 1):
            self.c = 0
            self._lf()
        row = self._row(self.r)
        row[self.c] = ch
        if w == 2:
            row[self.c + 1] = ""
        self.c += w
        if self.c >= self.cols:
            self.c = self.cols - 1
            self.pend = True

    def _csi(self, seq):
        final = seq[-1]
        body = seq[:-1]
        nums = [int(x) if x.isdigit() else 0 for x in body.split(";")] if body else []
        n = nums[0] if nums and nums[0] > 0 else 1
        self.pend = False
        if final == "A":
            self.r = max(self.top, self.r - n)
        elif final == "B":
            self.r = min(self.top + self.rows - 1, self.r + n)
        elif final == "C":
            self.c = min(self.cols - 1, self.c + n)
        elif final == "D":
            self.c = max(0, self.c - n)
        elif final in "Hf":
            row = nums[0] if nums and nums[0] > 0 else 1
            col = nums[1] if len(nums) > 1 and nums[1] > 0 else 1
            self.r = self.top + min(row, self.rows) - 1
            self.c = min(col, self.cols) - 1
        elif final == "J":
            mode = nums[0] if nums else 0
            if mode == 2:
                for r in range(self.top, self.top + self.rows):
                    self._row(r)[:] = [" "] * self.cols
            else:
                row = self._row(self.r)
                row[self.c:] = [" "] * (self.cols - self.c)
                for r in range(self.r + 1, len(self.grid)):
                    self.grid[r] = [" "] * self.cols
        elif final == "K":
            row = self._row(self.r)
            row[self.c:] = [" "] * (self.cols - self.c)
        elif final == "P":
            # delete characters: the rest of the row moves left
            row = self._row(self.r)
            n = min(n, self.cols - self.c)
            row[self.c:] = row[self.c + n:] + [" "] * n
        elif final == "@":
            # insert blanks: the rest of the row moves right
            row = self._row(self.r)
            n = min(n, self.cols - self.c)
            row[self.c:] = ([" "] * n + row[self.c:])[:self.cols - self.c]
        elif final == "X":
            row = self._row(self.r)
            n = min(n, self.cols - self.c)
            row[self.c:self.c + n] = [" "] * n
        elif final == "n" and body == "6":
            self.reply += f"\x1b[{self.r - self.top + 1};{self.c + 1}R".encode()

    def feed(self, data):
        for ch in self.dec.decode(data):
            o = ord(ch)
            if self.state == 1:
                if ch == "[":
                    self.state, self.seq = 2, ""
                elif ch == "]":
                    self.state = 3
                elif ch == "7":
                    self.saved = (self.r, self.c, self.pend)
                    self.state = 0
                elif ch == "8":
                    self.r, self.c, self.pend = self.saved
                    self.state = 0
                else:
                    self.state = 0
                continue
            if self.state == 2:
                self.seq += ch
                if 0x40 <= o <= 0x7E:
                    self._csi(self.seq)
                    self.state = 0
                continue
            if self.state == 3:
                if o == 7 or o == 0x9C:
                    self.state = 0
                elif o == 27:
                    self.state = 4
                continue
            if self.state == 4:
                self.state = 0
                continue
            if o == 27:
                self.state = 1
            elif o == 13:
                self.c, self.pend = 0, False
            elif o == 10:
                self._lf()
            elif o == 8:
                self.pend = False
                if self.c > 0:
                    self.c -= 1
            elif o == 9:
                self.pend = False
                self.c = min(self.cols - 1, (self.c // 8 + 1) * 8)
            elif o < 32 or o == 127:
                pass
            else:
                self._put(ch)

    def snapshot(self, start):
        """The rows from `start` (absolute) down, and the cursor."""
        last = self.r
        for r in range(len(self.grid) - 1, start - 1, -1):
            if "".join(self.grid[r]).strip():
                last = max(last, r)
                break
        rows = ["| " + "".join(self.grid[r]).rstrip() for r in range(start, last + 1)]
        return rows + [f"cursor {self.r - start} {self.c}"]


def read_screen(path):
    """A .screen file as {step: [lines]}."""
    out = {}
    cur = None
    with open(path, encoding="utf-8") as fh:
        for ln in fh.read().split("\n"):
            if ln.startswith("step "):
                cur = int(ln[5:])
                out[cur] = []
            elif cur is not None and ln:
                out[cur].append(ln)
    return out


def screen_steps(spec, n):
    """The steps a `screen=N[-M]` judges, of `n`."""
    a, _, b = spec.partition("-")
    last = int(b) if b else n - 1
    return list(range(int(a), min(last, n - 1) + 1))


def write_screen(path, screens, spec):
    with open(path, "w", encoding="utf-8") as fh:
        for i, rows in enumerate(screens):
            if i not in screen_steps(spec, len(screens)):
                continue
            fh.write(f"step {i}\n")
            for ln in rows:
                fh.write(ln + "\n")


_LMODES = termios.ICANON | termios.ECHO | termios.ISIG | termios.IEXTEN
_IMODES = termios.IXON


def _lmode(fd):
    """The modes a shell must give back: the local ones and IXON, as
    one number (the input flag shifted above the local ones)."""
    try:
        a = termios.tcgetattr(fd)
    except (termios.error, OSError):
        return None
    return (a[3] & _LMODES) | ((a[0] & _IMODES) << 32)


def flags_of(mode):
    """`_lmode`'s number as words, for a log."""
    if mode is None:
        return "unreadable"
    names = [("icanon", termios.ICANON), ("echo", termios.ECHO), ("isig", termios.ISIG),
             ("iexten", termios.IEXTEN)]
    out = [("" if mode & bit else "-") + n for n, bit in names]
    out.append(("" if (mode >> 32) & termios.IXON else "-") + "ixon")
    return " ".join(out)


def term_lmode(master, hold):
    """The terminal's local modes after the shell may have gone: through
    the master, which answers for the pair on linux and macOS alike (on
    macOS the slave is revoked when its session leader exits, and
    tcgetattr on it is ENOTTY); through the slave if the master cannot."""
    m = _lmode(master)
    return m if m is not None else _lmode(hold)


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
    order = ["args", "pelt_args", "oracle_args", "env", "oracle", "compare",
             "bash", "dash", "pending", "tr_by", "why"]
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
            elif line == "^Z":
                out.append(("^Z", b"\x1a"))
            elif line.startswith("\\k "):
                out.append((line, _raw_keys(line[3:])))
            elif line.startswith("\\size "):
                out.append((line, None))
            else:
                out.append((line, line.encode() + b"\n"))
    return out


def _raw_keys(text):
    out = bytearray()
    i = 0
    simple = {"e": 0x1b, "r": 0x0d, "n": 0x0a, "t": 0x09, "\\": 0x5c}
    while i < len(text):
        c = text[i]
        if c == "\\" and i + 1 < len(text):
            n = text[i + 1]
            if n in simple:
                out.append(simple[n])
                i += 2
                continue
            if n == "x" and i + 3 < len(text):
                out.append(int(text[i + 2:i + 4], 16))
                i += 4
                continue
        out += c.encode()
        i += 1
    return bytes(out)


def argv_for(shell, meta, is_pelt):
    if is_pelt:
        # pelt is given the oracle's job-control flag: `+m` unless the
        # case runs the oracle with `-m` (sh18: an interactive pelt has
        # job control on by default, as dash does)
        if "pelt_args" in meta:
            args = meta["pelt_args"].split()
            if args and "-m" not in args and "+m" not in args:
                args = ["+m"] + args
            return [shell] + args
        return [shell, "-i", "+m"] + meta.get("args", "").split()
    if "oracle_args" in meta:
        return [a for a in shell if a not in ("-i", "+m")] + meta["oracle_args"].split()
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
    # Every signal, since sh14: a shell leaves alone whichever it was
    # started ignoring, and the sessions trap and send others too.
    for n in range(1, signal.NSIG):
        if n in (signal.SIGKILL, signal.SIGSTOP):
            continue
        try:
            signal.signal(n, signal.SIG_DFL)
        except (OSError, ValueError):
            pass
    signal.pthread_sigmask(signal.SIG_SETMASK, [])


last_screens = []
last_mode = None

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


def shown_tail(b):
    """What a terminal shows of the text after the last line break:
    escape sequences dropped, and only what follows the last CR."""
    out = bytearray()
    i = 0
    while i < len(b):
        if b[i] == 27 and i + 1 < len(b) and b[i + 1] == 0x5B:
            j = i + 2
            while j < len(b) and not (0x40 <= b[j] <= 0x7E):
                j += 1
            i = j + 1
            continue
        if b[i] == 13:
            out = bytearray()
        else:
            out.append(b[i])
        i += 1
    return bytes(out)


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
            env[k] = v.replace("\\s", " ")
        return _session(argv, keystrokes(keys_path), env, work, expect, meta)
    finally:
        shutil.rmtree(holder, ignore_errors=True)


def _session(argv, keys, env, cwd, expect, meta=None):
    meta = meta or {}
    lr.subreaper()
    before = lr.children()
    cols = int(meta.get("cols") or 80)
    nrows = int(meta.get("rows") or 24)
    master, slave = pty.openpty()
    fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", nrows, cols, 0, 0))
    mode_before = _lmode(slave)
    # a second hold on the terminal, so its modes can be read after the
    # shell is gone (`last_mode`)
    hold = os.dup(slave)
    scr = Screen(cols, nrows)
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
        # the pty first: what the editor drew comes before the prompt
        # written after it
        r.sort(key=lambda fd: 0 if fd == master else 1)
        for fd in r:
            try:
                d = os.read(fd, 65536)
            except BlockingIOError:
                continue
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
                scr.feed(d)
            else:
                scr.feed(d)
                if scr.reply:
                    try:
                        os.write(master, scr.reply)
                    except OSError:
                        pass
                    scr.reply = b""
        return got

    def settle(step, want_prompt):
        """Wait until the shell waits for input, or exits."""
        start = time.time()
        if want_prompt:
            while time.time() - start < PROMPT_WAIT:
                pump(step, 0.05)
                if shown_tail(split_err(step.err)[1]) == shown_tail(want_prompt):
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

    global last_sig, last_screens, last_mode
    last_screens = []
    start_row = scr.r
    def type_bytes(step, data):
        """Write keys to the terminal, reading what it shows meanwhile.
        A pty takes a bounded amount of input (macOS: about 1 KB) and
        holds a bounded amount of output: one blocking write of a long
        line deadlocks against a shell echoing it (c_long_line hung on
        macOS until this)."""
        os.set_blocking(master, False)
        try:
            while data:
                _, w, _ = select.select([], [master], [], 0.05)
                if w:
                    try:
                        n = os.write(master, data)
                        data = data[n:]
                    except BlockingIOError:
                        pass
                pump(step, 0)
                if p.poll() is not None and data:
                    raise OSError("the shell is gone")
        finally:
            os.set_blocking(master, True)

    s0 = Step(None)
    settle(s0, want(0))
    steps.append(s0)
    last_screens.append(scr.snapshot(start_row))
    last_sig = None
    if any(label == "^C" for label, _ in keys):
        last_sig = _sig_state(p.pid)
    exit_line = None
    for label, data in keys:
        if p.poll() is not None:
            break
        st = Step(label)
        start_row = scr.r
        try:
            if data is None:
                # `\size COLS ROWS`: the window changes, nothing is typed
                cols, nrows = (int(x) for x in label.split()[1:3])
                fcntl.ioctl(hold, termios.TIOCSWINSZ, struct.pack("HHHH", nrows, cols, 0, 0))
                scr.resize(cols, nrows)
            elif SLOW > 0:
                # a slow line: one byte at a time, as a serial console
                # at a low rate delivers them
                for i in range(len(data)):
                    type_bytes(st, data[i:i + 1])
                    time.sleep(SLOW)
            else:
                type_bytes(st, data)
        except OSError:
            break
        settle(st, want(len(steps)))
        steps.append(st)
        last_screens.append(scr.snapshot(start_row))
    # wait for the exit reading all the while, as a terminal does: a
    # shell that puts its terminal's mode back waits for its output to
    # drain, and on macOS a pty's output drains only when it is read
    deadline = time.time() + (EXIT_WAIT if expect is not None else 3)
    rc = p.poll()
    while rc is None and time.time() < deadline:
        pump(steps[-1], 0.05)
        rc = p.poll()
    # whatever is still in flight belongs to the last step
    while (rout in open_fds or rerr in open_fds) and rc is not None:
        if not pump(steps[-1], 0.2):
            break
    if rc is not None and len(last_screens) == len(steps):
        # what the exit itself drew belongs to the last step
        last_screens[-1] = scr.snapshot(start_row)
    last_mode = None
    if rc is not None:
        last_mode = term_lmode(master, hold) == mode_before
    if rc is None:
        exit_line = "alive"
        # the session's whole tree, ended by pid (pelt#27): a group
        # signal missed every job the shell put in a group of its own,
        # and under the census reached the tracer, not the shell
        ended = lr.end_tree(p.pid, before)
        p.wait()
        lr.note(f"session {' '.join(argv)}", ended)
    lr.reap_adopted(before)
    elif rc < 0:
        exit_line = f"signal {-rc}"
    else:
        exit_line = f"exit {rc}"
    for fd in list(open_fds):
        os.close(fd)
    # the master first, then the slave: on macOS closing a terminal can
    # wait for its output to drain, and only a read of the master drains
    # it; once the master is closed there is nothing to wait for
    if master not in open_fds:
        try:
            os.close(master)
        except OSError:
            pass
    os.close(hold)
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
