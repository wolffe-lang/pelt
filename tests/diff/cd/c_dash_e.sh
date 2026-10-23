mkdir d; cd -P -e d; echo "st=$?"
(cd ..; mkdir gone; cd gone; rmdir ../gone; cd -P -e . 2>/dev/null; echo "missing=$?")
