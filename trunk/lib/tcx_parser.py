from datetime import datetime 
from dateutil import parser as dateparser 

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
