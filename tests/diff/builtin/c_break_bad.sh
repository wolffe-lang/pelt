(for i in 1; do break 0; echo after; done; echo end) 2>/dev/null; echo "st=$?"
(for i in 1; do break x; echo after; done; echo end) 2>/dev/null; echo "st=$?"
