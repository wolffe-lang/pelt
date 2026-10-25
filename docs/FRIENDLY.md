# Friendly editing

The friendly editor adds syntax colours, suggestions, filtered history and extra emacs keys
without changing the POSIX shell language. Enable it at a terminal prompt:

```sh
set -o friendly -o suggest -o histsearch
```

These options are **off by default at the current compiler pin**.
`friendly` also enables `highlight`; `set -o highlight` works independently.
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
is only a guess; Tab still inserts a common prefix or lists alternatives.
A leading `!` can match history but is never completed as a command name.
This feature does not add `!!` or `!$` expansion.

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
