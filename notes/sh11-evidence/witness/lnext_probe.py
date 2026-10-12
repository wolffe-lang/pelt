"""lnext_probe (sh11): which control keys reach a program whose terminal
has ICANON, ECHO and ISIG off but IEXTEN and IXON as a pty starts (on):
the mode pelt's editor can set through [os.term.mode]. Typed: Ctrl-V
Ctrl-A b Ctrl-O c Ctrl-S d Ctrl-Q e."""
import os, pty, termios, time
m, s = pty.openpty()
a = termios.tcgetattr(s)
a[3] &= ~(termios.ICANON | termios.ECHO | termios.ISIG)
a[6][termios.VMIN] = 0; a[6][termios.VTIME] = 1
termios.tcsetattr(s, termios.TCSANOW, a)
print("IEXTEN on:", bool(a[3] & termios.IEXTEN), "IXON on:", bool(a[0] & termios.IXON))
os.write(m, b"\x16\x01b\x0fc\x13d\x11e")
time.sleep(0.3)
print("slave read:", list(os.read(s, 100)))
