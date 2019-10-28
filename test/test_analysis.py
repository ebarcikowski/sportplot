from unittest import TestCase
from sportplot import analysis
from sportplot import fit
import fitparse


class TestTrimp(TestCase):

    data_fn = 'data/4141693581.fit'
    fit_file = fit.CyclingFitFile(data_fn)
    records = fit_file.records_to_df()

    def test_edwards_trimp(self):
        zones = analysis.zones_from_threshold(160)
        trimp = analysis.edwards_trimp(self.records, zones)

        print(trimp)

        self.assertGreaterEqual(trimp, 0)

    def test_banister_trimp(self):
        trimp = analysis.banister_trimp(self.records, 172, 50, True)

       self.assertGreaterEqual(trimp, 0)
