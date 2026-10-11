cat <<-E
	one
		two
  three (spaces kept)
	E
x='	tab-from-expansion'
cat <<-E
	$x
	E
