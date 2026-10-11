case b in (a|b|c) echo paren;; esac
case b in a | b ) echo spaces;; esac
case x in
  (y) echo no ;;
  x) echo newline-form
esac
