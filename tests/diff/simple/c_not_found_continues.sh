nonexistent-command-xyz 2>/dev/null; echo "st=$?"
nonexistent-command-xyz 2>&1 | wc -l | tr -d ' '
