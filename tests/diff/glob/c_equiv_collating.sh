case a in [[=a=]]) echo equiv;; *) echo equiv-no;; esac
case a in [[.a.]]) echo coll;; *) echo coll-no;; esac
case - in [[.-.]]) echo coll-dash;; *) echo coll-dash-no;; esac
