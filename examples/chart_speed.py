#!/usr/bin/env python
import sys
from itertools import tee, izip
from matplotlib import pyplot as plt
import matplotlib.dates as dates
from lib.tcx_parser import TCX, parse_time, parse_position
from lib.position import Position

# def format_date(x, pos=None):
#     datenum = dates.date2num(x)
#     return dates.num2date(datenum).strftime('%m-%d, %H:%M') #use FuncFormatter to format dates

def pairwise(seq):
    a, b = tee(seq, 2)
    b.next()
    for e1, e2 in izip(a, b):
        yield e1, e2

def speed_miles(pair1, pair2):
    t1, p1 = pair1
    t2, p2 = pair2
    distance = p2.distance(p1) # meters
    miles = distance / 1609.344
    timedelta = t2 - t1
    hours = timedelta.total_seconds() / 3600
    return miles / hours

def main(fname=None, outname=None):
    assert fname
    assert outname
    tcx = TCX(src=fname)
    time_position_sequence = ((parse_time(p), Position(*parse_position(p))) for p in tcx.position_points)
    time_speed_sequence = [(p2[0], speed_miles(p1, p2)) for p1, p2 in pairwise(time_position_sequence) if p1[0] != p2[0]]

    fig1 = plt.figure()
    ax_locs = fig1.add_subplot(111)
    t = [dates.date2num(tp[0]) for tp in time_speed_sequence]
    speed = [tp[1] for tp in time_speed_sequence]
    ax_locs.plot_date(t, speed, fmt='b-')
    fig1.savefig(outname)

if __name__ == '__main__':
    fname = sys.argv[1]
    outname = sys.argv[2]
    main(fname, outname)
