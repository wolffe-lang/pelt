"""Measure fish only through an owned pty, never implementation files."""
import fcntl, json, os, pty, re, select, struct, subprocess, sys, tempfile, termios, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import lib_session as ls
OUT = ROOT/'notes/sh30/fish'
OUT.mkdir(exist_ok=True)
CASES = {
    'command': [b'e', b'c', b'h', b'o', b' '],
    'unresolved': [b'zz_sh30_no_such_command', b' '],
    'reserved': [b'if', b' true', b'; end'],
    'quote-single': [b"echo '", b'hello', b"'"],
    'quote-double': [b'echo "', b'hello $HOME', b'"'],
    'variable': [b'echo $HOME'],
    'redirection': [b'echo >', b' output'],
    'comment': [b'echo word # comment'],
    'operator': [b'echo word |', b' cat'],
    'argument': [b'echo argument'],
    'bang': [b'!', b'!'],
    'enter-error': [b'echo )', b'\r'],
}
for term in ('xterm-256color', 'linux', 'dumb'):
    for name, steps in CASES.items():
        with tempfile.TemporaryDirectory(prefix='sh30-fish-') as temp:
            home = Path(temp)
            snapshot = home/'snapshot'
            variables = home/'variables'
            names = 'normal command keyword quote redirection end error param comment operator escape autosuggestion'
            init = "function fish_prompt; printf '$ '; end; set -g fish_greeting; "
            init += 'set --show ' + ' '.join('fish_color_'+n for n in names.split()) + ' > ' + str(variables) + '; '
            init += 'bind ctrl-o \'printf "%s\\n" (commandline) (commandline --cursor) > '+str(snapshot)+"'"
            master, slave = pty.openpty()
            fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack('HHHH', 24, 80, 0, 0))
            env = dict(PATH='/usr/bin:/bin', HOME=temp, LC_ALL='C.UTF-8', TERM=term)
            p = subprocess.Popen(['fish', '-i', '-C', init], stdin=slave, stdout=slave, stderr=slave,
                                 env=env, cwd=home, start_new_session=True, preexec_fn=ls._ctty)
            os.close(slave)
            screen = ls.Screen(80, 24)
            def drain(seconds=.25):
                data = b''
                end = time.monotonic()+seconds
                while time.monotonic() < end:
                    if select.select([master], [], [], .01)[0]:
                        try: chunk = os.read(master, 65536)
                        except OSError: break
                        data += chunk
                        screen.feed(chunk)
                        if b'\x1b[0c' in chunk: os.write(master, b'\x1b[?1;2c')
                        if screen.reply: os.write(master, screen.reply); screen.reply = b''
                return data
            rows = [dict(kind='start', raw=drain(.7).hex())]
            try:
                for step in steps:
                    os.write(master, step)
                    raw = drain()
                    rows.append(dict(input=step.hex(), raw=raw.hex(), sgr=[m.hex() for m in re.findall(rb'\x1b\[[0-9;:]*m', raw)]))
                os.write(master, b'\x0f')
                probe = drain(.1)
                result = dict(name=name, term=term, rows=rows, variables=variables.read_text() if variables.exists() else '',
                              snapshot=snapshot.read_text() if snapshot.exists() else None, probe_raw=probe.hex())
                (OUT/(name+'-'+term+'.json')).write_text(json.dumps(result, indent=2)+'\n')
                print(term, name, [(bytes.fromhex(r['input']), bytes.fromhex(r['raw'])) for r in rows[1:]], flush=True)
            finally:
                os.write(master, b'\x03exit\r')
                drain(.2)
                if p.poll() is None: p.kill()
                p.wait()
                os.close(master)
