import unittest

from xmllet import parse_file, register_filters, register_types
from tests.ndw import NDW_FILTERS, NDW_TYPES

class ParseTestCase(unittest.TestCase):

    def test_parse(self):
        # Expected output
        output = [
            {'longitude': 4.75460768, 'latitude': 52.34868},
            {'longitude': 4.629531, 'latitude': 52.27569},
            {'longitude': 4.482674, 'latitude': 51.91241},
            {'longitude': 4.77604437, 'latitude': 51.5860825},
            {'longitude': 5.07395363, 'latitude': 51.5895348},
            {'longitude': 5.07395363, 'latitude': 51.5895348},
            {'longitude': 4.701644, 'latitude': 52.2961464},
            {'longitude': 4.77674, 'latitude': 51.57619},
            {'longitude': 4.95742273, 'latitude': 52.6258163},
            {'longitude': 4.29176331, 'latitude': 52.07274},
            {'longitude': 4.27449942, 'latitude': 52.0853577},
            {'longitude': 5.0514493, 'latitude': 51.5378571},
            {'longitude': 4.769146, 'latitude': 52.6166039},
            {'longitude': 4.633512, 'latitude': 51.6980324},
            {'longitude': 6.19109631, 'latitude': 52.14135},
            {'longitude': 7.002804, 'latitude': 53.1637878},
            {'longitude': 4.353962, 'latitude': 52.04806},
            {'longitude': 4.663842, 'latitude': 52.34629},
            {'longitude': 4.64360476, 'latitude': 52.4784546},
            {'longitude': 5.09640837, 'latitude': 51.5690155},
            {'longitude': 4.25663328, 'latitude': 52.06138},
            {'longitude': 4.35340166, 'latitude': 52.048336},
            {'longitude': 4.78887749, 'latitude': 52.79873},
            {'longitude': 4.799059, 'latitude': 52.302494},
            {'longitude': 4.306135, 'latitude': 52.09128},
            {'longitude': 4.48012447, 'latitude': 51.9206429},
            {'longitude': 6.51473045, 'latitude': 53.2159653},
            {'longitude': 4.92245054, 'latitude': 52.20548},
            {'longitude': 4.75872326, 'latitude': 52.32754},
            {'longitude': 4.340979, 'latitude': 52.06586},
            {'longitude': 4.68217373, 'latitude': 51.66827},
            {'longitude': 4.7806673, 'latitude': 52.3362427},
            {'longitude': 4.36544847, 'latitude': 51.9458771},
            {'longitude': 6.41536236, 'latitude': 53.24465},
            {'longitude': 4.657545, 'latitude': 52.2883148},
            {'0': [{'longitude': 5.4489536, 'latitude': 52.216515}, {'longitude': 5.4138293, 'latitude': 52.14894}]},
            {'0': [{'longitude': 4.297021, 'latitude': 51.38703}, {'longitude': 4.3029838, 'latitude': 51.378857}]},
            {'0': [{'longitude': 5.1572504, 'latitude': 52.076183}, {'longitude': 5.1602974, 'latitude': 52.09327}]},
            {'0': [{'longitude': 4.933168, 'latitude': 52.33399}, {'longitude': 4.9280915, 'latitude': 52.332207}]},
            {'0': [{'longitude': 5.2399645, 'latitude': 52.23257}, {'longitude': 5.2520022, 'latitude': 52.26005}]},
            {'0': [{'longitude': 4.389556, 'latitude': 52.07162}, {'longitude': 4.389556, 'latitude': 52.07162}]},
            {'0': [{'longitude': 5.345984, 'latitude': 51.382183}, {'longitude': 5.2747517, 'latitude': 51.35166}]},
            {'0': [{'longitude': 5.5386395, 'latitude': 51.404964}, {'longitude': 5.5127754, 'latitude': 51.40502}]},
            {'0': [{'longitude': 5.422139, 'latitude': 51.49881}, {'longitude': 5.4259205, 'latitude': 51.49557}],
             '1': [{'longitude': 5.4259205, 'latitude': 51.49557}], '2': [{'longitude': 5.4269905, 'latitude': 51.489685}],
             '3': [{'longitude': 5.4269905, 'latitude': 51.489685}, {'longitude': 5.423607, 'latitude': 51.488148}]},
            {'0': [{'longitude': 6.0097075, 'latitude': 52.285454}, {'longitude': 6.009656, 'latitude': 52.29266}]},
            {'0': [{'longitude': 4.924597, 'latitude': 52.50347}, {'longitude': 4.8344965, 'latitude': 52.454983}]},
            {'0': [{'longitude': 4.1610355, 'latitude': 51.686012}, {'longitude': 4.167723, 'latitude': 51.6894}]},
            {'0': [{'longitude': 6.564277, 'latitude': 53.202244}, {'longitude': 6.5650306, 'latitude': 53.20155}]},
            {'0': [{'longitude': 6.7593417, 'latitude': 53.169422}, {'longitude': 6.7696977, 'latitude': 53.168644}]},
            {'0': [{'longitude': 4.3761425, 'latitude': 51.89476}], '1': [{'longitude': 4.370674, 'latitude': 51.904617}],
             '2': [{'longitude': 4.3706117, 'latitude': 51.903973}]},
            {'0': [{'longitude': 5.243503, 'latitude': 51.333164}, {'longitude': 5.321742, 'latitude': 51.37088}]},
            {'0': [{'longitude': 6.0075536, 'latitude': 52.328426}, {'longitude': 6.0103846, 'latitude': 52.33539}]},
            {'0': [{'longitude': 6.6036916, 'latitude': 53.21485}, {'longitude': 6.6087213, 'latitude': 53.216763}]},
            {'0': [{'longitude': 6.5764575, 'latitude': 53.206135}, {'longitude': 6.574999, 'latitude': 53.205864}]},
            {'0': [{'longitude': 6.4989605, 'latitude': 52.36356}, {'longitude': 6.494662, 'latitude': 52.36405}]},
            {'0': [{'longitude': 6.019993, 'latitude': 52.374516}, {'longitude': 6.021354, 'latitude': 52.372444}]},
            {'0': [{'longitude': 6.0084605, 'latitude': 52.301594}, {'longitude': 6.009203, 'latitude': 52.294415}]},
            {'0': [{'longitude': 5.438969, 'latitude': 51.493187}, {'longitude': 5.426444, 'latitude': 51.488743}]},
            {'0': [{'longitude': 6.0159516, 'latitude': 52.34651}, {'longitude': 6.0100684, 'latitude': 52.33561}]},
            {'0': [{'longitude': 6.0145373, 'latitude': 52.3942}, {'longitude': 6.0177293, 'latitude': 52.38178}]},
            {'0': [{'longitude': 5.367764, 'latitude': 52.40723}, {'longitude': 5.7268424, 'latitude': 52.838417}]},
            {'0': [{'longitude': 6.4303384, 'latitude': 52.36731}, {'longitude': 6.4361277, 'latitude': 52.367004}]},
            {'0': [{'longitude': 4.9243817, 'latitude': 52.330738}, {'longitude': 4.9294996, 'latitude': 52.332523}]},
            {'0': [{'longitude': 5.010569, 'latitude': 52.32883}, {'longitude': 4.9979753, 'latitude': 52.317883}]},
            {'0': [{'longitude': 5.2311845, 'latitude': 51.853916}, {'longitude': 5.221433, 'latitude': 51.865376}]},
            {'0': [{'longitude': 6.0120945, 'latitude': 52.33973}, {'longitude': 6.008875, 'latitude': 52.332825}]},
            {'0': [{'longitude': 4.1610355, 'latitude': 51.686012}, {'longitude': 4.167723, 'latitude': 51.6894}]},
            {'0': [{'longitude': 6.2296376, 'latitude': 51.944847}, {'longitude': 6.219461, 'latitude': 51.94487}]},
            {'0': [{'longitude': 5.2144794, 'latitude': 51.872726}, {'longitude': 5.228545, 'latitude': 51.85664}]},
            {'0': [{'longitude': 5.394706, 'latitude': 51.484398}, {'longitude': 5.40217, 'latitude': 51.478855}]},
            {'0': [{'longitude': 4.401292, 'latitude': 52.134453}, {'longitude': 4.3975606, 'latitude': 52.131763}]},
            {'0': [{'longitude': 6.5444407, 'latitude': 53.19793}, {'longitude': 6.5423994, 'latitude': 53.19727}]},
            {'0': [{'longitude': 6.563326, 'latitude': 53.19728}, {'longitude': 6.565599, 'latitude': 53.201565}]},
            {'0': [{'longitude': 6.444874, 'latitude': 52.36724}, {'longitude': 6.4419394, 'latitude': 52.367203}]},
            {'0': [{'longitude': 5.5108447, 'latitude': 51.385845}, {'longitude': 5.505671, 'latitude': 51.39797}]},
            ]

        # Setup
        fp = './actuele_statusberichten.xml'
        register_filters(NDW_FILTERS)
        register_types(NDW_TYPES)

        # Parse
        stream = parse_file(fp, 'situationRecord')
        self.assertListEqual(list(stream), output)


if __name__ == '__main__':
    unittest.main()
