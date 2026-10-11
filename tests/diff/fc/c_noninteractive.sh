fc -l >/dev/null 2>&1; echo "st=$?" | sed 's/st=[1-9][0-9]*/st=fails/;s/st=0/st=ok-or-empty/'
echo survived
