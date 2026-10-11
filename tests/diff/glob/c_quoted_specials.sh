case '*' in \*) echo star;; esac
case '?' in '?') echo q;; esac
case '[a]' in "[a]") echo bracket;; esac
case 'a\b' in a\\b) echo backslash;; esac
case ab in a\b) echo escaped-ordinary;; esac
