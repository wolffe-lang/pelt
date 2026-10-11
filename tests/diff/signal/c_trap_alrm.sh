trap 'echo got-alrm' ALRM
kill -ALRM $$; echo after
