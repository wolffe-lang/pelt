sleep 2 & p=$!
kill $p; wait
echo "--pipe"; jobs | wc -l
echo "--top"; jobs
echo "--top2"; jobs
sleep 2 & p=$!
kill $p; wait $p
echo "--top3"; jobs
sleep 0.1 &
sleep 0.5
echo "--top4"; jobs
echo "--top5"; jobs
