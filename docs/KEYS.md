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
`notes/sh28-evidence/logs/` retains `bind -p`, fish `bind` and `stty -a`.
Documentation was read with `info --subnodes '(bash) Bindable Readline Commands'` and `fish --no-config -c 'bind --help'`.
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
| C-\\ | `1c` or stty quit | clear pending input (updated in this pass) | terminal flush | not a default editing action | honoured, no editor signal |
| C-Z, C-Q, C-S | `1a`, `11`, `13` by default | ignored while editing | terminal/editor dependent | undo/pager functions vary | susp/start/stop ignored at prompt; restored for jobs |

## Foreground jobs and terminal keys

These are terminal actions while a foreground job, rather than the line
editor, owns the terminal. They are not new friendly key bindings. The
saved terminal mode is restored before a command runs (sh17/sh18's job
sessions and the current job-control sessions cover the separation).

| key / stty character | bytes by default | at the prompt | with a foreground job | verdict |
|---|---|---|---|---|
| C-C / intr | `03` | abandon edit, status 130 unless INT ignored | terminal delivers INT to foreground group; pelt takes terminal back when it ends | honoured; foreground action is not an editor injection |
| C-Z / susp | `1a` | ignored, not undo | terminal stops foreground job; `fg` resumes it and `bg` resumes in background | honoured outside editor; shell itself stays at prompt |
| C-\ / quit | `1c` | clear pending edit, no signal/status change | terminal's normal QUIT action for foreground group | editor flush and actual signal are distinct |
| C-D / eof | `04` | EOF on empty edit, otherwise delete | terminal's canonical EOF character / child's own read policy | honoured; it is not a signal |
| C-S / stop, C-Q / start | `13`, `11` | ignored with FLOW off | terminal flow control if the restored mode enables it | passed to terminal outside editor |
| C-V / lnext, C-W / werase, erase, kill | `16`, `17`, `7f`, `15` | editor implements the configured values | restored line discipline or foreground program interprets them | terminal mode, not a second pelt editor |

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

These act only with `friendly` and `friendly_keys` on at an interactive
terminal prompt. Stty characters take precedence over editor defaults.
Lower-case Alt letters have upper-case aliases. `bindings` prints the
current mode's keys, bytes and actions, followed by the live stty values;
`bindings -l` lists actions once. It cannot change a binding and rejects
operands other than `-l` with status 2. With both editing modes off it
reports disabled. Outside a friendly terminal prompt it is not a built-in.

| pelt key | bytes | action | readline | fish | verdict |
|---|---|---|---|---|---|
| M-. / M-_ | `ESC .`, `ESC _` | yank previous history line's last word, quotes kept | yank-last-arg | history-token-search-backward | line-by-line readline semantics; repeat replaces insertion, past oldest removes it and rings |
| M-y | `ESC y`, `ESC Y` | cycle the preceding yank through 10 kills | yank-pop | yank-pop | only immediately after C-Y / M-y; consecutive kills join |
| C-t | `14` | transpose characters, including combining clusters | transpose-chars | transpose-chars | at end, last two; counted motion clamps at end rather than swapping back; negative count has no effect |
| M-t | `ESC t`, `ESC T` | transpose words | transpose-words | transpose-words | positive count exchanges endpoint words and clamps motions; negative count has no effect in the measured bash session |
| M-u | `ESC u`, `ESC U` | upper-case word forward | upcase-word | upcase-word | ASCII case conversion, as tested in C locale; negative count works backward without moving point |
| M-l | `ESC l`, `ESC L` | lower-case word forward | downcase-word | file listing helper | readline action; not fish's listing helper |
| M-c | `ESC c`, `ESC C` | capitalise word forward | capitalize-word | capitalize-word | same word boundaries as M-f |
| C-_ / C-x C-u | `1f`, `18 15` | undo one edit group per press | undo | undo | consecutive insertion is one group; retained separately for each recalled line |
| M-r | `ESC r`, `ESC R` | revert current line to its original text | revert-line | unbound | recalled history restored; a fresh draft becomes empty |
| M-< / PageUp | `ESC <`, `ESC[5~` | oldest history entry | beginning-of-history | binding named beginning-of-history | readline's behavior; see fish observation below |
| M-> / PageDown | `ESC >`, `ESC[6~` | saved draft after newest entry | end-of-history | binding named end-of-history | readline's behavior |
| M-# | `ESC #` | prepend # and accept as comment | insert-comment | comment toggle without accepting | numeric argument toggles an existing leading # before accepting |
| M-\ | `ESC 5c` | delete blanks/tabs on both sides of point | delete-horizontal-space | unbound | not a kill |
| C-] / M-C-] | `1d`, `ESC 1d` | find next / previous character | character-search / backward | unbound | C-g cancels the awaited character; negative count reverses direction |
| M-0..9 / M-- | `ESC 30..39`, `ESC 2d` | argument to next command | digit-argument | unbound | following digits may be plain or Alt; zero and negative arguments, bounded at 99,999; explicit counted deletion is a kill |
| C-g | `07`, `ESC 07`, `18 07` | abort multi-key command or search and ring | abort | cancel | resets numeric argument; search restores pre-search line |
| C-@ / C-Space / M-Space | `00`, `ESC 20` | set mark at point (or numbered position) | set-mark | space insertion | documented readline intent; bash's measured NUL non-effect is not copied |
| C-x C-x | `18 18` | exchange point and mark | exchange-point-and-mark | unbound | mark is a saved index; the measured M-Space mark is not shifted by later insertions |

A numeric argument to the first M-. chooses history word n (command word
is 0); negative n selects backwards from the last word with 0-based offset.
A negative argument on a repeated M-. reverses traversal. A redirection's
operand is a word; a one-word command yanks itself. Empty history rings.
Alt-dot itself does not expand the shell language. The separate friendly
`histexpand` option now recognizes `!!` and `!$` at Enter (see below).

**Measured fish context.** Fish's `bind` names PageUp/PageDown
beginning/end-of-history. In the all-tty black-box probe, PageUp at a
fresh empty line did nothing; after C-p it left the newest entry selected,
not the oldest. PageDown restored the draft. Pelt deliberately uses the
readline history-end behavior consistently. Fish's filtered Up/Down and
history UI belong to the autosuggestion phase, not this key pass.

**Measured exceptions.** Bash C-@ did not set mark in this pty, although
its bind table and manual assign set-mark; M-Space did work. Pelt accepts
both. Pelt's kill ring is capped at 10 entries, unlike bash's longer ring.
The editor's quit flush does not itself send QUIT, change status or run a
trap; an explicitly installed QUIT trap still follows pelt's existing
signal machinery. The bash reference with an actual tty QUIT signal ran
that trap. Own transcripts pin these intentional differences.

## Terminal characters

The API `os_term_chars` exposes ten slots only. This table describes the
same editor code on Linux and macOS, not a claim of a macOS measurement.
Every mode is restored before a command, job or child runs.

| stty name | Linux default | pelt at the prompt | verdict |
|---|---|---|---|
| intr | C-C | abort line; ignored with ignored INT | honoured |
| quit | C-\\ | discard pending input and redraw empty edit line | honoured: pending input cleared; no signal/status/trap of its own |
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
werase and lnext, then quit flush, then ignored susp/start/stop. Default C-U/C-W/C-V
stop working when moved or disabled; DEL/C-H remain erase aliases unless
another special character claims them. Remapped rprnt/eol/eol2/discard
cannot be honoured until the terminal API exposes them. No `stty` subprocess
is spawned at a prompt.

## Complete readline inventory

`bind -p` reported **83 named bound actions**, **82** after treating `insert-last-argument` as the alias of `yank-last-arg`. At the baseline pelt covered **22** of these actions, leaving **60** absent. This pass adds **19** distinct actions. These are action counts, not counts of key aliases. The original prediction counted too few of the full default inventory. Rows below retain every measured byte alias, including aliases pelt does not accept; the pelt column lists its own accepted keys. A shared action name is not a promise that every bash alias or every numeric corner is present.

| readline action | measured readline bytes | pelt key | fish comparison | stty / verdict |
|---|---|---|---|---|
| abort | `\C-g` / `\C-x\C-g` / `\e\C-g` | C-g | see fish inventory | friendly addition; terminal precedence as above |
| accept-line | `\C-j` / `\C-m` | Enter | see fish inventory | present at baseline; aliases/terminal precedence as above |
| backward-char | `\C-b` / `\eOD` / `\e[D` | C-b / Left | same named action | present at baseline; aliases/terminal precedence as above |
| backward-delete-char | `\C-h` / `\C-?` | Backspace / C-h | same named action | present at baseline; aliases/terminal precedence as above |
| backward-kill-line | `\C-x\C-?` | — | same named action | not this lane: C-x Rubout alias not added; C-u supplies this edit |
| backward-kill-word | `\e\C-h` / `\e\C-?` | M-Backspace | same named action | present at baseline; aliases/terminal precedence as above |
| backward-word | `\e\e[D` / `\e[1;3D` / `\e[1;5D` / `\e[5D` / `\eb` | M-b / Ctrl-Left | see fish inventory | present at baseline; aliases/terminal precedence as above |
| beginning-of-history | `\e<` / `\e[5~` | M-< / PageUp | same named action | friendly addition; terminal precedence as above |
| beginning-of-line | `\C-a` / `\eOH` / `\e[1~` / `\e[7~` / `\e[H` | C-a / Home | same named action | present at baseline; aliases/terminal precedence as above |
| bracketed-paste-begin | `\e[200~` | — | see fish inventory | not this lane: paste protocol is not this lane; control-safe paste needs its own sessions |
| call-last-kbd-macro | `\C-xe` | — | see fish inventory | not this lane: keyboard macro recording/replay is not this lane |
| capitalize-word | `\ec` | M-c | same named action | friendly addition; terminal precedence as above |
| character-search | `\C-]` | C-] | see fish inventory | friendly addition; terminal precedence as above |
| character-search-backward | `\e\C-]` | M-C-] | see fish inventory | friendly addition; terminal precedence as above |
| clear-display | `\e\C-l` | — | see fish inventory | not this lane: scrollback erase is not portable to the PAX target; C-l redraws the screen |
| clear-screen | `\C-l` | C-l | see fish inventory | present at baseline; aliases/terminal precedence as above |
| complete | `\C-i` / `\e\e` | Tab | same named action | present at baseline; aliases/terminal precedence as above |
| complete-command | `\e!` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| complete-filename | `\e/` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| complete-hostname | `\e@` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| complete-into-braces | `\e{` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| complete-username | `\e~` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| complete-variable | `\e$` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| delete-char | `\C-d` / `\e[3~` | C-d / Delete | same named action | present at baseline; aliases/terminal precedence as above |
| delete-horizontal-space | `\e\\` | M-\ | see fish inventory | friendly addition; terminal precedence as above |
| digit-argument | `\e-` / `\e0` / `\e1` / `\e2` / `\e3` / `\e4` / `\e5` / `\e6` / `\e7` / `\e8` / `\e9` | M-digits / M-- | see fish inventory | friendly addition; terminal precedence as above |
| display-shell-version | `\C-x\C-v` | — | see fish inventory | not this lane: version-display chord, not an edit; no inputrc interpreter |
| do-lowercase-version | `\C-xA` / `\C-xB` / `\C-xC` / `\C-xD` / `\C-xE` / `\C-xF` / `\C-xG` / `\C-xH` / `\C-xI` / `\C-xJ` / `\C-xK` / `\C-xL` / `\C-xM` / `\C-xN` / `\C-xO` / `\C-xP` / `\C-xQ` / `\C-xR` / `\C-xS` / `\C-xT` / `\C-xU` / `\C-xV` / `\C-xW` / `\C-xX` / `\C-xY` / `\C-xZ` / `\eA` / `\eB` / `\eC` / `\eD` / `\eE` / `\eF` / `\eG` / `\eH` / `\eI` / `\eJ` / `\eK` / `\eL` / `\eM` / `\eN` / `\eP` / `\eQ` / `\eR` / `\eS` / `\eT` / `\eU` / `\eV` / `\eW` / `\eX` / `\eY` / `\eZ` | — | see fish inventory | not this lane: partial: M-uppercase aliases work; C-x uppercase dispatch is not added |
| downcase-word | `\el` | M-l | see fish inventory | friendly addition; terminal precedence as above |
| dynamic-complete-history | `\e\C-i` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| edit-and-execute-command | `\C-x\C-e` | — | see fish inventory | not this lane: use fc (or vi v); no new C-x C-e launch path |
| end-kbd-macro | `\C-x)` | — | see fish inventory | not this lane: keyboard macro recording/replay is not this lane |
| end-of-history | `\e>` / `\e[6~` | M-> / PageDown | same named action | friendly addition; terminal precedence as above |
| end-of-line | `\C-e` / `\eOF` / `\e[4~` / `\e[8~` / `\e[F` | C-e / End | same named action | present at baseline; aliases/terminal precedence as above |
| exchange-point-and-mark | `\C-x\C-x` | C-x C-x | see fish inventory | friendly addition; terminal precedence as above |
| execute-named-command | `\ex` | — | see fish inventory | not this lane: requires named command dispatch/rebinding; read-only bindings only |
| forward-char | `\C-f` / `\eOC` / `\e[C` | C-f / Right | same named action | present at baseline; aliases/terminal precedence as above |
| forward-search-history | `\C-s` | — | see fish inventory | not this lane: forward incremental/history UI is the autosuggestion phase |
| forward-word | `\e\e[C` / `\e[1;3C` / `\e[1;5C` / `\e[5C` / `\ef` | M-f / Ctrl-Right | see fish inventory | present at baseline; aliases/terminal precedence as above |
| glob-complete-word | `\eg` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| glob-expand-word | `\C-x*` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| glob-list-expansions | `\C-xg` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| history-expand-line | `\e^` | — | see fish inventory | not this lane: line/history expansion is not added; POSIX expansion still happens when accepted |
| insert-comment | `\e#` | M-# | see fish inventory | friendly addition; terminal precedence as above |
| insert-completions | `\e*` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| insert-last-argument | `\e.` / `\e_` | M-. / M-_ | see fish inventory | friendly addition; terminal precedence as above |
| kill-line | `\C-k` | C-k | same named action | present at baseline; aliases/terminal precedence as above |
| kill-word | `\e[3;5~` / `\ed` | M-d | same named action | present at baseline; aliases/terminal precedence as above |
| next-history | `\C-n` / `\eOB` / `\e[B` | C-n / Down | see fish inventory | present at baseline; aliases/terminal precedence as above |
| non-incremental-forward-search-history | `\en` | — | see fish inventory | not this lane: vi ?/n/N and C-r cover this pass; extra emacs search not added |
| non-incremental-reverse-search-history | `\ep` | — | see fish inventory | not this lane: vi / and C-r cover this pass; extra emacs search not added |
| operate-and-get-next | `\C-o` | — | see fish inventory | not this lane: default C-o overlaps discard; operation-and-next command not added |
| possible-command-completions | `\C-x!` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| possible-completions | `\e=` / `\e?` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| possible-filename-completions | `\C-x/` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| possible-hostname-completions | `\C-x@` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| possible-username-completions | `\C-x~` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| possible-variable-completions | `\C-x$` | — | see fish inventory | not this lane: specialised completion chord not added; Tab and vi =/\/* are available |
| previous-history | `\C-p` / `\eOA` / `\e[A` | C-p / Up | see fish inventory | present at baseline; aliases/terminal precedence as above |
| quoted-insert | `\C-q` / `\C-v` / `\e[2~` | C-v / stty lnext | see fish inventory | present at baseline; aliases/terminal precedence as above |
| re-read-init-file | `\C-x\C-r` | — | see fish inventory | not this lane: no inputrc language; bindings is read-only |
| reverse-search-history | `\C-r` | C-r | see fish inventory | present at baseline; aliases/terminal precedence as above |
| revert-line | `\e\C-r` / `\er` | M-r | see fish inventory | friendly addition; terminal precedence as above |
| self-insert | ` ` / `!` / `\"` / `#` / `$` / `%` / `&` / `'` / `(` / `)` / `*` / `+` / `,` / `-` / `.` / `/` / `0` / `1` / `2` / `3` / `4` / `5` / `6` / `7` / `8` / `9` / `:` / `;` / `<` / `=` / `>` / `?` / `@` / `A` / `B` / `C` / `D` / `E` / `F` / `G` / `H` / `I` / `J` / `K` / `L` / `M` / `N` / `O` / `P` / `Q` / `R` / `S` / `T` / `U` / `V` / `W` / `X` / `Y` / `Z` / `[` / `\\` / `]` / `^` / `_` / ``` / `a` / `b` / `c` / `d` / `e` / `f` / `g` / `h` / `i` / `j` / `k` / `l` / `m` / `n` / `o` / `p` / `q` / `r` / `s` / `t` / `u` / `v` / `w` / `x` / `y` / `z` / `{` / `\|` / `}` / `~` / `\200` / `\201` / `\202` / `\203` / `\204` / `\205` / `\206` / `\207` / `\210` / `\211` / `\212` / `\213` / `\214` / `\215` / `\216` / `\217` / `\220` / `\221` / `\222` / `\223` / `\224` / `\225` / `\226` / `\227` / `\230` / `\231` / `\232` / `\233` / `\234` / `\235` / `\236` / `\237` / `\240` / `\241` / `\242` / `\243` / `\244` / `\245` / `\246` / `\247` / `\250` / `\251` / `\252` / `\253` / `\254` / `\255` / `\256` / `\257` / `\260` / `\261` / `\262` / `\263` / `\264` / `\265` / `\266` / `\267` / `\270` / `\271` / `\272` / `\273` / `\274` / `\275` / `\276` / `\277` / `\300` / `\301` / `\302` / `\303` / `\304` / `\305` / `\306` / `\307` / `\310` / `\311` / `\312` / `\313` / `\314` / `\315` / `\316` / `\317` / `\320` / `\321` / `\322` / `\323` / `\324` / `\325` / `\326` / `\327` / `\330` / `\331` / `\332` / `\333` / `\334` / `\335` / `\336` / `\337` / `\340` / `\341` / `\342` / `\343` / `\344` / `\345` / `\346` / `\347` / `\350` / `\351` / `\352` / `\353` / `\354` / `\355` / `\356` / `\357` / `\360` / `\361` / `\362` / `\363` / `\364` / `\365` / `\366` / `\367` / `\370` / `\371` / `\372` / `\373` / `\374` / `\375` / `\376` / `\377` | printable UTF-8 | same named action | present at baseline; aliases/terminal precedence as above |
| set-mark | `\C-@` / `\e ` | C-@ / M-Space | see fish inventory | friendly addition; terminal precedence as above |
| shell-backward-word | `\e\C-b` | — | see fish inventory | not this lane: shell-token editing family not added; ordinary word editing is available |
| shell-expand-line | `\e\C-e` | — | see fish inventory | not this lane: line/history expansion is not added; POSIX expansion still happens when accepted |
| shell-forward-word | `\e\C-f` | — | see fish inventory | not this lane: shell-token editing family not added; ordinary word editing is available |
| shell-kill-word | `\e\C-d` | — | see fish inventory | not this lane: shell-token editing family not added; ordinary word editing is available |
| shell-transpose-words | `\e\C-t` | — | see fish inventory | not this lane: shell-token editing family not added; ordinary word editing is available |
| spell-correct-word | `\C-xs` | — | see fish inventory | not this lane: no spelling oracle or dictionary subsystem in this pass |
| start-kbd-macro | `\C-x(` | — | see fish inventory | not this lane: keyboard macro recording/replay is not this lane |
| tilde-expand | `\e&` | — | see fish inventory | not this lane: line/history expansion is not added; POSIX expansion still happens when accepted |
| transpose-chars | `\C-t` | C-t | same named action | friendly addition; terminal precedence as above |
| transpose-words | `\et` | M-t | same named action | friendly addition; terminal precedence as above |
| undo | `\C-x\C-u` / `\C-_` | C-_ / C-x C-u | same named action | friendly addition; terminal precedence as above |
| unix-line-discard | `\C-u` | C-u / stty kill | see fish inventory | present at baseline; aliases/terminal precedence as above |
| unix-word-rubout | `\C-w` | C-w / stty werase | see fish inventory | present at baseline; aliases/terminal precedence as above |
| upcase-word | `\eu` | M-u | same named action | friendly addition; terminal precedence as above |
| yank | `\C-y` | C-y | same named action | present at baseline; aliases/terminal precedence as above |
| yank-last-arg | `\e.` / `\e_` | M-. / M-_ | see fish inventory | friendly addition; terminal precedence as above |
| yank-nth-arg | `\e\C-y` | — | see fish inventory | not this lane: use M-n M-.; the M-C-y alias is not bound |
| yank-pop | `\ey` | M-y | same named action | friendly addition; terminal precedence as above |

## Complete fish default inventory

All **95** measured default rows follow. Of the distinct command payloads, **28** have no same-named readline action or mapped basic editor equivalent (up/down-or-search, buffer ends, cancel, execute, delete-or-exit, directory/word motion, path rubout and token-history insertion are mapped). This is a reproducible payload count, not a claim that fish has only that many extra behaviors: a conditional fish command payload may perform several operations.

| fish key | measured fish action / command payload | pelt equivalent | stty / verdict |
|---|---|---|---|
| ctrl-y | yank | C-y | action or basic equivalent present; stty precedence applies |
| alt-y | yank-pop | M-y | action or basic equivalent present; stty precedence applies |
| right | forward-char | C-f / Right | action or basic equivalent present; stty precedence applies |
| left | backward-char | C-b / Left | action or basic equivalent present; stty precedence applies |
| ctrl-right | forward-token | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| ctrl-left | backward-token | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| pageup | beginning-of-history | M-< / PageUp | pelt uses readline history ends; fish contextual observation above |
| pagedown | end-of-history | M-> / PageDown | pelt uses readline history ends; fish contextual observation above |
| ctrl-x | fish_clipboard_copy | — | no clipboard integration; PAX needs a portable policy first |
| ctrl-v | fish_clipboard_paste | — | no clipboard integration; PAX needs a portable policy first |
| escape | cancel | C-g | action or basic equivalent present; stty precedence applies |
| ctrl-[ | cancel | C-g | action or basic equivalent present; stty precedence applies |
| tab | complete | Tab | action or basic equivalent present; stty precedence applies |
| ctrl-i | complete | Tab | action or basic equivalent present; stty precedence applies |
| ctrl-s | pager-toggle-search | — | fish filtered history/pager is the autosuggestion/completion campaign, not this pass |
| shift-tab | complete-and-search | — | fish filtered history/pager is the autosuggestion/completion campaign, not this pass |
| shift-delete | history-delete or backward-delete-char | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| down | down-or-search | C-n / Down | fish filtered history/pager is the autosuggestion/completion campaign, not this pass |
| up | up-or-search | C-p / Up | fish filtered history/pager is the autosuggestion/completion campaign, not this pass |
| shift-right | forward-bigword | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| shift-left | backward-bigword | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| alt-b | prevd-or-backward-word | M-b / Ctrl-Left | word motion only; no directory-history action |
| alt-f | nextd-or-forward-word | M-f / Ctrl-Right | word motion only; no directory-history action |
| alt-right | nextd-or-forward-word | M-f / Ctrl-Right | word motion only; no directory-history action |
| e[1;9C | nextd-or-forward-word | M-f / Ctrl-Right | word motion only; no directory-history action |
| alt-left | prevd-or-backward-word | M-b / Ctrl-Left | word motion only; no directory-history action |
| e[1;9D | prevd-or-backward-word | M-b / Ctrl-Left | word motion only; no directory-history action |
| alt-up | history-token-search-backward | M-. / M-_ | pelt M-. walks lines and selects their last words, not fish token-search UI |
| alt-down | history-token-search-forward | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| e[1;9A | history-token-search-backward | M-. / M-_ | pelt M-. walks lines and selects their last words, not fish token-search UI |
| e[1;9B | history-token-search-forward | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| alt-. | history-token-search-backward | M-. / M-_ | pelt M-. walks lines and selects their last words, not fish token-search UI |
| alt-l | __fish_list_current_token | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| alt-o | __fish_preview_current_file | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| alt-w | __fish_whatis_current_token | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| ctrl-l | status test-terminal-feature scroll-content-up && commandline -f scrollback-push clear-screen | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| ctrl-c | clear-commandline | C-g | action or basic equivalent present; stty precedence applies |
| ctrl-u | backward-kill-line | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| ctrl-k | kill-line | C-k | action or basic equivalent present; stty precedence applies |
| ctrl-w | backward-kill-path-component | C-w / stty werase | pelt C-w is stty werase, blanks rather than path components |
| end | end-of-line | C-e / End | action or basic equivalent present; stty precedence applies |
| home | beginning-of-line | C-a / Home | action or basic equivalent present; stty precedence applies |
| alt-d | if test "$(commandline; printf .)" = \\n.; __fish_echo dirh; else; commandline -f kill-word; end | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| ctrl-d | delete-or-exit | C-d / Delete | action or basic equivalent present; stty precedence applies |
| alt-s | for cmd in sudo doas please run0; if command -q $cmd; fish_commandline_prepend $cmd; break; end; end | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| f1 | __fish_man_page | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| alt-h | __fish_man_page | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| alt-p | __fish_paginate | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| alt-# | __fish_toggle_comment_commandline | — | M-# comments and accepts, rather than toggling in place |
| alt-e | edit_command_buffer | — | use fc or vi v; no fish external-editor chord |
| alt-v | edit_command_buffer | — | use fc or vi v; no fish external-editor chord |
| (default printable) | self-insert | printable UTF-8 | action or basic equivalent present; stty precedence applies |
| space | self-insert expand-abbr | — | abbreviations/completion phase, not this pass |
| ; | self-insert expand-abbr | — | abbreviations/completion phase, not this pass |
| \| | self-insert expand-abbr | — | abbreviations/completion phase, not this pass |
| & | self-insert expand-abbr | — | abbreviations/completion phase, not this pass |
| > | self-insert expand-abbr | — | abbreviations/completion phase, not this pass |
| < | self-insert expand-abbr | — | abbreviations/completion phase, not this pass |
| shift-enter | commandline -i \\n (commandline --search-field >/dev/null && echo --search-field) expand-abbr | — | abbreviations/completion phase, not this pass |
| alt-enter | commandline -i \\n (commandline --search-field >/dev/null && echo --search-field) expand-abbr | — | abbreviations/completion phase, not this pass |
| ) | self-insert expand-abbr | — | abbreviations/completion phase, not this pass |
| ctrl-space | test -n "$(commandline)" && commandline -i " " (commandline --search-field >/dev/null && echo --search-field) | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| shift-space | commandline -i " " (commandline --search-field >/dev/null && echo --search-field) expand-abbr | — | abbreviations/completion phase, not this pass |
| enter | execute | Enter | action or basic equivalent present; stty precedence applies |
| ctrl-j | execute | Enter | action or basic equivalent present; stty precedence applies |
| ctrl-m | execute | Enter | action or basic equivalent present; stty precedence applies |
| ctrl-enter | execute | Enter | action or basic equivalent present; stty precedence applies |
| delete | delete-char | C-d / Delete | action or basic equivalent present; stty precedence applies |
| backspace | backward-delete-char | Backspace / C-h | action or basic equivalent present; stty precedence applies |
| shift-backspace | backward-delete-char | Backspace / C-h | action or basic equivalent present; stty precedence applies |
| ctrl-a | beginning-of-line | C-a / Home | action or basic equivalent present; stty precedence applies |
| ctrl-e | end-of-line | C-e / End | action or basic equivalent present; stty precedence applies |
| ctrl-h | backward-delete-char | Backspace / C-h | action or basic equivalent present; stty precedence applies |
| ctrl-p | up-or-search | C-p / Up | fish filtered history/pager is the autosuggestion/completion campaign, not this pass |
| ctrl-n | down-or-search | C-n / Down | fish filtered history/pager is the autosuggestion/completion campaign, not this pass |
| ctrl-f | forward-char | C-f / Right | action or basic equivalent present; stty precedence applies |
| ctrl-b | backward-char | C-b / Left | action or basic equivalent present; stty precedence applies |
| ctrl-t | transpose-chars | C-t | action or basic equivalent present; stty precedence applies |
| ctrl-g | cancel | C-g | action or basic equivalent present; stty precedence applies |
| ctrl-/ | undo | C-_ / C-x C-u | action or basic equivalent present; stty precedence applies |
| ctrl-_ | undo | C-_ / C-x C-u | action or basic equivalent present; stty precedence applies |
| ctrl-z | undo | C-_ / C-x C-u | pelt honours prompt suspend policy (ignored); undo is C-_ |
| ctrl-shift-z | redo | — | not this lane: undo only |
| alt-/ | redo | — | not this lane: undo only |
| alt-t | transpose-words | M-t | action or basic equivalent present; stty precedence applies |
| alt-u | upcase-word | M-u | action or basic equivalent present; stty precedence applies |
| alt-c | capitalize-word | M-c | action or basic equivalent present; stty precedence applies |
| alt-backspace | backward-kill-word | M-Backspace | action or basic equivalent present; stty precedence applies |
| ctrl-alt-h | backward-kill-word | M-Backspace | action or basic equivalent present; stty precedence applies |
| ctrl-backspace | backward-kill-token | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| alt-delete | kill-word | M-d | action or basic equivalent present; stty precedence applies |
| ctrl-delete | kill-token | — | not this lane: fish helper/token/completion UI action; no equivalent claimed |
| alt-< | beginning-of-buffer | C-a / Home | action or basic equivalent present; stty precedence applies |
| alt-> | end-of-buffer | C-e / End | action or basic equivalent present; stty precedence applies |
| ctrl-r | history-pager | — | fish filtered history/pager is the autosuggestion/completion campaign, not this pass |

## PAX delivery

No new PAX session was run in this pass. The framebuffer evidence is
[pax#162 at 09471da4](https://github.com/wolffe-lang/pax/pull/162),
`notes/px70/keys-hex.rows` and `tests/mpx5-yew`'s PS2_TABLE (lines 322–345).
Copies of the measured rows are in `notes/sh28-evidence/px70-*`.
The serial console passes every byte through; the host terminal chooses
its physical key encodings. F1 needs a px-owned pelt-session slot before
console sessions begin; F5 owns that fixture and the new-console runs.

The table distinguishes bytes actually present in the measured rows from
inferences about the same key families. A two-key ESC prefix is always an
alternative to an Alt chord; do not assume Alt+Shift works, since the
measured Alt+Shift+a emits nothing.

| new editor key | framebuffer delivery of required bytes | serial |
|---|---|---|
| M-. | ESC then `.`; direct Alt follows the measured left-Alt prefix family (alt-a/alt-z); dot chord not individually measured | yes |
| M-_ | ESC then `_`; direct shifted Alt chord not established | yes |
| M-y / M-t / M-u / M-l / M-c / M-r | ESC then letter; same measured left-Alt letter-prefix family; upper-case aliases can use sequential ESC then shifted letter | yes |
| C-t | control byte 14; numeric Alt-keypad entry can deliver byte 20 decimal; direct C-t not individually in px70 rows | yes |
| C-_ | control byte 1f; numeric entry can deliver 31 decimal; direct chord not individually measured | yes |
| C-x C-u / C-x C-x | bytes 18 15 / 18 18; numeric entry mechanism can deliver these control bytes; direct chords not individually measured | yes |
| M-< / M-> | sequential ESC then `<` / `>`; shifted Alt chords not established | yes |
| PageUp / PageDown | **measured** `off-9` = `1b 5b 35 7e`, `off-3` = `1b 5b 36 7e` | yes |
| M-# | sequential ESC then `#`; direct shifted Alt chord not established | yes |
| M-\ | ESC then backslash; direct punctuation chord not individually measured | yes |
| C-] / M-C-] | byte 1d / ESC then 1d; numeric entry can deliver 29 decimal; ctrl-alt-a demonstrates ESC plus a control byte | yes |
| M-0..9 / M-- | ESC then digit/minus; **measured** alt-1 = `1b 31`; other digits/minus are family inference, not Alt-keypad (which is numeric entry) | yes |
| C-g | **measured** Alt-keypad 7 produces `07`; direct C-g not individually in this table | yes |
| C-@ / C-Space / M-Space | **measured** Alt-keypad 0 produces `00`; ESC then space supplies M-Space; physical Ctrl-Space not separately measured | yes |
| quit flush (default C-\) | byte 1c via numeric entry 28; direct chord not separately in this table; a remapped printable quit can be typed directly | yes |
| vi `_` (spelling correction) | ordinary `_` in command mode; not an Alt chord | yes |

## Follow-on boundaries

- After wolf-lang#904 is in the pin, read argv[0], reject basename `sh`,
  and reconsider the recommended default-on policy. Until then opt-in is
  deliberate; `--posix` is a hard disable today.
- Autosuggestions must keep all shadow text out of the edit buffer. Keep
  readline Up/Down when friendly is off; fish-style filtered Up/Down and
  the history UI belong to that phase. PageUp/PageDown stay history ends.
- Expose VEOL, VEOL2, VREPRINT and VDISCARD through the terminal API before
  honoring remapped values. No `stty` subprocess at a prompt.
- The prompt's quit event is an editor flush, never a new signal sender.
- Preserve the ten-entry kill ring, grouped per-line undo and saved draft
  when adding suggestions/search. Suggestions are not edits or undo entries.

## Cost and regression coverage

85 new typed sessions pin these keys, their undo/kill-ring boundaries, live
listing, quit remaps and vi/search flushes. There are 375 active session
expectations and two named pending cases in the tree; the full gauntlet and
CI decide the final head. No pre-existing session expectation was changed.

The focused witness before the idle-accounting correction (kasumi, CPUs
12–15, the pinned container and
compiler pair above) loads 32,767 history entries and measures 100 M-.
responses after one warmup. It waits for the requested word, not just the
first output byte. Idle measurement begins only after a C-g acknowledgement,
so prompt initialization is not mistaken for idle allocation.

| tier | M-. median | p99 | idle 10 seconds |
|---|---:|---:|---|
| native | 0.020292 ms | 0.062855 ms | 0 context switches, RSS 2961 → 2961 pages |
| release | 0.016817 ms | 0.028302 ms | 0 context switches, RSS 2612 → 2612 pages |

These are live-process observations, not allocation-counter readings or a
universal latency guarantee. The external witness also verifies empty-history
bells, C-g cancellation/bells in CSI, SS3, C-x, numeric input, character search
and incremental search; script/pipe/POSIX/terminal gates; read-only listing,
remapped stty characters and mode restoration. Commands and raw results are
under `notes/sh28-evidence/`.

### Idle accounting isolation

A later full release run saw resident pages grow with zero context switches.
Repeated isolated measurements reproduced background transparent-huge-page
promotion: AnonHugePages rose by 4096 KiB while anonymous RSS rose by 236 KiB,
with unchanged CPU ticks and page-fault counters. This was not recorded as
pelt allocation. `notes/sh28-evidence/idle-accounting.txt` preserves the
original failure, component counters and the distinction between statm pages
and the kernel's kB fields.

The idle/cost fixture now disables THP only in its child before exec with
PR_SET_THP_DISABLE; the application and host setting are unchanged. It
verifies the disabled flag after exec, emits RSS/THP/CPU/fault counters and
requires exactly zero context switches plus unchanged anonymous and total
resident memory. Eight isolated release repetitions passed those stronger
guards. The earlier timing rows above retain their original uncontrolled-THP
provenance; full gauntlets are rerun with the isolated fixture.

## Suggestions and filtered history

With `friendly` and `suggest`, emacs mode draws the newest exact-prefix
history suffix, otherwise the first sorted file/command completion. It uses
SGR 90, resets with SGR 39, clears with EL (`ESC[K`) before edits, and restores
the cursor. It never wraps the suffix; the last cell is reserved. No shadow
is drawn for an empty line, mid-line cursor or `TERM=dumb`.

| keys | bytes | precedence with these options enabled |
|---|---|---|
| Right / Ctrl-F | `ESC[C`, `ESCOC`, `06` | at end accept whole shadow; otherwise ordinary character motion |
| End / Ctrl-E | `ESC[F`, `ESCOF`, `ESC[4~`, `ESC[8~`, `05` | at end accept whole shadow; otherwise move to end without accepting |
| Alt-F | `ESC f`, `ESC F` | at end accept next word; otherwise ordinary word motion |
| Ctrl-Right | `ESC[1;5C`, `ESC[1;3C` | at end accept next blank-delimited token; otherwise ordinary word motion |
| Tab | `09` | existing completion, never implicit suggestion acceptance |
| Up / Ctrl-P | `ESC[A`, `ESCOA`, `10` | with `histsearch`, previous exact-prefix history match |
| Down / Ctrl-N | `ESC[B`, `ESCOB`, `0e` | next prefix match, then restore original draft and cursor |
| PageUp / PageDown | `ESC[5~`, `ESC[6~` | unchanged oldest-history / saved-draft actions |
| Ctrl-R | `12` | with `histsearch`, filtered history pager; without it, existing incremental search |
| Enter in pager | `0d`, `0a` | accept selected line into editor, never execute it |
| Escape / Ctrl-G / Ctrl-C in pager | `1b`, `07`, stty intr | restore original draft and clear list; Ctrl-C deliberately differs from fish's clear-draft action |

Stty remappings still win before editor dispatch. Unaccepted shadow text is
absent from Enter, undo, every kill, Ctrl-C, Ctrl-U and Ctrl-L. Accepted text
is one undo group. `friendly_keys` does not gate `suggest` or `histsearch`.
Both new options default off at this pin; enable them explicitly. See
[FRIENDLY.md](FRIENDLY.md) for the future invocation-name-gated default.

Fish 4.9.3 was measured through a pty on kasumi, CPUs 4–7, using the same
Arch image and package versions recorded above. It emits SGR 90, not SGR 2,
indexed 244 or RGB grey, even with truecolour advertised. Its narrow shadow
uses an ellipsis and does not wrap in the measured case; pelt truncates
without an ellipsis. No prefix-of-a-word history fallback appeared in the
measurements. Raw reference bytes are in `notes/sh29/fish/`.

PAX evidence is px70's `notes/px70/final-validation.txt`, its SGR and palette
rows, and pax#162. Dim, indexed and RGB inputs are mapped to the framebuffer
console's 16-entry palette; serial passes terminal bytes through. This pass
runs no PAX session: the two exact-byte rows in `tests/session/PENDING.md`
await a px-owned session slot. It does not claim a PAX rendering result.


## Highlighted editing

`set -o highlight` enables display-only syntax colours independently;
`set -o friendly` enables it as part of friendly editing. All three standard
descriptors must be terminals. `set +o highlight` removes syntax and shadow
colours at that terminal without accepting, deleting or changing any text.
No editing key's meaning changes. Cursor motion, resize, completion lists,
the history pager, Ctrl-C and Enter reset the style before other output.

45 additional typed sessions cover colours and open syntax, Unicode,
resize with the cursor at the end and mid-line, completion rows, history
pager rows, shadow acceptance boundaries, undo, kill/yank, custom themes,
malformed themes and disable gates. The colour pass brought the tree to 488 sessions;
all 443 pre-colour expectations are unchanged. `tools/colour-witness` also
asserts raw SGR/reset bytes, persistent history, non-execution while typing,
idle counters and per-key cost. The compiled and checked selfchecks read the
actual buffer, both undo stores and the kill ring after coloured edits.

The PAX palette basis remains pax#162's sixteen entries. No new PAX result
is claimed; the exact framebuffer and serial input rows in
`tests/session/PENDING.md` wait for a px-owned harness slot.


## Words and completion

The words pass adds 64 independently asserted typed sessions, for 552
recorded sessions total. All earlier expectations stay unchanged.
`tools/words-witness` additionally checks raw reset boundaries, expanded
history, separate-shell abbreviation persistence, script isolation,
exclusive temporary-file failure, the explicit help probe/cache/deadline,
idle counters and per-key cost after an executed history event.

| key | bytes | friendly words action |
|---|---|---|
| Space | `20` | expand an unquoted command abbreviation; ordinary arguments stay literal |
| Enter | `0d` / `0a` | expand a command abbreviation, then `!!` / `!$`, then accept |
| Tab | `09` | complete a unique/common prefix or open the described pager; advance within it |
| Shift-Tab | `ESC[Z` | previous pager candidate |
| Up / Down | `ESC[A` / `ESC[B` | previous / next pager candidate |
| Left / Right | `ESC[D` / `ESC[C` | move across pager columns |
| PageUp / PageDown | `ESC[5~` / `ESC[6~` | move one pager page |
| Enter in pager | `0d` / `0a` | accept selection, never execute; with none, dismiss |
| Escape / Ctrl-G / Ctrl-C in pager | `1b` / `07` / `03` | dismiss and restore line/cursor |

Fish 4.9.3 was measured through fresh-HOME ptys, never its source.
Abbreviations expanded on both Space and Enter, and after command
separators; quoted spellings stayed literal. Undo after Space restored the
abbreviation plus its space. Six described choices occupied three columns
at 80 and 120 columns, one at 24 and 40: there is no fixed two-column rule.
Pelt deliberately shows selection only in the pager until Enter, whereas
fish's measured commandline includes the candidate during navigation.
Both accept without executing on that Enter. See `docs/FRIENDLY.md` for
persistence limits, help-probe effects and event quoting.

PAX remains pending the px-owned session slot. The exact framebuffer and
serial rows already in `tests/session/PENDING.md` are retained unchanged;
px70's sixteen-entry palette/cell evidence remains the rendering basis.
No PAX session or new key-delivery measurement is claimed here.


## Left and right prompt

The prompt pass adds no key binding. `prompt_friendly` is enabled by
`friendly` but leaves every explicitly assigned PS1 alone. The default is
`user@host path> `, with abbreviated HOME-relative directories, a nonzero
status and a root `#`. A `prompt_right` shell function supplies display-only
text once per primary prompt; its controls are escaped, width capped at a
third, and it is hidden below 40 columns or on overlap/wrap/pager rows.
Resize clears and redraws it without rerunning the function. Execution,
Ctrl-C, EOF and editor teardown clear it. None of its bytes are input.

32 new typed sessions bring the tree to 584 recorded sessions. All 552
older expectations remain unchanged. `tools/prompt-witness` checks raw
reset/cursor/storage laws, PS1 precedence, function isolation, width/resize,
script/POSIX/dumb gates, real subprocess cache deadlines, idle counters and
per-key cost. Pure checks use explicit completion times for the deadline
boundary. Fish 4.9.3's user/root, Unicode, 24/40/80/200-column raw recordings
are under `notes/sh32/oracle/`. PAX framebuffer and serial pending rows are
unchanged; no new PAX session or delivery claim is made.
