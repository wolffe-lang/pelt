echo $(case x in x) echo matched;; esac)
echo $(echo a # comment )
)
echo $(cat <<E
here )
E
)
echo "$(echo ')')" $(echo \))
