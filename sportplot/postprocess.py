"""
Handles some post-processing that needs to happen for any real analysis
"""
import geopy.distance
import pandas as pd
import numpy as np
from collections import namedtuple

ActSummary = namedtuple('ActSummary',
                        "dist time ascent ave_hr")

METERS_TO_FEET = 3.28084


class ActData:
    def __init__(self, points):
        self.df = pd.DataFrame(points)

        self._process()

    def _process(self):

        dist = np.zeros(len(self.df))
        dt = np.zeros(len(self.df))

        last_geopt = None
        last_time = None
        for i, row in self.df.iterrows():
            geopt = row[['lat', 'lon']]
            if last_geopt is None:
                dist[i] = 0
                last_geopt = geopt

                dt[i] = 1e9
                last_time = row.time
                continue
            # Get the distance between two points
            dist[i] = geopy.distance.geodesic(last_geopt, geopt).miles
            last_geopt = geopt

            # Get the time between two points
            dt[i] = (row.time - last_time).seconds
            last_time = row.time

        self.df['time_s'] = \
            (self.df.time - self.df.time[0]) / np.timedelta64(1, 's')
        # Hack for plotting timedelta's see:
        # https://github.com/altair-viz/altair/issues/967
        self.df['time_from_start'] = pd.to_datetime('2019-01-01') + \
            + (self.df.time - self.df.time[0])

        self.df['ele'] = self.df['ele'] * METERS_TO_FEET
        self.df['distance'] = np.cumsum(dist)
        self.df['speed'] = dist / dt

    def get_summary_text(self):
        summ = self.get_summary()
        summ_text = {}
        summ_text['ascent'] = '{:.1f}'.format(summ.ascent)
        summ_text['dist'] = '{:.1f}'.format(summ.dist)
        summ_text['ave_hr'] = '{:.1f}'.format(summ.ave_hr)
        summ_text['time'] = summ.time.strftime('%H:%M:%S')
        return summ_text

    def get_summary(self):
        dist = np.max(self.df.distance)
        time = np.max(self.df.time)
        ave_hr = np.mean(self.df.hr)
        ascent = 0.0

        last_ele = None
        for i, ele in enumerate(self.df.ele):
            if i == 0:
                last_ele = ele
                continue

            d_ele = ele - last_ele
            last_ele = ele
            if d_ele > 0:
                ascent = ascent + d_ele

        return ActSummary(dist, time, ascent, ave_hr)


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    from sportplot.gpx_parser import GPXFile

    sample_file = '/home/elliottb/garmin/4132209152_activity.gpx'
    gpx = GPXFile(sample_file)

    act_data = ActData(gpx.points)

    act_data.df.distance.sum().plot()
    plt.show()
