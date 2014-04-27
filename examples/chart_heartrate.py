#!/usr/bin/env python
import sys
from itertools import tee, izip
from matplotlib import pyplot as plt
import matplotlib.dates as dates
from lib.tcx_parser import TCX, parse_time, parse_heart_rate

# def format_date(x, pos=None):
#     datenum = dates.date2num(x)
#     return dates.num2date(datenum).strftime('%m-%d, %H:%M') #use FuncFormatter to format dates

def pairwise(seq):
    a, b = tee(seq, 2)
    b.next()
    for e1, e2 in izip(a, b):
        yield e1, e2

def main(fname=None, outname=None):
    assert fname
    assert outname
    tcx = TCX(src=fname)
    time_hr_sequence = [(parse_time(p), parse_heart_rate(p)) for p in tcx.position_points]

    fig1 = plt.figure()
    ax = fig1.add_subplot(111)
    t = [dates.date2num(tp[0]) for tp in time_hr_sequence]
    hr = [tp[1] for tp in time_hr_sequence]
    ax.plot_date(t, hr, fmt='b-')
    ax.set_ylim(140, 200)
    fig1.savefig(outname)
    #fig1.show()
    #return ax

if __name__ == '__main__':
    fname = sys.argv[1]
    outname = sys.argv[2]
    main(fname, outname)
