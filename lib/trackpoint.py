from datetime import datetime 
from dateutil import parser as dateparser
import itertools
import pyproj
# from tcx_parser import TCX

# Web: 
#    (Outdated: http://proj.maptools.org)
#    http://trac.osgeo.org/proj/
# Projection codes:
#    http://www.remotesensing.org/geotiff/proj_listQ

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


def validated_tracks(tcx=None):
    """Generator providing the trackpoint list for every track that has one"""
    assert hasattr(tcx,'trackpoint_lists'), "Must have a trackpoint_list iterable"
    # All tracks that have a trackpoint list
    for tpl in tcx.trackpoint_lists:
        tp_list = [tp for tp in itertools.ifilter(tp_check,tpl)]
        if tp_list:
            yield tp_list

class Track(object):
    def __init__(self,tcx=None):
        self.tracks = [[TrackPoint(tp) for tp in t ] for t in validated_tracks(tcx)]

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

    # def utm(self,zone=None):
    #     """Return the UTM coordinates of the point"""
    #     if zone is None:
    #         # Select the zone for this coordinate
    #         p = pyproj.Proj(proj='utm',ellps='WGS84',zone=zone)
        

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
