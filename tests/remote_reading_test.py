import unittest

from iec_api.models.remote_reading import PeriodConsumption, RemoteReadingResponse


class PeriodConsumptionTest(unittest.TestCase):
    def test_naive_interval_becomes_tz_aware(self):
        pc = PeriodConsumption.from_dict({"interval": "2023-07-20T10:00:00", "consumption": 1.0})
        self.assertIsNotNone(pc.interval.tzinfo)

    def test_aware_interval_stays_tz_aware(self):
        pc = PeriodConsumption.from_dict({"interval": "2023-07-20T10:00:00+00:00", "consumption": 1.0})
        self.assertIsNotNone(pc.interval.tzinfo)


class MeterReadingDataTest(unittest.TestCase):
    def _make_response_dict(self, intervals: list[str]) -> dict:
        return {
            "reportStatus": 0,
            "meterList": [
                {
                    "periodConsumptions": [{"interval": iv, "consumption": float(i)} for i, iv in enumerate(intervals)],
                }
            ],
        }

    def test_period_consumptions_sorted_after_deserialization(self):
        payload = self._make_response_dict(
            [
                "2023-07-20T12:00:00+00:00",
                "2023-07-20T08:00:00+00:00",
                "2023-07-20T16:00:00+00:00",
                "2023-07-20T04:00:00+00:00",
            ]
        )
        resp = RemoteReadingResponse.from_dict(payload)
        meter = resp.meter_list[0]
        intervals = [pc.interval for pc in meter.period_consumptions]
        self.assertEqual(intervals, sorted(intervals))

    def test_empty_period_consumptions(self):
        payload = self._make_response_dict([])
        resp = RemoteReadingResponse.from_dict(payload)
        self.assertEqual(resp.meter_list[0].period_consumptions, [])

    def test_mixed_naive_and_aware_intervals_do_not_raise(self):
        payload = self._make_response_dict(
            [
                "2023-07-20T12:00:00+00:00",
                "2023-07-20T08:00:00",
                "2023-07-20T16:00:00+03:00",
            ]
        )
        resp = RemoteReadingResponse.from_dict(payload)
        meter = resp.meter_list[0]
        intervals = [pc.interval for pc in meter.period_consumptions]
        self.assertEqual(intervals, sorted(intervals))
        for pc in meter.period_consumptions:
            self.assertIsNotNone(pc.interval.tzinfo)


if __name__ == "__main__":
    unittest.main()
