[ ~root = "$(cd ~root 2>/dev/null && pwd -P || echo ~root)" ] && case ~root in /*) echo absolute;; *) echo unexpanded;; esac
