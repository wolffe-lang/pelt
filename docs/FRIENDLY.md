# Friendly editing

The friendly editor adds suggestions, filtered history and extra emacs keys
without changing the POSIX shell language. Enable it at a terminal prompt:

```sh
set -o friendly -o suggest -o histsearch
```

All three options are **off by default at the current compiler pin**.
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
Colour customization is planned through `PELT_COLORS`; it is not available
yet. SGR 90 is the portable default, including the PAX framebuffer palette.
