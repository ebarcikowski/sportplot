"""
Handles some post-processing that needs to happen for any real analysis
"""
import geopy.distance
import pandas as pd
import numpy as np


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

        self.df['distance'] = np.cumsum(dist)
        self.df['speed'] = dist / dt

if __name__ == '__main__':
    from matplotlib import pyplot as plt
    from sportplot.gpx_parser import GPXFile

    sample_file = '/home/elliottb/garmin/4132209152_activity.gpx'
    gpx = GPXFile(sample_file)


    act_data = ActData(gpx.points)

    act_data.df.distance.sum().plot()
    plt.show()
