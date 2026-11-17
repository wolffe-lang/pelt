/* A test-only interposer that makes every file sync slow and logs it.
 *
 * tools/history-paths-witness compiles this into the row's own temporary
 * directory and loads it into the pelt it starts, through LD_PRELOAD on
 * Linux and DYLD_INSERT_LIBRARIES on macOS. PELT_SYNC_DELAY_MS (0 to
 * 1000) is slept before each sync; PELT_SYNC_LOG, when set, gets two
 * lines per sync, "BEGIN pid=<pid> fd=<fd> rc=0" before the delay and
 * "END pid=<pid> fd=<fd> rc=<rc>" after the real call.
 * Only documented interfaces: fsync(2), fdatasync(2), fcntl(2)'s
 * F_FULLFSYNC, dlsym(3) and nanosleep(2).
 */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

static void note(const char *kind, int fd, int rc) {
    const char *path = getenv("PELT_SYNC_LOG");
    if (!path || !*path) return;
    int log = open(path, O_WRONLY | O_CREAT | O_APPEND | O_CLOEXEC, 0600);
    if (log < 0) return;
    char line[96];
    int n = snprintf(line, sizeof line, "%s pid=%ld fd=%d rc=%d\n", kind,
                     (long)getpid(), fd, rc);
    if (n > 0 && n < (int)sizeof line) {
        ssize_t wrote = write(log, line, (size_t)n);
        (void)wrote;
    }
    (void)close(log);
}

static void slow(void) {
    const char *text = getenv("PELT_SYNC_DELAY_MS");
    long ms = text ? strtol(text, 0, 10) : 0;
    if (ms <= 0 || ms > 1000) return;
    struct timespec left = {ms / 1000, (ms % 1000) * 1000000L};
    while (nanosleep(&left, &left) != 0 && errno == EINTR) {}
}

#ifdef __APPLE__
/* dyld's interposing table: calls from other images reach these, and
 * the calls made in here reach the originals. */
static int slow_fsync(int fd) {
    note("BEGIN", fd, 0);
    slow();
    int rc = fsync(fd);
    int saved = errno;
    note("END", fd, rc);
    errno = saved;
    return rc;
}

static int slow_fcntl(int fd, int cmd, ...) {
    va_list ap;
    va_start(ap, cmd);
    void *arg = va_arg(ap, void *);
    va_end(ap);
    if (cmd != F_FULLFSYNC) return fcntl(fd, cmd, arg);
    note("BEGIN", fd, 0);
    slow();
    int rc = fcntl(fd, cmd);
    int saved = errno;
    note("END", fd, rc);
    errno = saved;
    return rc;
}

__attribute__((used, section("__DATA,__interpose")))
static const struct { const void *with; const void *instead_of; } interposed[] = {
    {(const void *)slow_fsync, (const void *)fsync},
    {(const void *)slow_fcntl, (const void *)fcntl},
};
#else
static int (*real_fsync)(int);
static int (*real_fdatasync)(int);

int fsync(int fd) {
    if (!real_fsync) real_fsync = (int (*)(int))dlsym(RTLD_NEXT, "fsync");
    if (!real_fsync) { errno = ENOSYS; return -1; }
    note("BEGIN", fd, 0);
    slow();
    int rc = real_fsync(fd);
    int saved = errno;
    note("END", fd, rc);
    errno = saved;
    return rc;
}

int fdatasync(int fd) {
    if (!real_fdatasync) real_fdatasync = (int (*)(int))dlsym(RTLD_NEXT, "fdatasync");
    if (!real_fdatasync) { errno = ENOSYS; return -1; }
    note("BEGIN", fd, 0);
    slow();
    int rc = real_fdatasync(fd);
    int saved = errno;
    note("END", fd, rc);
    errno = saved;
    return rc;
}
#endif
