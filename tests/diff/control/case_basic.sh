for x in apple banana cherry; do
  case $x in
    a*) echo A;;
    *an*) echo AN;;
    *) echo other;;
  esac
done
