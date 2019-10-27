import numpy as np
import pandas as pd


def zones_from_threshold(lt):
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

def zones_from_max(hrmax):
    UPPER_LIMITS = [0.60, 0.70, 0.80, 0.9, 1.0]
    return [hrmax * limit for limit in UPPER_LIMITS]


def get_time_in_zone(df, lt):
    names = ['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4',
             'Zone 5a', 'Zone 5b', 'Zone 5c']
    hr = df.hr[1:]
    dt = df.time.diff() / np.timedelta64(1, 's')
    dt = dt[1:]
    zones = zones_from_threshold(lt)
    time_in_zone = np.zeros(7)
    time_in_zone[0] = np.sum(dt[hr <= zones[0]])
    time_in_zone[1] = np.sum(dt[(hr > zones[0]) & (hr <= zones[1])])
    time_in_zone[2] = np.sum(dt[(hr > zones[1]) & (hr <= zones[2])])
    time_in_zone[3] = np.sum(dt[(hr > zones[2]) & (hr <= zones[3])])
    time_in_zone[4] = np.sum(dt[hr > zones[4]])

    return pd.DataFrame({'zone': names[:-2], 'time': time_in_zone[:-2]})


def get_time_by_zones(df, zones):
    hr = df.hr[1:]
    dt = df.time.diff() / np.timedelta64(1, 's')
    dt = dt[1:]
    time_in_zones = np.zeros(len(zones))

    time_in_zones[0] = np.sum(dt[hr <= zones[0]])
    time_in_zones[-1] = np.sum(dt[hr > zones[-1]])
    for i in range(1, len(zones) - 1):
        time_in_zones[i] = np.sum(dt[(hr > zones[i]) & (hr <= zones[i+1])])

    return time_in_zones


def edwards_trimp(df, zones):
    time_in_zones = get_time_by_zones(df, zones)
    trimp = 0.0
    for i in range(len(time_in_zones)):
        trimp += i * time_in_zones[i]

    return trimp


def banister_trimp(df, max_hr, rest_hr, is_male=True):
    MALE_PARAMS = (0.64, 1.92)
    FEMALE_PARAMS = (0.86, 1.67)

    if is_male:
        params = MALE_PARAMS
    else:
        params = FEMALE_PARAMS

    dur = (df.time.max() - df.time.min()) / np.timedelta64(1, 'm')
    mean_hr = df.hr.mean()

    delta_hr = (mean_hr - rest_hr) / (max_hr - rest_hr)

    return dur * params[0] * delta_hr * np.exp(params[1] * delta_hr)
