echo 'echo from-env' > envf
ENV=$PWD/envf ../sh -c 'echo cmd'
