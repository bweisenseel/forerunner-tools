import lib.tcx_parser as tcx_parser
reload(tcx_parser)

src='/home/lorax/src/ant0_t3/results/20110213-2034/13.02.2011 100234.TCX'
tcx = tcx_parser.TCX(src=src)

# tcx_track=tcx.validated_track
tcx_track=[t for t in tcx.validated_tracks ]
# print tcx.num_valid_points

track_points=[tp for tp in tcx.track_points]

import itertools
import pylab as plt

lon=[]
lat=[]
for tp_list in tp_set:
    lon.extend(tp.longitude for tp in tp_list)
    lat.extend(tp.latitude for tp in tp_list)

plt.plot(lon,lat,'ro')
plt.show()

# start_time = 

# t=[]
# alt=[]
# hr=[]
# for j,track in enumerate(tracks):
#     t.append([])
#     alt.append([])
#     hr.append([])
#     # AltitudeMeters:u'70.3134766', 
#     # DistanceMeters:u'4.9896846', 
#     # Extensions:{TPX:{CadenceSensor:u'Footpod', xmlns:u'http://www.garmin.com/xmlschemas/ActivityExtension/v2'}}, 
#     # HeartRateBpm:
#     #     Value:u'143',
#     #     xsi_type:u'HeartRateInBeatsPerMinute_t', 
#     # Position:
#     #     LatitudeDegrees:u'42.4263496', 
#     #     LongitudeDegrees:u'-71.1702403', 
#     # SensorState:u'Absent', 
#     # Time:u'2010-10-30T18:49:59Z'
#     #
#     # for tstr,hrstr,latstr,lonstr,altstr in zip(track.Trackpoint[:].Time,
#     #                                            track.Trackpoint[:].HeartRateBpm.Value,
#     #                                            track.Trackpoint[:].Position.LatitudeDegrees,
#     #                                            track.Trackpoint[:].Position.LongitudeDegrees,
#     #                                            track.Trackpoint[:].Position.AltitudeMeters):
#     #     if (tstr and hrstr and latstr and lonstr and altstr):
#     #         print tstr, '\t', int(hrstr),'\t', float(latstr), '\t', float(lonstr), '\t', float(altstr)
#     for i,tp in enumerate(track.Trackpoint):
#         # AltitudeMeters:u'70.3134766', 
#         # DistanceMeters:u'4.9896846', 
#         # Extensions:{TPX:{CadenceSensor:u'Footpod', xmlns:u'http://www.garmin.com/xmlschemas/ActivityExtension/v2'}}, 
#         # HeartRateBpm:
#         #     Value:u'143',
#         #     xsi_type:u'HeartRateInBeatsPerMinute_t', 
#         # Position:
#         #     LatitudeDegrees:u'42.4263496', 
#         #     LongitudeDegrees:u'-71.1702403', 
#         # SensorState:u'Absent', 
#         # Time:u'2010-10-30T18:49:59Z'
#         if not ( tp.HeartRateBpm and tp.AltitudeMeters and tp.Position and tp.Time ):
#             continue
    
#         tstr   = tp.Time
#         hrstr  = tp.HeartRateBpm.Value
#         latstr = tp.Position.LatitudeDegrees
#         lonstr = tp.Position.LongitudeDegrees
#         altstr = tp.AltitudeMeters

#         #t[j].append(dateutil.parser.parse(tstr)-starttime)
#         t[j].append(dateutil.parser.parse(tstr))
#         alt[j].append(float(altstr))
#         hr[j].append(int(hrstr))

#         #pxsrint (dateutil.parser.parse(tstr)-starttime), '\t', int(hrstr),'\t', float(latstr), '\t', float(lonstr), '\t', float(altstr)
#         # if (tp.HeartRateBpm and tp.AltitudeMeters and tp.Position and tp.Time):
#         #     print tp.Time, '\t', int(tp.HeartRateBpm.Value),'\t', float(tp.Position.LatitudeDegrees), '\t', float(tp.Position.LongitudeDegrees), '\t', float(tp.AltitudeMeters)

# print "Found", len(tracks), "tracks"

import pylab
temp=[ (pylab.date2num(tau)-pylab.date2num(t[2][0]))*24.*60.  for tau in t[2] ]
#pylab.plot_date(t[2], alt[2], fmt='b-', tz=None, xdate=True, ydate=False)
#pylab.plot_date(t[2], hr[2], fmt='r-', tz=None, xdate=True, ydate=False)
pylab.subplot(211)
pylab.plot(temp, alt[2], '-')
pylab.ylabel("Altitude")
pylab.subplot(212)
pylab.plot(temp, hr[2], '-')
pylab.ylabel("Heart Rate")
pylab.xlabel("Minutes from start")
pylab.show()
