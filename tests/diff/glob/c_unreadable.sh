mkdir d; touch d/f; chmod 000 d
echo d/*; echo "st=$?"
chmod 755 d
