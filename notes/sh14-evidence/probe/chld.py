import signal, subprocess, sys
def pre():
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
for sh in sys.argv[1:]:
    r = subprocess.run([sh, "-c", "/bin/sh -c 'exit 3'; echo st=$?; grep SigIgn /proc/self/status; trap 'echo c' CHLD; /bin/sh -c 'exit 4'; echo st=$?; trap"],
                       capture_output=True, text=True, preexec_fn=pre, timeout=30)
    print(sh, r.returncode, repr(r.stdout), repr(r.stderr))
