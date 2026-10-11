# A slash inside a bracket expression is an ordinary member in a `case`
# pattern and in ${x#pattern}: XCU 2.14.3's rule that a slash must be
# matched explicitly is for pathname expansion only (2.14.1, 2.6.2).
for w in /abs rel ./rel 'a\b' '$var/x' c:/dos; do
    case $w in
    [\\/$]* | ?:[\\/]*) printf '%s: absolute\n' "$w" ;;
    *[\\/]*) printf '%s: has a separator\n' "$w" ;;
    *) printf '%s: plain\n' "$w" ;;
    esac
done
case a/b in a[/]b) echo "bracket matches slash" ;; *) echo "no match" ;; esac
case a/b in a[!x]b) echo "negated bracket matches slash" ;; *) echo "no match" ;; esac
x=usr/local/bin
echo "${x#*[/]}" "${x%[/]*}" "${x##*[/]}" "${x%%[/]*}"
