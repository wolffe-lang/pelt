# 300 jobs nobody waits for, between two whose ends say something (an exit
# status, a signal): each of the two still answers by its $! after the
# loops, and `jobs` lists every job (dash, black-box; pelt#39: a script
# reaps ended jobs as the next starts and keeps a one-process job's
# status in its slot). The signal's message is not compared: dash says it
# only when `wait` reaps the job itself, which a job ended long before
# never is (it was reaped as the next started)
sh -c 'exit 3' & first=$!
i=0
while [ $i -lt 150 ]; do env true & i=$((i+1)); done
sh -c 'kill -TERM $$' & mid=$!
while [ $i -lt 300 ]; do env true & i=$((i+1)); done
wait $first; echo "first: $?"
wait $mid 2>/dev/null; echo "mid: $?"
jobs > listed
echo "listed: $(wc -l < listed | tr -d ' ')"
