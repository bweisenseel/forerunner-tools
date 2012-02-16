"""Module for the position class"""

from math import sqrt, hypot
from pyproj import Geod, Proj, transform
from itertools import izip

geodetic = Proj(proj='latlong', ellps='WGS84', datum='WGS84')
ecef = Proj(proj='geocent',  ellps='WGS84', datum='WGS84')

def is_numeric(num):
    return isinstance(num, (int, float))

class Position(object):
    __slots__ = ('latitude', 'longitude', 'altitude')

    geodesic = Geod(ellps='WGS84', datum='WGS84')

    def __init__(self, latitude, longitude, altitude):
        if altitude is None:
            altitude = 0.0
        if latitude is None or longitude is None:
            raise AttributeError("A {0} object requires latitude and longitude specified".format(self.__class__.__name__))
        if any(not is_numeric(attr) for attr in (latitude, longitude, altitude)):
            raise TypeError("The attributes of a {0} must be numeric".format(self.__class__.__name__))
        if (abs(latitude) > 90 ):
            raise ValueError("Latitudes must be between -90.0 and 90.0 degrees (inclusive)")
        if (abs(longitude) > 180 ):
            raise ValueError("Longitudes must be greater than -180 and less than 180.0 degrees (inclusive)")
        self.altitude = altitude
        self.longitude = -180 if longitude == 180 else longitude
        self.latitude = latitude

    @property
    def tuple(self):
        return (self.latitude, self.longitude, self.altitude)

    @property
    def ecef(self):
        return transform(geodetic, ecef, self.longitude, self.latitude, self.altitude)

    @property
    def radius(self):
        return sqrt(sum(direction ** 2 for direction in self.ecef))

    @classmethod
    def mean_position(cls, p1, p2, geodesic=None):
        if geodesic is None:
            geodesic = cls.geodesic
        lat1, lon1, alt1 = p1.tuple
        lat2, lon2, alt2 = p2.tuple
        mean_alt = (alt1 + alt2) * 0.5
        mean_lon, mean_lat = geodesic.npts(lon1, lat1, lon2, lat2, 1)[0]
        return cls(mean_lat, mean_lon, mean_alt)

    @classmethod
    def distances(cls, p_seq1, p_seq2, geodesic=None):
        """Computes the distances between the points in a pair of position sequences. It will terminate when the either sequence runs out."""
        if geodesic is None:
            geodesic = cls.geodesic
        for p1, p2 in izip(p_seq1, p_seq2):
            lat1, lon1, alt1 = p1.tuple
            lat2, lon2, alt2 = p2.tuple
            # This next is quite lame, and inaccurate, but probably good enough for my short distance uses
            mean_position = cls.mean_position(p1, p2, geodesic=geodesic)
            forward_azimuth, backward_azimuth, horizontal_distance = geodesic.inv(lon1, lat1, lon2, lat2)
            earth_radius = mean_position.radius
            horizontal_distance *=  1.0 + mean_position.altitude / earth_radius
            total_distance = hypot(horizontal_distance, alt1 - alt2)
            yield total_distance

    def distance(self, other):
        distance = [d for d in self.distances([self],[other])]
        return distance[0]

    def __str__(self):
        str(self.tuple)

    def __repr__(self):
        cls = self.__class__
        mod = cls.__module__
        name = cls.__name__
        return "{0}.{1}{2}".format(mod, name, self.tuple)
