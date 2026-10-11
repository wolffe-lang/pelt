trap 'echo got-pipe >&2' PIPE
kill -PIPE $$; echo after
