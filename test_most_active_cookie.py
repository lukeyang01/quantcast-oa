import unittest

from most_active_cookie import parse_args, calc_cookie, verify_line

class TestArgs(unittest.TestCase):
    def test_correct_parse(self):
        args = ['most_active_cookie.py', 'spec_example.csv', '-d', '2022-12-08']
        fname, date_str = parse_args(args)
        self.assertEqual(fname, args[1])
        self.assertEqual(date_str, args[3])

    def test_arg_count(self):
        args = ['most_active_cookie.py', 'spec_example.csv', '-d', '2022-12-08', 'hello']
        with self.assertRaises(ValueError):
            parse_args(args)

    def test_wrong_tag(self):
        args = ['most_active_cookie.py', 'spec_example.csv', '-g', '2022-12-08']
        with self.assertRaises(ValueError):
            parse_args(args)

    def test_wrong_extension(self):
        args = ['most_active_cookie.py', 'spec_example.txt', '-d', '2022-12-08']
        with self.assertRaises(ValueError):
            parse_args(args)
    
    def test_wrong_date(self):
        args = ['most_active_cookie.py', 'spec_example.csv', '-d', '202f-12-08']
        with self.assertRaises(ValueError):
            parse_args(args)

        args = ['most_active_cookie.py', 'spec_example.csv', '-d', '08-12-2022']
        with self.assertRaises(ValueError):
            parse_args(args)
    
class TestCalc(unittest.TestCase):

    def test_spec(self):
        lines =     ['AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n',
                    'SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00\n',
                    '5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00\n',
                    'AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00\n',
                    'SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00\n',
                    '4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00\n',
                    'fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00\n',
                    '4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00\n']
        date_str = '2018-12-08'

        out = calc_cookie(lines, date_str)
        self.assertEqual(out, ['SAZuXPGUrfbcn5UA', '4sMM2LxV07bPJzwf', 'fbcn5UAVanZf6UtG'])

        date_str = '2018-12-09'
        out = calc_cookie(lines, date_str)
        self.assertEqual(out, ['AtY0laUfhglK3lC7',])

    def test_one(self):
        lines =     ['AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n',]
        date_str = '2018-12-09'

        out = calc_cookie(lines, date_str)
        self.assertEqual(out, ['AtY0laUfhglK3lC7'])

    def test_none(self):
        lines =     ['AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n',]
        date_str = '2018-12-08'

        out = calc_cookie(lines, date_str)
        self.assertEqual(out, ['No active cookies on 2018-12-08'])

    def test_sorted_order(self):
        lines =     ['AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n',
                    'SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00\n',
                    '5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00\n',
                    'AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00\n',
                    'SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00\n',
                    'SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00\n',
                    'SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00\n',
                    '4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00\n',
                    '4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00\n',
                    'fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00\n',
                    '4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00\n']
        date_str = '2018-12-08'

        out = calc_cookie(lines, date_str)
        self.assertEqual(out, ['SAZuXPGUrfbcn5UA'])

    def test_tied_output(self):
        lines =     ['AtY0laUfhglK3lC7,2018-12-08T14:19:00+00:00\n',
                    '5UAVanZf6UtGyKVS,2018-12-08T07:25:00+00:00\n',
                    'SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00\n',
                    '4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00\n',
                    'fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00\n']
        date_str = '2018-12-08'

        out = calc_cookie(lines, date_str)
        self.assertEqual(out, ['AtY0laUfhglK3lC7', '5UAVanZf6UtGyKVS', 'SAZuXPGUrfbcn5UA', '4sMM2LxV07bPJzwf', 'fbcn5UAVanZf6UtG'])

class TestVerifier(unittest.TestCase):
    def test_wrong_cookie(self):
        cookie = 'AtY0laUfhglK3lC-'
        date = '2018-12-08'
        time = '14:19:00+00:00'

        # Test special character
        with self.assertRaises(TypeError) as t:
            verify_line(cookie, date, time)
        self.assertTrue('cookie' in str(t.exception))
        # Test wrong length
        cookie = 'AtY0laUfhglK3lC'
        with self.assertRaises(TypeError) as t:
            verify_line(cookie, date, time)
        self.assertTrue('cookie' in str(t.exception))

    def test_wrong_date(self):
        cookie = 'AtY0laUfhglK3lCT'
        date = '201f-12-08'
        time = '14:19:00+00:00'

        # Test not digit
        with self.assertRaises(TypeError) as t:
            verify_line(cookie, date, time)
        self.assertTrue('date' in str(t.exception))
        # Test wrong length
        date = '20-12-2020'
        with self.assertRaises(TypeError) as t:
            verify_line(cookie, date, time)
        self.assertTrue('date' in str(t.exception))

    def test_wrong_time(self):
        cookie = 'AtY0laUfhglK3lCT'
        date = '2010-12-08'
        time = '1f:19:00+00:00'

        # Test not digit
        with self.assertRaises(TypeError) as t:
            verify_line(cookie, date, time)
        self.assertTrue('time' in str(t.exception))
        # Test wrong length
        time = '14:19:000+00:00'
        with self.assertRaises(TypeError) as t:
            verify_line(cookie, date, time)
        self.assertTrue('time' in str(t.exception))

if __name__ == '__main__':
    unittest.main()