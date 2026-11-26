# Long expressions: 32 subtractions, left-associative; a long mixed
# chain of multiplication and remainder; parentheses sixteen deep.
echo $((100-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1))
echo $((2*3*5%7*11*13%17*19%23*29%31*37%41*43%47*53%59))
echo $(( ((((((((((((((((1+2)*2)-1)*2)-1)*2)-1)*2)-1)*2)-1)*2)-1)*2)-1)*2) ))
