# One expression per adjacent pair of binary precedence levels, each
# chosen so that exchanging the two levels changes the result, then
# the ternary against `||`, assignment against the ternary, and unary
# operators against binary ones.
echo $((1||0&&0)) $((1&&0|2)) $((1|2^3)) $((1^3&2)) $((1&2==2))
echo $((0==1<0)) $((1<1<<1)) $((1<<2+1)) $((1+2*3)) $((7-4%3))
echo $((0||1?2:3)) $((a=0?1:2)) $a $((-2*-3)) $((!0+1)) $((~1&3)) $((-2<<1))
