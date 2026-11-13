/* Whom does the kernel name as the sender of the signals it makes itself?
 * G (this program) starts P; P starts C in a process group of its own and
 * C stops itself.  When P exits, C's group is orphaned with a stopped
 * member, and the kernel sends it SIGHUP and SIGCONT (POSIX _exit()).
 * Nobody calls kill(2) on C.  C records si_code and si_pid and prints
 * them, naming P's pid.  Each take is run twice: P exits by _exit(0), and
 * P is killed by G with SIGKILL (by P's pid). */
#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

static volatile sig_atomic_t n;
static int rs[16], rc[16], rp[16];

static void h(int s, siginfo_t *si, void *u) {
    (void)u;
    if (n < 16) { rs[n] = s; rc[n] = si->si_code; rp[n] = si->si_pid; n++; }
}

static void nap(int ms) {
    struct timespec t = { ms / 1000, (ms % 1000) * 1000000L };
    while (nanosleep(&t, &t) == -1 && errno == EINTR) {}
}

static void take(const char *label, int killed) {
    int fd[2];
    if (pipe(fd) != 0) return;
    pid_t p = fork();
    if (p == 0) {
        close(fd[0]);
        pid_t me = getpid();
        pid_t c = fork();
        if (c == 0) {
            struct sigaction a;
            memset(&a, 0, sizeof a);
            a.sa_sigaction = h;
            a.sa_flags = SA_SIGINFO;
            sigfillset(&a.sa_mask);
            sigaction(SIGHUP, &a, 0); sigaction(SIGCONT, &a, 0);
            setpgid(0, 0);
            raise(SIGSTOP);
            for (int i = 0; i < 50; i++) nap(10);
            char b[512]; int k = snprintf(b, sizeof b, "%-22s", label);
            for (int i = 0; i < n; i++) {
                const char *who = rp[i] == me ? "P(exited)" : rp[i] == 0 ? "0" : "other";
                k += snprintf(b + k, sizeof b - k, " %s:%s/code=0x%x",
                              rs[i] == SIGHUP ? "HUP" : rs[i] == SIGCONT ? "CONT" : "?", who,
                              (unsigned)rc[i]);
            }
            k += snprintf(b + k, sizeof b - k, "\n");
            (void)!write(fd[1], b, k);
            _exit(0);
        }
        close(fd[1]);
        int st;
        waitpid(c, &st, WUNTRACED);
        if (killed) { for (;;) pause(); }
        _exit(0);
    }
    close(fd[1]);
    if (killed) { nap(200); kill(p, SIGKILL); }
    int st;
    waitpid(p, &st, 0);
    char b[512]; ssize_t r;
    while ((r = read(fd[0], b, sizeof b)) > 0) (void)!write(1, b, r);
    close(fd[0]);
}

int main(void) {
    /* a session of its own, so that P's exit orphans C's group wherever
     * this runs (in a container, pid 1 would otherwise share it) */
    pid_t g = fork();
    if (g == 0) {
        setsid();
        alarm(30);
        for (int i = 0; i < 3; i++) {
            take("P _exit(0)", 0);
            take("P killed (SIGKILL)", 1);
        }
        _exit(0);
    }
    int st;
    waitpid(g, &st, 0);
    return 0;
}
