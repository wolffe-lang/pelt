"""Generate complete reference inventories from measured bind outputs."""
from pathlib import Path
import re
import shlex
ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/'docs/KEYS.md'
text=DOC.read_text()
text=text.split('\n## Complete readline inventory')[0]
a=text.index('## Friendly additions');b=text.index('## Terminal characters',a)
text=text[:a]+'''## Friendly additions

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
| C-t | `14` | transpose characters, including combining clusters | transpose-chars | transpose-chars | at end, last two; negative count has no effect |
| M-t | `ESC t`, `ESC T` | transpose words | transpose-words | transpose-words | negative count has no effect in the measured bash session |
| M-u | `ESC u`, `ESC U` | upper-case word forward | upcase-word | upcase-word | ASCII case conversion, as tested in C locale; negative count works backward without moving point |
| M-l | `ESC l`, `ESC L` | lower-case word forward | downcase-word | file listing helper | readline action; not fish's listing helper |
| M-c | `ESC c`, `ESC C` | capitalise word forward | capitalize-word | capitalize-word | same word boundaries as M-f |
| C-_ / C-x C-u | `1f`, `18 15` | undo one edit group per press | undo | undo | consecutive insertion is one group; retained separately for each recalled line |
| M-r | `ESC r`, `ESC R` | revert current line to its original text | revert-line | unbound | recalled history restored; a fresh draft becomes empty |
| M-< / PageUp | `ESC <`, `ESC[5~` | oldest history entry | beginning-of-history | binding named beginning-of-history | readline's behavior; see fish observation below |
| M-> / PageDown | `ESC >`, `ESC[6~` | saved draft after newest entry | end-of-history | binding named end-of-history | readline's behavior |
| M-# | `ESC #` | prepend # and accept as comment | insert-comment | comment toggle without accepting | numeric argument toggles an existing leading # before accepting |
| M-\\ | `ESC 5c` | delete blanks/tabs on both sides of point | delete-horizontal-space | unbound | not a kill |
| C-] / M-C-] | `1d`, `ESC 1d` | find next / previous character | character-search / backward | unbound | C-g cancels the awaited character; negative count reverses direction |
| M-0..9 / M-- | `ESC 30..39`, `ESC 2d` | argument to next command | digit-argument | unbound | following digits may be plain or Alt; zero and negative arguments, bounded at 99,999 |
| C-g | `07`, `ESC 07`, `18 07` | abort multi-key command or search and ring | abort | cancel | resets numeric argument; search restores pre-search line |
| C-@ / C-Space / M-Space | `00`, `ESC 20` | set mark at point (or numbered position) | set-mark | space insertion | documented readline intent; bash's measured NUL non-effect is not copied |
| C-x C-x | `18 18` | exchange point and mark | exchange-point-and-mark | unbound | mark is a saved index; the measured M-Space mark is not shifted by later insertions |

A numeric argument to the first M-. chooses history word n (command word
is 0); negative n selects backwards from the last word with 0-based offset.
A negative argument on a repeated M-. reverses traversal. A redirection's
operand is a word; a one-word command yanks itself. Empty history rings.
This does not expand the shell language: `!!` and `!$` remain absent.

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

''' + text[b:]
text=text.replace('the installed bash 5.3 manual\'s Readline chapter and fish\'s bind manual.', "reference commands. Documentation was read with `info --subnodes '(bash) Bindable Readline Commands'` and `fish --no-config -c 'bind --help'`.")
text=text.replace('Bash\'s repeated M-. removes the\nlast insertion on running past the oldest entry. Both correct the initial\ncampaign guesses (R-sh28-2).','Bash\'s repeated M-. removes the last insertion on running past the oldest entry.')
text=text.replace('| quit | C-\\\\ | no effect | ignored (dash/bash interactive shells ignore QUIT) |','| quit | C-\\\\ | discard pending input and redraw empty edit line | honoured: pending input cleared; no signal/status/trap of its own |')
text=text.replace('then ignored quit/susp/start/stop','then quit flush, then ignored susp/start/stop')
text=text.replace('| C-\\\\, C-Z, C-Q, C-S | `1c`, `1a`, `11`, `13` by default | ignored while editing | terminal/editor dependent | cancel/undo/pager functions vary | quit/susp/start/stop: ignore at prompt; restored for jobs |','| C-\\\\ | `1c` or stty quit | clear pending input (updated in this pass) | terminal flush | not a default editing action | honoured, no editor signal |\n| C-Z, C-Q, C-S | `1a`, `11`, `13` by default | ignored while editing | terminal/editor dependent | undo/pager functions vary | susp/start/stop ignored at prompt; restored for jobs |')

baseline={
'accept-line':'Enter','backward-char':'C-b / Left','backward-delete-char':'Backspace / C-h','backward-kill-word':'M-Backspace','backward-word':'M-b / Ctrl-Left','beginning-of-line':'C-a / Home','clear-screen':'C-l','complete':'Tab','delete-char':'C-d / Delete','end-of-line':'C-e / End','forward-char':'C-f / Right','forward-word':'M-f / Ctrl-Right','kill-line':'C-k','kill-word':'M-d','next-history':'C-n / Down','previous-history':'C-p / Up','quoted-insert':'C-v / stty lnext','reverse-search-history':'C-r','self-insert':'printable UTF-8','unix-line-discard':'C-u / stty kill','unix-word-rubout':'C-w / stty werase','yank':'C-y'}
added={'abort':'C-g','capitalize-word':'M-c','character-search':'C-]','character-search-backward':'M-C-]','delete-horizontal-space':'M-\\','digit-argument':'M-digits / M--','downcase-word':'M-l','exchange-point-and-mark':'C-x C-x','insert-comment':'M-#','revert-line':'M-r','set-mark':'C-@ / M-Space','transpose-chars':'C-t','transpose-words':'M-t','undo':'C-_ / C-x C-u','upcase-word':'M-u','yank-last-arg':'M-. / M-_','yank-pop':'M-y','beginning-of-history':'M-< / PageUp','end-of-history':'M-> / PageDown'}
byaction={}
for line in (ROOT/'notes/sh28-evidence/logs/readline-bind-interactive.rows').read_text().splitlines():
    m=re.match(r'^"(.*)": ([a-z0-9-]+)$',line)
    if m:
        byaction.setdefault(m[2],[]).append(m[1])
canonical=set(byaction)-{'insert-last-argument'}

# Explicit reasons for every default action not implemented, not an implicit omission.
reasons={
'backward-kill-line':'C-x Rubout alias not added; C-u supplies this edit',
'bracketed-paste-begin':'paste protocol is not this lane; control-safe paste needs its own sessions',
'clear-display':'scrollback erase is not portable to the PAX target; C-l redraws the screen',
'display-shell-version':'version-display chord, not an edit; no inputrc interpreter',
'do-lowercase-version':'partial: M-uppercase aliases work; C-x uppercase dispatch is not added',
'edit-and-execute-command':'use fc (or vi v); no new C-x C-e launch path',
'execute-named-command':'requires named command dispatch/rebinding; read-only bindings only',
'forward-search-history':'forward incremental/history UI is the autosuggestion phase',
'non-incremental-forward-search-history':'vi ?/n/N and C-r cover this pass; extra emacs search not added',
'non-incremental-reverse-search-history':'vi / and C-r cover this pass; extra emacs search not added',
'operate-and-get-next':'default C-o overlaps discard; operation-and-next command not added',
'quoted-insert':'C-q alias conflicts with stty start; use C-v / stty lnext',
're-read-init-file':'no inputrc language; bindings is read-only',
'spell-correct-word':'no spelling oracle or dictionary subsystem in this pass',
'yank-nth-arg':'use M-n M-.; the M-C-y alias is not bound',
}
for name in canonical:
    if name not in baseline and name not in added and name not in reasons:
        if 'kbd-macro' in name: reasons[name]='keyboard macro recording/replay is not this lane'
        elif 'complet' in name or 'glob-' in name: reasons[name]='specialised completion chord not added; Tab and vi =/\\/* are available'
        elif name in {'history-expand-line','shell-expand-line','tilde-expand'}: reasons[name]='line/history expansion is not added; POSIX expansion still happens when accepted'
        elif name.startswith('shell-'): reasons[name]='shell-token editing family not added; ordinary word editing is available'
        else: raise SystemExit('missing verdict for '+name)

fish_rows=[]
for line in (ROOT/'notes/sh28-evidence/logs/fish-bind.rows').read_text().splitlines():
    if not line.startswith('bind '): continue
    words=shlex.split(line)
    fish_rows.append((words[2] or '(default printable)', ' '.join(words[3:])))
fish_alias={'delete-or-exit':'delete-char','prevd-or-backward-word':'backward-word','nextd-or-forward-word':'forward-word','up-or-search':'previous-history','down-or-search':'next-history','history-token-search-backward':'yank-last-arg','cancel':'abort','beginning-of-buffer':'beginning-of-line','end-of-buffer':'end-of-line','backward-kill-path-component':'unix-word-rubout','clear-commandline':'abort','execute':'accept-line','backward-delete-char':'backward-delete-char'}
fish_beyond=set()
for _,action in fish_rows:
    if action not in canonical and action not in fish_alias:
        fish_beyond.add(action)

def esc(s): return s.replace('|','\\|').replace('\n',' ')
text+='''\n## Complete readline inventory\n\n'''
text+=(f'`bind -p` reported **{len(byaction)} named bound actions**, **{len(canonical)}** after treating '
       '`insert-last-argument` as the alias of `yank-last-arg`. At the baseline pelt '
       f'covered **{len(baseline)}** of these actions, leaving **{len(canonical)-len(baseline)}** absent. '
       f'This pass adds **{len(added)}** distinct actions. These are action counts, not counts of '
       'key aliases. The original prediction counted too few of the full default inventory. '
       'Rows below retain every measured byte alias, including aliases pelt does not accept; '
       'the pelt column lists its own accepted keys. A shared action name is not a promise '
       'that every bash alias or every numeric corner is present.\n\n')
text+='| readline action | measured readline bytes | pelt key | fish comparison | stty / verdict |\n|---|---|---|---|---|\n'
for name,keys in sorted(byaction.items()):
    canon='yank-last-arg' if name=='insert-last-argument' else name
    if canon in baseline: key=baseline[canon]; verdict='present at baseline; aliases/terminal precedence as above'
    elif canon in added: key=added[canon];verdict='friendly addition; terminal precedence as above'
    else: key='—';verdict='not this lane: '+reasons[canon]
    fish='same named action' if any(action==canon for _,action in fish_rows) else 'see fish inventory'
    text+='| '+esc(name)+' | '+esc(' / '.join('`'+k+'`' for k in keys))+' | '+esc(key)+' | '+fish+' | '+esc(verdict)+' |\n'
text+='''\n## Complete fish default inventory\n\n'''
text+=(f'All **{len(fish_rows)}** measured default rows follow. Of the distinct command payloads, '
       f'**{len(fish_beyond)}** have no same-named readline action or mapped basic editor equivalent '
       '(up/down-or-search, buffer ends, cancel, execute, delete-or-exit, directory/word motion, '
       'path rubout and token-history insertion are mapped). This is a reproducible payload count, '
       'not a claim that fish has only that many extra behaviors: a conditional fish command '
       'payload may perform several operations.\n\n')
text+='| fish key | measured fish action / command payload | pelt equivalent | stty / verdict |\n|---|---|---|---|\n'
for key,action in fish_rows:
    canon=fish_alias.get(action,action)
    equivalent=baseline.get(canon,added.get(canon,'—'))
    if action in {'up-or-search','down-or-search','history-pager','pager-toggle-search','complete-and-search'}: verdict='fish filtered history/pager is the autosuggestion/completion campaign, not this pass'
    elif action in {'prevd-or-backward-word','nextd-or-forward-word'}: verdict='word motion only; no directory-history action'
    elif action=='backward-kill-path-component': verdict='pelt C-w is stty werase, blanks rather than path components'
    elif key=='ctrl-z': verdict='pelt honours prompt suspend policy (ignored); undo is C-_'
    elif action=='history-token-search-backward': verdict='pelt M-. walks lines and selects their last words, not fish token-search UI'
    elif action in {'beginning-of-history','end-of-history'}: verdict='pelt uses readline history ends; fish contextual observation above'
    elif equivalent!='—': verdict='action or basic equivalent present; stty precedence applies'
    elif 'expand-abbr' in action: verdict='abbreviations/completion phase, not this pass'
    elif 'clipboard' in action: verdict='no clipboard integration; PAX needs a portable policy first'
    elif 'edit_command_buffer' in action: verdict='use fc or vi v; no fish external-editor chord'
    elif 'toggle_comment' in action: verdict='M-# comments and accepts, rather than toggling in place'
    elif action=='redo': verdict='not this lane: undo only'
    else: verdict='not this lane: fish helper/token/completion UI action; no equivalent claimed'
    text+='| '+esc(key)+' | '+esc(action)+' | '+esc(equivalent)+' | '+esc(verdict)+' |\n'

text+='''\n## PAX delivery\n\nNo new PAX session was run in this pass. The framebuffer evidence is
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
| M-\\ | ESC then backslash; direct punctuation chord not individually measured | yes |
| C-] / M-C-] | byte 1d / ESC then 1d; numeric entry can deliver 29 decimal; ctrl-alt-a demonstrates ESC plus a control byte | yes |
| M-0..9 / M-- | ESC then digit/minus; **measured** alt-1 = `1b 31`; other digits/minus are family inference, not Alt-keypad (which is numeric entry) | yes |
| C-g | **measured** Alt-keypad 7 produces `07`; direct C-g not individually in this table | yes |
| C-@ / C-Space / M-Space | **measured** Alt-keypad 0 produces `00`; ESC then space supplies M-Space; physical Ctrl-Space not separately measured | yes |
| quit flush (default C-\\) | byte 1c via numeric entry 28; direct chord not separately in this table; a remapped printable quit can be typed directly | yes |
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
'''
DOC.write_text(text)
print(f'readline named={len(byaction)} canonical={len(canonical)} baseline={len(baseline)} missing={len(canonical)-len(baseline)} added={len(added)} fish_rows={len(fish_rows)} fish_extra_payloads={len(fish_beyond)}')
