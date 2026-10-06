for x in 1 2 3; do
  if [ $x = 1 ]; then echo one
  elif [ $x = 2 ]; then echo two
  else echo other
  fi
done
