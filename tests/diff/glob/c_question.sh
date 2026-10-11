case a in ?) echo one;; esac
case ab in ?) echo no;; ??) echo two;; esac
case '' in ?) echo no;; *) echo empty-not-matched;; esac
