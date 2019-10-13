import numpy as np
import pandas as pd


def calc_thresholds(lt):
    """
    Taken from https://www.trainingpeaks.com/blog/joe-friel-s-quick-guide-to-setting-zones/
    """
    # Upper limits for each zone as a ratio of latate threshold
    # Zones are:
    #     Zone 1: below 85%
    #     Zone 2: between 85% to 8%9
    #     Zone 3: Between 89% to 94
    #     Zone 4: between 94 to 99
    #     Zone 5a: between 100 to 102
    #     Zone 5b: between 102 and 106
    #     Zone 5c: above 106
    UPPER_LIMITS = [0.85, 0.89, 0.94, 0.99, 1.00, 1.02, 1.06]
    return [lt * limit for limit in UPPER_LIMITS]


def get_time_in_zone(df, lt):
    names = ['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4',
             'Zone 5a', 'Zone 5b', 'Zone 5c']
    hr = df.hr[1:]
    dt = df.time.diff() / np.timedelta64(1, 's')
    dt = dt[1:]
    zones = calc_thresholds(lt)
    time_in_zone = np.zeros(7)
    time_in_zone[0] = np.sum(dt[hr <= zones[0]])
    time_in_zone[1] = np.sum(dt[(hr > zones[0]) & (hr <= zones[1])])
    time_in_zone[2] = np.sum(dt[(hr > zones[1]) & (hr <= zones[2])])
    time_in_zone[3] = np.sum(dt[(hr > zones[2]) & (hr <= zones[3])])
    time_in_zone[4] = np.sum(dt[hr > zones[4]])

    return pd.DataFrame({'zone': names[:-2], 'time': time_in_zone[:-2]})
