echo 'echo stdin "$#"' | ../sh -cs 'echo string' 2>/dev/null; echo "st=$?"
