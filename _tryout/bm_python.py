import time

__author__ = 'Peipei YI'

twitter = "D:\data\dataset\links-anon.txt"


def bm_io():
    """
    Python IO Benchmark
    """
    with open(twitter) as f:
        for line in f:
            pass


start = time.time()
bm_io()
end = time.time()
print end - start, 'seconds'
# 448.019999981 seconds for 36GB input file, about 80 MB/s.
