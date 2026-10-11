x=$(cat <<E
inner $(echo "nested )")
E
)
echo "$x"
