for c in a Z 5 ' ' . _; do
  case $c in [[:alpha:]]) echo alpha;; [[:digit:]]) echo digit;; [[:space:]]) echo space;; [[:punct:]]) echo punct;; *) echo other;; esac
done
case aB3 in [[:lower:]][[:upper:]][[:alnum:]]) echo three;; esac
case f in [[:xdigit:]]) echo xdigit;; esac
case a in [![:digit:]]) echo not-digit;; esac
case 5 in [[:alpha:][:digit:]]) echo two-classes;; esac
