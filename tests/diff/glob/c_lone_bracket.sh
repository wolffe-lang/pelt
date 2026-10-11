case '[' in [) echo lone;; esac
case '[a' in [a) echo open-a;; esac
case a in [a) echo no;; *) echo not-a-class;; esac
