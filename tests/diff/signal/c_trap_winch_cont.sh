trap 'echo got-winch' WINCH
trap 'echo got-cont' CONT
kill -WINCH $$; kill -CONT $$; echo after
