import itertools

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
        return sum(len(acts.Activity) for acts in self.data.Activities)

    @property
    def lap_tracks(self):
        """Returns iterable over the track lists for every lap that has one"""
        laplist = self.data.Activities[0].Activity[0].Lap
        return itertools.chain.from_iterable(itertools.imap(lambda x: x.Track,itertools.ifilter(lambda x: x.Track,laplist)))
        # for lap in itertools.ifilter(lambda x: x.Track,laplist):
        #     yield lap.Track

    @property
    def trackpoint_lists(self):
        """Iterable providing the trackpoint list for every track that has one"""
        # All tracks that have a trackpoint list
        for t in self.lap_tracks:
            yield t.Trackpoint

