from dateutil import parser as dateparser
import itertools

class TCX(object):
    def __init__(self, src=None):
        if src:
            self.parse_file(src=src)
        else:
            self._tcx=None

    def parse_file(self, src=None):
        from third_party.xml2obj import xml2obj
        if isinstance(src, file):
            srcfile=src
        elif isinstance(src, str):
            srcfile=open(src)
        self._tcx=xml2obj(srcfile)
        srcfile.close()
        return

    @property
    def data(self):
        return self._tcx

    @property
    def num_acts(self):
        return sum(len(acts.Activity) for acts in self.data.Activities)

    @property
    def lap_tracks(self):
        """Returns an iterable over the track lists for every lap that has one"""
        # Only grab the first activity
        laplist = self.data.Activities[0].Activity[0].Lap
        track_sequence = (lap.Track for lap in laplist if 'Track' in lap)
        # Return iterable over all tracks, independent of lap
        return itertools.chain.from_iterable(track_sequence)
        # non_empty_tracks = itertools.ifilter(lambda x: x.Track, laplist)
        # track_sequence = itertools.imap(lambda x: x.Track, non_empty_tracks)
        # return itertools.chain.from_iterable(track_sequence)

    @property
    def trackpoint_lists(self):
        """Iterable providing the trackpoint list for every track that has one"""
        # All tracks that have a trackpoint list
        for t in self.lap_tracks:
            if 'Trackpoint' in t:
                yield t.Trackpoint

    @property
    def validated_tracks(self):
        """Generator providing the trackpoint list for every track that has one"""
        assert hasattr(tcx, 'trackpoint_lists'), "Must have a trackpoint_list iterable"
        # All tracks that have a trackpoint list
        for tpl in self.trackpoint_lists:
            tp_list = [tp for tp in itertools.ifilter(tp_check, tpl)]
            if tp_list:
                yield tp_list

    @property
    def position_points(self):
        for tpl in self.trackpoint_lists:
            for tp in tpl:
                if hasattr(tp, "Time") and has_valid_position(tp):
                    yield tp

    @property
    def heart_rate_points(self):
        for tpl in self.trackpoint_lists:
            for tp in tpl:
                if hasattr(tp, "Time") and has_valid_heart_rate(tp):
                    yield tp


def parse_time(point):
    return dateparser.parse(point.Time)

def parse_position(point):
    latitude=float(point.Position.LatitudeDegrees)
    longitude=float(point.Position.LongitudeDegrees)
    altitude=float(point.AltitudeMeters)
    return latitude, longitude, altitude

def parse_heart_rate(point):
    return int(point.HeartRateBpm.Value)

def has_valid_position(point):
    return (hasattr(point, "Position") and hasattr(point, "Altitude") and
            hasattr(point.Position, "LatitudeDegrees") and
            hasattr(point.Position, "LongitudeDegrees"))

def has_valid_heart_rate(point):
    return hasattr(point, "HeartRateBpm") and hasattr(point.HeartRateBpm, "Value")

def tp_check(track_point=None):
    if point is None:
        return False
    # A track point must have a time
    if not hasattr(point, "Time"):
        return False
    # A trackpoint must have either have position in lat, lon, and alt or have a heart rate (it can have both)
    if not has_valid_position(point) and not has_valid_heart_rate(point):
        return False
    return True

