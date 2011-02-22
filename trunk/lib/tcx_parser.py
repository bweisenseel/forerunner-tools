from datetime import datetime 
from dateutil import parser as dateparser
# Web: 
#    (Outdated: http://proj.maptools.org)
#    http://trac.osgeo.org/proj/
# Projection codes:
#    http://www.remotesensing.org/geotiff/proj_listQ
import pyproj
import itertools

#  >>> from pyproj import Proj
#  >>> p = Proj(proj='utm',zone=10,ellps='WGS84') # use kwargs
#  >>> x,y = p(-120.108, 34.36116666)
#  >>> print 'x=%9.3f y=%11.3f' % (x,y)
#  >>> # do 3 cities at a time in a tuple (Fresno, LA, SF)
#  >>> lons = (-119.72,-118.40,-122.38)
#  >>> lats = (36.77, 33.93, 37.62 )
#  >>> x,y = p(lons, lats)
#  >>> lons, lats = p(x, y, inverse=True) # inverse transform
#  >>> p2 = Proj('+proj=utm +zone=10 +ellps=WGS84') # use proj4 string
#  >>> x,y = p2(-120.108, 34.36116666)

# >>> # projection 1: UTM zone 15, grs80 ellipse, NAD83 datum
# >>> # (defined by epsg code 26915)
# >>> p1 = pyproj.Proj(init='epsg:26915')
# >>> # projection 2: UTM zone 15, clrk66 ellipse, NAD27 datum
# >>> p2 = pyproj.Proj(init='epsg:26715')
# >>> # find x,y of Jefferson City, MO.
# >>> x1, y1 = p1(-92.199881,38.56694)
# >>> # transform this point to projection 2 coordinates.
# >>> x2, y2 = pyproj.transform(p1,p2,x1,y1)

# >>> # process 3 points at a time in a tuple
# >>> lats = (38.83,39.32,38.75) # Columbia, KC and StL Missouri
# >>> lons = (-92.22,-94.72,-90.37)
# >>> x1, y1 = p1(lons,lats)
# >>> x2, y2 = pyproj.transform(p1,p2,x1,y1)
# >>> xy = x1+y1
# >>> xy = x2+y2
# >>> lons, lats = p2(x2,y2,inverse=True)
# >>> xy = lons+lats

class TrackPoint(object):
    def __init__(self,track_point=None):
        if getattr(track_point,"Time",None):
            self.time=dateparser.parse(getattr(track_point,"Time"))
        else:
            self.time=None
        if (getattr(track_point,"AltitudeMeters",None) and 
            getattr(track_point,"Position",None) and 
            getattr(getattr(track_point,"Position"),"LatitudeDegrees",None) and
            getattr(getattr(track_point,"Position"),"LongitudeDegrees",None)):
            self.latitude=float(getattr(getattr(track_point,"Position"),"LatitudeDegrees"))
            self.longitude=float(getattr(getattr(track_point,"Position"),"LongitudeDegrees"))
            self.altitude=float(getattr(track_point,"AltitudeMeters"))
        else:
            self.latitude=None
            self.longitude=None
            self.altitude=None
        if (getattr(track_point,"HeartRateBpm",None) and 
            getattr(getattr(track_point,"HeartRateBpm"),"Value",None)):
            self.heart_rate=int(getattr(getattr(track_point,"HeartRateBpm"),"Value"))
        else:
            self.heart_rate=None

    @property
    def isotime(self):
        if self.time:
            return self.time.isoformat()
        else:
            return str(None)

    def utm(self,zone=None):
        """Return the UTM coordinates of the point"""
        if zone is None:
            # Select the zone for this coordinate
        p = pyproj.Proj(proj='utm',ellps='WGS84',zone=zone)
        

    def __repr__(self):
        pointStr = "Time: " + self.isotime
        pointStr += "\nLat: " + str(self.latitude) + " Deg"
        pointStr += "\nLon: " + str(self.longitude) + " Deg"
        pointStr += "\nAlt: " + str(self.altitude) + " Meters"
        pointStr += "\nHR: " + str(self.heart_rate) + " BPM"
        pointStr += "\n"
        return pointStr
        
    
# tp_keys=set("AltitudeMeters","Position","HeartRateBpm","Time")
# pos_keys=set("LatitudeDegrees","LongitudeDegrees")
# hr_keys=set("Value")
def tp_check(track_point=None):
    if track_point is None:
        return False
    # A track point must have a time
    if not hasattr(track_point, "Time"):
        return False
    # A trackpoint must have either have position in lat, lon, and alt or have a heart rate (it can have both)
    if not ( (hasattr(track_point, "Position") and hasattr(track_point, "Altitude") and 
              hasattr(track_point.Position, "LatitudeDegrees") and 
              hasattr(track_point.Position, "LongitudeDegrees")) or
             (hasattr(track_point, "HeartRateBpm") and 
              hasattr(track_point.HeartRateBpm, "Value"))):
        return False
    return True

# class TCXTrackList(list):
#     def __init__(self,tracklist=None):
#         self=tracklist
#     def __str__(self):
#         return  ("Contains " + str(len(self)) + "tracks\n" + 
#                  sum( "\tTrack " + str(i) + ": " + str(len(track)) + " points\n" 
#                       for (i,track) in enumerate(self)))
#     def __repr__(self):
#         return self.__str__
        
# class TCXLapList(list):
#     def __init__(self,laplist=None):
#         self=laplist
#     def __str__(self):
#         return ("Contains " + str(len(self)) + "laps\n" + 
#                 sum( "\tLap " + str(i) + ": " + str(TCXTrackList(tracklist=lap.track))
#                      for i,lap in enumerate(self)))

class TCX(object):
    def __init__(self,src=None):
        if src:
            self.parse_file(src=src)
        else:
            self._tcx=None

    def parse_file(self,src=None):
        from third_party.xml2obj import xml2obj
        if isinstance(src,file):
            srcfile=src
        elif isinstance(src,str):
            srcfile=open(src)
        self._tcx=xml2obj(srcfile)
        srcfile.close()
        return 

    @property
    def data(self):
        return self._tcx

    @property
    def num_acts(self):
        #N_acts=len(self.data.Activities)
        #N_act=[len(acts.Activity) for acts in tcx.data.Activities]
        return sum(len(acts.Activity) for acts in self.data.Activities)

    @property
    def num_valid_points(self):
        return sum(len(t) for t in self.validated_track)

    @property
    def lap_tracks(self):
        """Returns generator over the track lists for every lap that has one"""
        laplist = self.data.Activities[0].Activity[0].Lap
        return itertools.chain.from_iterable(itertools.imap(lambda x: x.Track,itertools.ifilter(lambda x: x.Track,laplist)))
        # for lap in itertools.ifilter(lambda x: x.Track,laplist):
        #     yield lap.Track

    @property
    def validated_tracks(self):
        """Generator providing the trackpoint list for every track that has one"""
        # All tracks that have a trackpoint list
        for t in self.lap_tracks:
            tp_list = [tp for tp in itertools.ifilter(tp_check,t.Trackpoint)]
            if tp_list:
                yield tp_list
                
    # @property
    # def validated_track(self):
        #laplist = self.data.Activities[0].Activity[0].Lap
        # track=[]
        # for lap in laplist:
        #     if lap.Track:
        #         for t in lap.Track:
        #             # Keep only trackpoints that have data we are interested in
        #             temp=filter(tp_check,t.Trackpoint)
        #             if temp:
        #                 track.append(temp)
        # return track

    @property
    def track_points(self):
        for tp_list in self.validated_tracks:
            for tp in tp_list:
                yield TrackPoint(tp)

    #@property 
    #def trackpoint(self):
    #    return [tp
    #            for tp in track.TrackPoint 
    #            for track in lap.Track 
    #            for lap in activity.Lap 
    #            for activity in activities.Activity
    #            for activities in self._tcx.activities]

    #@property
    #def lap(self):
    #    return TCXLapList(laplist=self._tcx.Activities.Activity.Lap)
    
    #@property
    #def start_time(self):
    #    return dateparser.parse(self.track[0].Trackpoint[0].Time)
