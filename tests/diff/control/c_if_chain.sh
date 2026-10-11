if false; then echo 1; elif false; then echo 2; elif true; then echo 3; else echo 4; fi
if false; true; then echo last-decides; fi
