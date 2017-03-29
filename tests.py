import unittest
from datetime import datetime, timedelta
from datero import Date, Day
from random import randint


class TestDatero(unittest.TestCase):
    def test_weekday(self):
        date = {'year': 2017, 'month': 3, 'day': 28}
        real_date = datetime(**date)
        my_date = Date(**date)
        week_days = ['월', '화', '수', '목', '금', '토', '일']
        self.assertEqual(week_days[real_date.weekday()] + '요일', my_date.weekday())

    def test_calculation(self):
        cases = (
            ({'year': 2017, 'month': 1, 'day': 31}, 2, '+', 'simple month addition'),
            ({'year': 2017, 'month': 1, 'day': 1}, 2, '-', 'simple month subtraction'),
            ({'year': 2016, 'month': 12, 'day': 31}, 1, '+', 'simple year addition'),
            ({'year': 2016, 'month': 12, 'day': 31}, 60, '+', 'year and month addition'),
            ({'year': 2016, 'month': 2, 'day': 28}, 2, '+', 'leap year month addition'),
            ({'year': 2016, 'month': 2, 'day': 28}, 350, '+', 'leap year, month and year addition'),
            ({'year': randint(2014, 2015), 'month': randint(1, 12), 'day': 28}, randint(350, 800), '+', 'random test'),
            ({'year': randint(2014, 2015), 'month': randint(1, 12), 'day': 28}, randint(350, 800), '+', 'random test'),
            ({'year': randint(2014, 2015), 'month': randint(1, 12), 'day': 28}, randint(350, 800), '+', 'random test'),
        )
        for case in cases:
            date = case[0]
            added_day = case[1]
            my_date = Date(**date)
            real_date = datetime(**date)
            if case[2] == '+':
                real_date += timedelta(days=added_day)
                my_date += Day(added_day)
            elif case[2] == '-':
                real_date -= timedelta(days=added_day)
                my_date -= Day(added_day)
            self.assertEqual(real_date.day, my_date.day)
            self.assertEqual(real_date.month, my_date.month)
            self.assertEqual(real_date.year, my_date.year)
            print(case[3])

    def test_exception(self):
        date = {'year': 2016, 'month': 2, 'day': 30}
        try:
            Date(**date)
        except Exception as e:
            self.assertEqual('Invalid day, day must between 1 and 29', str(e))
        else:
            self.fail('ExpectedException not raised')


if __name__ == '__main__':
    unittest.main()
