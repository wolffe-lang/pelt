# Keys at the prompt

pelt's POSIX editor is emacs by default, or vi with `set -o vi`.
The friendly campaign adds interactive keys under `set -o friendly`.
Friendly remains **opt-in at this pin**: wolf 0.2.35 cannot report the
invocation's argv[0] (wolf-lang#904, fixed after the pin). Once re-pinned,
the default-on recommendation can exclude an invocation named `sh`.
`--posix` is a hard disable; scripts, `-c` and pipes get no friendly keys.
Both stdin and stderr must be terminals. `set +o friendly` restores the
POSIX editor; `set +o friendly_keys` disables the extra keys alone.

## How this table was obtained

The baseline is pelt `70eec14`. The reference programs were run, never read:
dash **0.5.13.4-1.1**, bash **5.3.20-2**, fish **4.9.3-1**, on kasumi,
CPUs 12–15, inside the lane's rootless Arch container. Image id
`3ed18d5c7b242c675807f875e43eabf11bdf87f9eebd875fce9e9b1d1bf7297f`,
digest `sha256:8185e444e45ba166146b244b41f1cba2d7d91f3eddce533a839cc9591e0fa785`.
`notes/sh28-evidence/logs/` retains `bind -p`, fish `bind`, `stty -a`,
the installed bash 5.3 manual's Readline chapter and fish's bind manual.
Those are documentation and black-box outputs, not implementation sources.
Pelt CI itself has no pinned oracle image: its runners are ubuntu-latest
and macOS. Reproducing the oracle environment in CI is a track gap.

`C-` means Ctrl, `M-` means Alt (an ESC byte first), and `ESC` is hex 1b.
A key listed as an editor key does not bind that byte in a script or pipe.
An unrecognised CSI/SS3 sequence is consumed, not inserted. Plain printable
characters insert themselves; C-V quotes the following byte.

## The POSIX editor at the baseline

| pelt key | accepted bytes | action | readline | fish | stty / verdict |
|---|---|---|---|---|---|
| C-A / Home | `01`, `ESC[H`, `ESCOH`, `ESC[1~`, `ESC[7~` | beginning of line | beginning-of-line | beginning-of-line | editor key |
| C-E / End | `05`, `ESC[F`, `ESCOF`, `ESC[4~`, `ESC[8~` | end of line | end-of-line | end-of-line | editor key |
| C-B / Left | `02`, `ESC[D`, `ESCOD` | backward character | backward-char | backward-char | editor key |
| C-F / Right | `06`, `ESC[C`, `ESCOC` | forward character | forward-char | forward-char | editor key |
| M-B / Ctrl-Left | `ESC b`, `ESC B`, `ESC[1;5D`, `ESC[1;3D` | backward word | backward-word | prevd-or-backward-word / backward-token | editor key; pelt words are letters/digits/non-ASCII |
| M-F / Ctrl-Right | `ESC f`, `ESC F`, `ESC[1;5C`, `ESC[1;3C` | forward word | forward-word | nextd-or-forward-word / forward-token | editor key |
| M-D | `ESC d`, `ESC D` | kill forward word | kill-word | kill-word / directory history | editor key |
| M-Backspace | `ESC 7f`, `ESC 08` | kill backward word | backward-kill-word | backward-kill-word | editor key |
| C-W | `17` or stty werase | kill backward blank-delimited word | unix-word-rubout | backward-kill-path-component | honours stty |
| C-U | `15` or stty kill | kill to beginning | unix-line-discard | backward-kill-line | honours stty |
| C-K | `0b` | kill to end | kill-line | kill-line | editor key |
| C-Y | `19` | yank most recent kill | yank | yank | editor key |
| Backspace / C-H | `7f`, `08`, or stty erase | delete backward character | backward-delete-char | backward-delete-char | honours stty; 7f/08 aliases unless another special character wins |
| Delete | `ESC[3~` | delete character | delete-char | delete-char | editor key |
| C-D | `04` or stty eof | EOF on empty line, otherwise delete character | delete-char / EOF | delete-or-exit | honours stty |
| C-L | `0c` | clear screen and redraw | clear-screen | clear-screen | editor key |
| C-C | `03` or stty intr | abandon line, status 130; ignored when INT ignored | interrupt | clear-commandline | honours stty |
| C-P / Up | `10`, `ESC[A`, `ESCOA` | previous history | previous-history | up-or-search | editor key; fish's filtered history is sh29 |
| C-N / Down | `0e`, `ESC[B`, `ESCOB` | next history / saved draft | next-history | down-or-search | editor key |
| C-R | `12` | incremental backward substring search | reverse-search-history | history-pager | editor wins over default stty rprnt |
| C-V | `16` or stty lnext | quote next byte | quoted-insert | clipboard paste | honours stty; not fish's clipboard |
| Tab | `09` | complete; second Tab lists | complete | complete | editor key; commands/files/variables only |
| Enter | `0d`, `0a` | accept line | accept-line | execute | editor key |
| C-\\, C-Z, C-Q, C-S | `1c`, `1a`, `11`, `13` by default | ignored while editing | terminal/editor dependent | cancel/undo/pager functions vary | quit/susp/start/stop: ignore at prompt; restored for jobs |

## vi mode

Insert mode honours stty erase, kill, intr, eof, werase, lnext, CR/LF,
ESC (command mode), the arrows, and Tab completion. C-V Tab inserts a tab.
Command mode honours intr/eof, but printable stty erase characters remain
vi commands. Counts apply where XCU defines them.

| pelt command | action | readline / fish comparison | verdict |
|---|---|---|---|
| `h`, Left / `l`, space, Right | previous / next character | bash vi mode; fish vi is not the default | XCU |
| `w W`, `b B`, `e E` | next word, previous word, word end; capital form uses blanks | bash vi | XCU |
| `0`, `^`, `$`, `|`, Home, End | beginning, first nonblank, end, numbered column | bash vi | XCU |
| `f F t T`, `;`, `,` | find character forward/back; repeat/reverse | bash vi | XCU |
| `i I a A`, `R` | insert here/start/after/end; overwrite | bash vi | XCU |
| `c` motion, `cc`, `C`, `S` | change range/line/rest/line | bash vi | XCU |
| `d` motion, `dd`, `D`, `x X` | delete range/line/rest/character | bash vi | XCU |
| `y` motion, `yy`, `Y`, `p P` | yank range/line/rest; put after/before | bash vi | XCU |
| `r`, `~` | replace character; swap case | bash vi | XCU |
| `.`, `u`, `U` | repeat change; undo/toggle undo; restore original line | bash vi | XCU |
| `k`, `-`, Up / `j`, `+`, Down | previous / next history | bash vi | XCU |
| `[number]G` | history number; uncounted oldest | bash vi | XCU |
| `/`, `?`, `n`, `N` | history search; repeat/reverse | bash vi | XCU |
| `[number]_` | insert a space and previous line's last / numbered word, enter insert mode | measured against bash vi only | dash binary has no libedit/editor; no claim about dash libedit |
| `[number]v` | edit line/history through vi and fc | bash vi | XCU |
| `#`, CR/LF, C-L | comment and accept; accept; redraw | bash vi | XCU |
| `=`, `\\`, `*` | list / complete / expand pathname bigword | bash vi | XCU |
| `@letter` | named alias `_letter` command | no enabled aliases in original sh11 path | existing path; alias integration not this lane |

## Friendly additions

This section is completed from the measured sessions as implementations land.
The complete measured readline and fish inventories follow; a missing action
is not silently claimed as supported. PageUp/PageDown follow measured fish
beginning/end-of-history, not prefix search. Bash's repeated M-. removes the
last insertion on running past the oldest entry. Both correct the initial
campaign guesses (R-sh28-2).

## Terminal characters

The API `os_term_chars` exposes ten slots only. This table describes the
same editor code on Linux and macOS, not a claim of a macOS measurement.
Every mode is restored before a command, job or child runs.

| stty name | Linux default | pelt at the prompt | verdict |
|---|---|---|---|
| intr | C-C | abort line; ignored with ignored INT | honoured |
| quit | C-\\ | no effect | ignored (dash/bash interactive shells ignore QUIT) |
| erase | DEL | backward erase | honoured |
| kill | C-U | kill to beginning | honoured |
| eof | C-D | EOF only on empty line, otherwise delete | honoured |
| eol / eol2 | undefined | not exposed by pinned API; printable assigned values are ordinary text | missing; issue text in lane evidence |
| swtch | undefined | no editor action; no Linux job-control switch | ignored / platform legacy |
| start / stop | C-Q / C-S | FLOW disabled while editing; bytes consumed without flow control | passed through line discipline to editor, ignored there |
| susp | C-Z | no suspension at prompt; restored for foreground jobs | ignored at prompt |
| rprnt | C-R | incremental search; remapping not exposed | editor key wins; API gap |
| werase | C-W | kill previous blank-delimited word | honoured |
| lnext | C-V | insert following byte literally | honoured |
| discard | C-O | EXTENDED disabled; unbound C-O ignored | passed through discipline; remapping not exposed |
| dsusp | absent on Linux | no pinned API slot on either host | platform legacy / API gap |

When exposed characters collide, intr wins, then eof, then erase, kill,
werase and lnext, then ignored quit/susp/start/stop. Default C-U/C-W/C-V
stop working when moved or disabled; DEL/C-H remain erase aliases unless
another special character claims them. Remapped rprnt/eol/eol2/discard
cannot be honoured until the terminal API exposes them. No `stty` subprocess
is spawned at a prompt.
