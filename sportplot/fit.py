"""
Process data using fit files instead of gpx, using fitparse package
"""
import fitparse
import pandas as pd
import numpy as np


class GenFitFile(fitparse.FitFile):
    FIELDS = {}

    def __init__(self, fn):
        super(GenFitFile, self).__init__(fn)

        self.fn = fn
        self.fn_id = fn[:-4]

    def _get_first_entry(self, tag):
        return [f for f in self.messages(names=tag)][0].get_values()

    @property
    def sport(self):
        return self._get_first_entry('sport')

    @property
    def session(self):
        return self._get_first_entry('session')

    @property
    def activity(self):
        return self._get_first_entry('activity')

    def records_to_df(self):

        recs = self.get_messages(name='record')
        data = {key: [] for key in self.FIELDS.keys()}

        for i, rec in enumerate(recs):
            values = rec.get_values()

            for k, v in values.items():
                if k in self.FIELDS:
                    data[k].append(v)

            # If we're missing a value, pad it to the current position
            for _, v in data.items():
                if len(v) < i+1:
                    v.append(np.nan)

        df = pd.DataFrame(data)
        # rename to pretty fields
        df = df.rename(columns=self.FIELDS)
        return df


class CyclingFitFile(GenFitFile):

    FIELDS = {
        'position_lat': 'lat',
        'position_long': 'lon',
        'timestamp': 'timestamp',
        'distance': 'distance',
        'heart_rate': 'hr',
        'enhanced_altitude': 'e_alt',
        'altitude': 'alt',
        'enhanced_speed': 'e_speed',
    }

    def __init__(self, fn):
        super(CyclingFitFile, self).__init__(fn)


def main():
    fn = 'data/4132209152.fit'
    cff = CyclingFitFile(fn)
    df = cff.records_to_df()
    print(df.head())
    print(len(df))


if __name__ == '__main__':
    main()
