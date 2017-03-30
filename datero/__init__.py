# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


class Date:
    def __init__(self, year=1, month=1, day=1):
        self.year= 1
        self.month = 1
        self.day = 1
        self.set_date(year, month, day)

    def __add__(self, other):
        if other.__class__.__name__ != 'Day':
            # Why support only day: http://egloos.zum.com/mcchae/v/11203068
            raise NotImplemented
        days = self._ymd2ord(self.year, self.month, self.day) + getattr(other, 'day')

        year, month, day = self._toordinal2ymd(days)
        self.set_date(year, month, day)
        return self

    def __sub__(self, other):
        if other.__class__.__name__ != 'Day':
            # Why support only day: http://egloos.zum.com/mcchae/v/11203068
            raise NotImplemented

        days = self._ymd2ord(self.year, self.month, self.day) - getattr(other, 'day')
        year, month, day = self._toordinal2ymd(days)
        self.set_date(year, month, day)
        return self

    def __str__(self):
        return '<Date [{year}년 {month}월 {day}일]>'.format(year=self.year, month=self.month, day=self.day)

    @staticmethod
    def _days_in_month(year, month):
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return 29 if (is_leap_year(year) and month == 2) else days_in_month[month - 1]

    def _days_before_year(self, year):
        """
        # Best solution:
        y = year - 1
        return y*365 + y//4 - y//100 + y//400
        """
        days = 0
        for y in range(1, year):
            days += sum(self._days_in_month(y, month) for month in range(1, 13))
        return days

    def _days_before_month(self, year, month):
        return sum(self._days_in_month(year, m) for m in range(1, month))

    def _ymd2ord(self, year, month, day):
        # 특정일 전까지 흐른 날짜 수
        if not 1 <= month <= 12:
            raise ValueError('Invalid month, month must between 1 and 12. Not %d' % month)
        dim = self._days_in_month(year, month)
        if not 1 <= day <= dim:
            raise ValueError('Invalid day, day must between 1 and %d' % dim)
        return sum([self._days_before_year(year), self._days_before_month(year, month), day])

    def _toordinal2ymd(self, days):
        year = 0
        while days > 0:
            year += 1
            tmp = days
            days -= 366 if is_leap_year(year) else 365
            if days < 0:
                days = tmp
                break
        print('days: %d' % days)
        month = 0
        day = 0

        while days > 0:
            day = days
            month += 1
            days -= self._days_in_month(year, month)

        return year, month, day

    def set_date(self, year, month, day):
        if not (1 <= month <= 12):
            raise ValueError('Invalid month, month must between 1 and 12. Not %d' % month)
        self.month = month

        dim = self._days_in_month(year, month)
        if not (1 <= day <= dim):
            raise ValueError('Invalid day, day on %d/%d month must between 1 and %d. Not %d' % (
                year, month, dim, day
            ))
        self.day = day
        self.year = year
        return True

    def weekday(self):
        week_days = ['월', '화', '수', '목', '금', '토', '일', ]
        remainder = (self._ymd2ord(self.year, self.month, self.day) + 6) % 7
        # 1년 1월 1일은 월요일 1 % 7 == 1, 고로 week_days[0]이 월요일이 되게 하기 위해 6 더함
        return '{}요일'.format(week_days[remainder])


class Day:
    def __init__(self, day):
        self.day = day
