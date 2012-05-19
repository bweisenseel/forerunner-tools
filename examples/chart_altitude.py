#!/usr/bin/env python
import sys
from matplotlib import pyplot as plt
import matplotlib.dates as dates
from lib.tcx_parser import TCX, parse_time, parse_position
from lib.position import Position

# def format_date(x, pos=None):
#     datenum = dates.date2num(x)
#     return dates.num2date(datenum).strftime('%m-%d, %H:%M') #use FuncFormatter to format dates

def main(fname=None, outname=None):
    assert fname
    assert outname
    tcx = TCX(src=fname)
    time_position_sequence = [(parse_time(p), Position(*parse_position(p))) for p in tcx.position_points]

    fig1 = plt.figure()
    ax_locs = fig1.add_subplot(111)
    t = [dates.date2num(tp[0]) for tp in time_position_sequence]
    alt = [tp[1].altitude for tp in time_position_sequence]
    ax_locs.plot_date(t, alt, fmt='b-')
    fig1.savefig(outname)

if __name__ == '__main__':
    fname = sys.argv[1]
    outname = sys.argv[2]
    main(fname, outname)
