"""Own-process prctl probe; no host configuration write.
API: PR_SET_THP_DISABLE(2const), PR_GET_THP_DISABLE(2const), man-pages 6.19.
strace independently renders the numeric ABI values as their named commands.
"""
import ctypes
prctl=ctypes.CDLL(None,use_errno=True).prctl
prctl.argtypes=[ctypes.c_int]+[ctypes.c_ulong]*4
prctl.restype=ctypes.c_int
print('before',prctl(42,0,0,0,0),flush=True)
assert prctl(41,1,0,0,0)==0
print('after',prctl(42,0,0,0,0),flush=True)
assert prctl(42,0,0,0,0)==1
