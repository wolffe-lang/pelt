# Friendly editing

The friendly editor adds abbreviations, described completion, history events,
syntax colours, suggestions, filtered history and extra emacs keys
without changing the POSIX shell language. Enable it at a terminal prompt:

```sh
set -o friendly -o suggest -o histsearch
```

These options are **off by default at the current compiler pin**.
`friendly` also enables `highlight`, `abbr`, `complete` and `histexpand`; `set -o highlight` works independently.
`friendly_keys` is on, but does nothing without `friendly`. Both stdin and
stderr must be terminals. Scripts, `-c`, pipes and `--posix` do not use
friendly editing. `TERM=dumb` uses the terminal's ordinary line discipline,
with no suggestions or pager. Vi mode retains its existing keys.

When the compiler pin can report the invocation name, the planned default
is to enable `friendly`, `suggest` and `histsearch` at interactive terminal
prompts, except when invoked as `sh`. That default is not enabled yet.

## Options

| option | effect |
|---|---|
| `friendly` | gates all friendly editing and the read-only `bindings` command |
| `friendly_keys` | enables the extra emacs keys, grouped undo and kill ring |
| `suggest` | draws a history, file or command suffix at the end of the line |
| `histsearch` | filters Up/Down by the typed prefix and gives Ctrl-R a history pager |
| `highlight` | colours shell syntax without changing the input |
| `abbr` | expands a command abbreviation on Space or Enter |
| `complete` | describes Tab candidates in a bounded selection pager |
| `histexpand` | expands `!!` and `!$` when you press Enter |

`set +o suggest` disables suggestions; `set +o histsearch` restores ordinary
history movement and readline-style Ctrl-R search. Turning off
`friendly_keys` does not disable suggestions or filtered history. Turning
off `friendly` disables them all. `set -o` lists their current settings
while friendly editing is active.

## Suggestions are not input

A suggestion appears in bright black (SGR 90) after the cursor. It is never
part of the command until accepted: **Enter runs only what you typed**.
Moving into the line removes it. Empty lines have no suggestion. The suffix
is truncated to the remaining screen width and never wraps.

The newest history line with the exact typed line as its prefix wins.
Otherwise the editor offers the first sorted file or command completion.
File names retain the completion engine's quoting. An ambiguous suggestion
is only a guess; Tab inserts a common prefix or offers alternatives.
A leading `!` can match history but is never completed as a command name.
Suggestions never expand `!!` or `!$`; the separate `histexpand` option
handles those only when Enter accepts a command.

At the end of the line:

- Right, End, Ctrl-E and Ctrl-F accept the whole suggestion.
- Alt-F accepts through the next word; Ctrl-Right accepts through the next
  blank-delimited token. For `alpha-beta/gamma`, Alt-F stops after `alpha`
  and Ctrl-Right after `gamma`.
- Acceptance is one undo group when `friendly_keys` is enabled. Unaccepted
  text never enters undo or the kill ring.

## History

Up and Ctrl-P search backward for the prefix you typed before starting the
history walk; Down and Ctrl-N search forward. Returning past the newest
match restores your draft and cursor. With an empty draft this is the usual
history walk. PageUp/PageDown retain their oldest-history/saved-draft keys.

Ctrl-R opens a short list below the prompt. Typing filters it by substring;
Up/Down select a match and Ctrl-R cycles. Enter copies the selection into
the editor **without running it**. Press Enter again to run it. Escape,
Ctrl-G or Ctrl-C closes the list and keeps the original draft. Ctrl-U clears
the search query; Backspace edits it. The list is cleared when it closes.

See [KEYS.md](KEYS.md) for byte encodings and terminal-character precedence.
SGR 90 remains the portable suggestion default, including the PAX framebuffer
palette. `PELT_COLORS` can change it while highlighting is active.


## Syntax colours

Use `set -o highlight`, or enable it with `set -o friendly`. It requires
stdin, stdout and stderr to be terminals. Scripts, `-c`, pipes, `--posix`
and `TERM=dumb` do not get highlighting. `set +o highlight` removes syntax
and suggestion colours at a fully attached terminal; suggestions can still
be shown as plain text. `set +o friendly` turns highlighting off too.

The default palette follows the measured fish 4.9.3 theme, not a green
command convention. A command that resolves is the default foreground;
a name that does not resolve is bright red immediately, even before you
finish typing. Arguments are cyan, comments red, quoted text yellow,
variables bright cyan and separators green. An open quote's delimiter is
bright red. Syntax errors show a coloured offending span and caret before
the ordinary diagnostic. An incomplete command still requests another line.

The display classifier does not expand variables, glob, execute a command
or run a substitution. Substitution bodies are one variable span rather
than recursively highlighted programs. Aliases are not expanded for display.
Command names use the completion engine's builtin/function/PATH census,
taken once per prompt. An explicit path is checked once per distinct
spelling during that prompt. Files created by another process may therefore
need a fresh prompt to change an already cached result.

Colours belong only to drawing. The input buffer, history, undo and kill
ring contain your text, never colour escapes. Full redraw, edits and resize
share the same renderer. Pager rows keep their own plain style, and the
suggestion's style is separate from the line's.

## PELT_COLORS

Set a colon-separated list of `role=value` entries. Values can be a named
16-colour foreground, `idx0` through `idx255`, or `#rrggbb`. Append one of
`+bold`, `+dim` or `+underline` if wanted. For example:

```sh
PELT_COLORS='command=green:argument=cyan:shadow=idx244:error=#ff5050'
```

Names are `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`,
`white`, and their bright forms prefixed with `br`. `normal` and `default`
restore the default foreground and attributes. The default shadow is
`brblack` (SGR 90), not indexed 244 or an RGB grey.

| role | default | fish variable with the equivalent purpose |
|---|---|---|
| `normal` | default | `fish_color_normal` |
| `command` | default | `fish_color_command` |
| `argument` (`param`) | cyan | `fish_color_param` |
| `reserved` | default | `fish_color_command` |
| `quote` | yellow | `fish_color_quote` |
| `quote_open` | brred | `fish_color_error` |
| `variable` | brcyan | `fish_color_operator` |
| `redirection` | cyan+bold | `fish_color_redirection` |
| `comment` | red | `fish_color_comment` |
| `operator` (`end`) | green | `fish_color_end` |
| `error` | brred | `fish_color_error` |
| `unknown` | brred | `fish_color_error` |
| `shadow` (`autosuggestion`) | brblack | `fish_color_autosuggestion` |

These are documented equivalents, not environment-variable aliases.
`TERM=linux` always uses the 16-colour fallback. Elsewhere,
`COLORTERM=truecolor` or `24bit` allows RGB, and a TERM containing
`256color` allows indexed colour. Unsupported colours are mapped to the
nearest standard palette entry; terminal-specific palette changes can alter
how that entry looks. Portable defaults need neither indexed nor RGB colour.

The whole value is checked before drawing. An unknown role or malformed
value produces a warning naming that entry at the next prompt and uses the
complete default palette, never a partially applied theme. Correct or unset
`PELT_COLORS` to stop the warning. Unset roles retain their defaults.

## Abbreviations

```sh
abbr add gs 'git status'
abbr add greet "echo 'hello there'"
abbr list
abbr erase gs
```

An abbreviation replaces a whole, unquoted first word of a command on
**Space or Enter**. Command position after a separator or pipe counts;
arguments, comments, quoted spellings and redirection targets do not.
It is an editor operation, not an alias or script-language expansion.
A literal-next Space does not trigger it. Empty and multi-word replacement
text is allowed. With friendly keys enabled, undo after Space restores the
typed abbreviation and its space; Ctrl-C discards the edit as usual.
`set +o abbr` disables expansion without disabling the other features.
The `abbr` command itself is available only at a friendly terminal prompt.

Records are saved under `$HOME/.pelt/abbr`, one `name<TAB>replacement` per
line. Add and erase write a private, exclusively created temporary file
and rename it over the old file only after a successful write and close.
A failed replacement leaves the old file intact. Separate shells read the
saved records at each prompt. Concurrent writers are last-writer-wins.
Malformed records are ignored; a later valid duplicate wins. Invalid UTF-8,
a non-regular file or a file over 64 KiB yields an empty table. The table
holds at most 256 names, names at most 128 bytes, replacements at most
4096 bytes. Control characters, including tabs/newlines, are rejected.
The file is data, never a script to execute.

## Described completion

With `complete` enabled, an ambiguous Tab opens a pager if no further
common prefix can be inserted. Builtins and reserved words have pelt's own
descriptions; file entries show their type and regular-file byte size.
Columns fit the current terminal width, with at most five candidate rows
and a range heading. At most 256 candidates are offered in one pager.

- Tab/Down advances; Shift-Tab/Up goes backward, wrapping at the ends.
- Left/Right moves across columns. PageUp/PageDown moves a page.
- Enter accepts a selected completion **without executing the command**.
  With no selection it just closes the pager. A second Enter runs the line.
- Escape, Ctrl-G or Ctrl-C dismisses it and preserves the line and cursor.
- An ordinary editing key closes the pager and is then handled normally.

Selection only changes a marker in the pager. It does not put a candidate,
a description or a style byte into the edit buffer. Rows use their own
plain style; resize and dismissal clear them and restore the command line.
`set +o complete` restores ordinary common-prefix/second-Tab listing.

For an option word starting with `-`, an **explicit Tab** may run the
literal command at the beginning of the line with `--help`. It does not
run shell aliases, functions or substitutions for that probe, and never
reads man pages. This is execution of that external program: its help
handler can have side effects. Merely highlighting a command or selecting
a candidate never runs it.

The probe has a 50 ms collection budget and a 32 KiB output cap. Late,
oversized or invalid UTF-8 output is discarded; the owned child is stopped
and reaped. Process startup, scheduling and cleanup can add wall time to
the collection deadline. Successful and unsuccessful results are cached
for the current prompt, for at most eight executable paths. No probe or
cache refresh occurs at an idle prompt. Only plain option declarations
are recognized; this is not programmable completion.

## Previous-command events

`histexpand` recognizes only `!!` (the previous command) and `!$` (its
last shell word, with its original quotes and escapes). It acts at Enter,
after abbreviation expansion, before normal shell parsing and expansion.
The expanded command is echoed, then executed, and that expanded text is
recorded in history. It never replaces the editable buffer, undo or kill
ring. It does not expand recursively inside substituted history text.

Single quotes, a backslash before `!`, and comments protect these events.
Double quotes permit them. Comments do not contribute a last word;
redirection operands do. Other event syntax, including `!23`, `!-2`,
`!prefix` and `^old^new^`, stays literal. With no previous command or word,
pelt prints its own one-line error and keeps the unexpanded line for
editing. Ctrl-C before Enter never expands anything.

Use `set +o histexpand` to leave both forms literal. These features require
`friendly` and the interactive editor; scripts, `-c`, pipes, `--posix` and
`TERM=dumb` remain unchanged. The current pin still defaults to opt-in.
