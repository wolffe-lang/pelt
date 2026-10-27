printf '%g %g %g %g %g\n' 0x1.8p+2 0X.8P-2 0x1.00000000000008p0 inf -nan
printf '[%+08G][% 8F][%-8e]\n' inf nan -inf
printf '%.1f %.2f %.20g\n' 0.15 2.675 1.234567890123456789
printf '%g %g\n' 1e9999 1e-9999
echo status:$?
printf '%g %g %g\n' 0x1p-1074 0x1p-1075 0x3p-1075
echo status:$?
printf '%f %f %g %g\n' ' 1.2' '1.2 ' 1e+ 'nan(payload)'
echo status:$?
