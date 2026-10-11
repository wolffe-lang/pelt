( ( echo a ) ; { echo b; } ) | { ( cat ) ; } && { ! ( false ) ; } && echo c
