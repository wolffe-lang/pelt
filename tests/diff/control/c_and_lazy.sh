false && echo $(echo evaluated >&2) 2>&1
true && echo ran
i=0; false && : $((i=1)); echo $i
