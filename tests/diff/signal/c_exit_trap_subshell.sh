trap 'echo parent' EXIT
( echo in-sub )
( trap 'echo child' EXIT; echo in-sub2 )
echo "$(trap 'echo cmdsub-exit' EXIT; echo body)"
echo end
