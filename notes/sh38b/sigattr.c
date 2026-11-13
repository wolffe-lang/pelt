/* Which senders does the kernel record in siginfo for a signal sent with
 * kill(2) to a child that is stopped, or running?  The parent sends every
 * signal itself, by the child's pid, so the true sender is always the
 * parent.  The child records si_signo, si_code and si_pid in its handlers
 * and prints them when it is done. */
#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

static volatile sig_atomic_t n;
static int rs[32], rc[32], rp[32];

static void h(int s, siginfo_t *si, void *u) {
    (void)u;
    if (n < 32) { rs[n] = s; rc[n] = si->si_code; rp[n] = si->si_pid; n++; }
}

static void nap(int ms) {
    struct timespec t = { ms / 1000, (ms % 1000) * 1000000L };
    while (nanosleep(&t, &t) == -1 && errno == EINTR) {}
}

static const char *nm(int s) {
    switch (s) {
    case SIGHUP: return "HUP"; case SIGTERM: return "TERM"; case SIGCONT: return "CONT";
    case SIGUSR1: return "USR1"; case SIGINT: return "INT"; default: return "?";
    }
}

/* how: 'r' child runs; 's' child stops itself (raise SIGSTOP); 'p' the
 * parent stops it with SIGSTOP.
 * seq: the signals, in order.  gap: ms between sends. */
static void run(const char *label, char how, const int *seq, int len, int gap) {
    pid_t parent = getpid();
    pid_t c = fork();
    if (c == 0) {
        struct sigaction a;
        memset(&a, 0, sizeof a);
        a.sa_sigaction = h;
        a.sa_flags = SA_SIGINFO;
        sigemptyset(&a.sa_mask);
        sigaction(SIGHUP, &a, 0); sigaction(SIGTERM, &a, 0);
        sigaction(SIGCONT, &a, 0); sigaction(SIGUSR1, &a, 0);
        sigaction(SIGINT, &a, 0);
        if (how == 's') raise(SIGSTOP);
        for (int i = 0; i < 100; i++) nap(10);
        printf("%-28s", label);
        for (int i = 0; i < n; i++) {
            const char *who = rp[i] == parent ? "parent" : rp[i] == 0 ? "0" : "other";
            printf(" %s:%s/code=0x%x", nm(rs[i]), who, (unsigned)rc[i]);
        }
        printf("\n");
        fflush(stdout);
        _exit(0);
    }
    int st;
    if (how == 's') {
        waitpid(c, &st, WUNTRACED);
    } else {
        nap(100);
        if (how == 'p') { kill(c, SIGSTOP); waitpid(c, &st, WUNTRACED); }

    }
    for (int i = 0; i < len; i++) {
        kill(c, seq[i]);
        if (gap) nap(gap);
    }
    /* a child left stopped is continued so that it can report and exit */
    nap(200);
    kill(c, SIGCONT);
    waitpid(c, &st, 0);
}

int main(void) {
    setvbuf(stdout, 0, _IONBF, 0);
    int hct[] = { SIGHUP, SIGCONT, SIGTERM };
    int hctc[] = { SIGHUP, SIGCONT, SIGTERM, SIGCONT };
    int c1[] = { SIGCONT };
    int tc[] = { SIGTERM, SIGCONT };
    int h1[] = { SIGHUP };
    int u1[] = { SIGUSR1 };
    int hu[] = { SIGHUP, SIGUSR1 };
    int ht[] = { SIGHUP, SIGTERM };
    for (int rep = 0; rep < 3; rep++) {
        printf("-- take %d (parent sends every signal)\n", rep + 1);
        run("run  HUP,CONT,TERM gap0", 'r', hct, 3, 0);
        run("run  HUP,CONT,TERM gap50", 'r', hct, 3, 50);
        run("run  CONT", 'r', c1, 1, 0);
        run("run  HUP,TERM gap0", 'r', ht, 2, 0);
        run("stop HUP,CONT,TERM,CONT gap0", 's', hctc, 4, 0);
        run("stop HUP,CONT,TERM gap0", 's', hct, 3, 0);
        run("stop HUP,CONT,TERM gap50", 's', hct, 3, 50);
        run("stop CONT", 's', c1, 1, 0);
        run("stop TERM,CONT gap50", 's', tc, 2, 50);
        run("stop HUP (then CONT)", 's', h1, 1, 0);
        run("stop USR1 (then CONT)", 's', u1, 1, 0);
        run("stop HUP,USR1 (then CONT)", 's', hu, 2, 50);
        run("pstop HUP,CONT,TERM gap50", 'p', hct, 3, 50);
    }
    return 0;
}
