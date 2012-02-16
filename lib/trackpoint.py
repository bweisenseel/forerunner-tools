import itertools
#import pyproj
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



class HeartTrack(object):
    @classmethod
    def is_valid(cls, point):
        return hasattr(point, 'Time') and hasattr(point, 'HeartRateBpm')

    @classmethod
    def _extract_time_and_bpm(cls, point):
        return (parse_time(point), parse_heart_rate(point))

    # Create and maintain it as a time-sorted list
    def __init__(self, trackpoints):
        self._heart_rate = sorted(self._extract_time_and_bpm(point) for point in trackpoints if self.is_valid(point))

class Track(object):
    def __init__(self, tcx=None):
        self.tracks = [sorted(TrackPoint(tp) for tp in t if Trackpoint.is_valid(tp)) for t in validated_tracks(tcx)]

class TrackPoint(object):
    """ """
    @classmethod
    def is_valid(cls, point):
        return hasattr(point, 'Time') and hasattr(point, 'Position') and hasattr(point, 'AltitudeMeters')

    @classmethod
    def valid_points(cls, points):
        for p in points:
            if cls.is_valid(p):
                yield cls(p)

    def __init__(self, point):
        self.time = parse_time(point)
        self.latitude=float(track_point.Position.LatitudeDegrees)
        self.longitude=float(track_point.Position.LongitudeDegrees)
        self.altitude=float(track_point.AltitudeMeters)

    @property
    def isotime(self):
        if self.time:
            return self.time.isoformat()
        return str(None)

    def _key(self):
        return (self.time, (self.latitude, self.longitude, self.altitude))

    def __hash__(self):
        return hash(self._key)

    def __eq__(self, other):
        for attr in ('time', 'latitude', 'longitude', 'altitude'):
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.time < other.time

    def __le__(self, other):
        return self.time <= other.time

    def __gt__(self, other):
        return self.time > other.time

    def __ge__(self, other):
        return self.time >= other.time

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
