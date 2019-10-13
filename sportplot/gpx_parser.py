from xml.etree import ElementTree as ET
from collections import namedtuple
from datetime import datetime
import pandas as pd


# Basic row for database, based on a single Garmin cycling gpx file.
TrackPoint = namedtuple("Point", "lat lon ele time temp hr")


def cvt_time(dt_str):
    """Convert time in Garmin GPX files to datatime"""
    # Note, these timestamps don't include time zones
    return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%fZ')


class GPXFile:
    """Basic GPX parser.
    :param fn: -- input gpx file
    """

    def __init__(self, fn):
        self.fn = fn
        self.exec_type = None
        self.start_time = None
        self.name = None
        self.points = []
        self.prefix = ''
        self._build()

    def get_df(self):
        """Return points as a DataFrame"""
        return pd.DataFrame(self.points)

    def _get_tag(self, tag):
        """Manages these prefix tags on the xml ET elements"""
        return self.prefix + tag

    def _build(self):
        """Actually parses the xml file."""
        xml = ET.parse(self.fn)
        root = xml.getroot()

        metadata = None
        trk = None
        self.prefix = root.tag[:-3]
        metadata = root.find(self._get_tag('metadata'))
        # print(metadata.find(self._get_tag('time')))
        trk = root.find(self._get_tag('trk'))

        trkseg = trk.find(self._get_tag('trkseg'))

        # I just wanted to flatten the track point and get the
        # fields that I am actually interested in.
        def walker(node):
            nonlocal data
            tags = {'lat': float,
                    'lon': float,
                    'ele': float,
                    'time': cvt_time,
                    'temp': float,
                    'hr': float}
            for tag in tags:
                if node.tag.find(tag) >= 0:
                    data[tag] = tags[tag](node.text)
            for child in node:
                walker(child)

        for trkpt in trkseg.findall(self._get_tag('trkpt')):
            data = {}
            data['lat'] = trkpt.attrib['lat']
            data['lon'] = trkpt.attrib['lon']
            walker(trkpt)
            self.points.append(TrackPoint(**data))


if __name__ == "__main__":
    sample_file = '/home/elliottb/garmin/4132209152_activity.gpx'
    gpx = GPXFile(sample_file)
