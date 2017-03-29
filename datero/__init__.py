from __future__ import unicode_literals


def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = self.set_month(month)
        self.day = self.set_day(day)

    def set_month(self, month):
        if not (1 <= month <= 12):
            raise ValueError('Invalid month, month must between 1 and 12. Not %d' % month)
        self.month = month
        return month

    def set_day(self, day):
        dim = self._days_in_month(self.year, self.month)
        if not (1 <= day <= dim):
            raise ValueError('Invalid day, day must between 1 and %d' % dim)
        self.day = day
        return day

    def __str__(self):
        return '<Date [{year}년 {month}월 {day}일]>'.format(year=self.year, month=self.month, day=self.day)

    def __add__(self, other):
        if other.__class__.__name__ != 'Day':
            # Why support only day: http://egloos.zum.com/mcchae/v/11203068
            raise NotImplemented

        days = self._ymd2ord(self.year, self.month, self.day) + getattr(other, 'day')
        year = 0
        while days > 0:
            year += 1
            tmp = days
            days -= 366 if is_leap_year(year) else 365
            if days < 0:
                days = tmp
                break
        month = 0
        day = 0

        while days > 0:
            month += 1
            day = days
            days -= self._days_in_month(year, month)

        self.year = year
        self.month = month
        self.day = day
        return self

    def __sub__(self, other):
        if other.__class__.__name__ != 'Day':
            # Why support only day: http://egloos.zum.com/mcchae/v/11203068
            raise NotImplemented

        days = self._ymd2ord(self.year, self.month, self.day) - getattr(other, 'day')
        year = 0
        while days > 0:
            year += 1
            tmp = days
            days -= 366 if is_leap_year(year) else 365
            if days < 0:
                days = tmp
                break
        month = 0
        day = 0

        while days > 0:
            month += 1
            day = days
            days -= self._days_in_month(year, month)

        self.year = year
        self.month = month
        self.day = day
        return self

    @staticmethod
    def _days_to_date():
        years = [year for year in range(1, 736616 // 365)]
        filter(lambda year: is_leap_year(year), years)

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

    def weekday(self):
        week_days = ['월', '화', '수', '목', '금', '토', '일', ]
        remainder = (self._ymd2ord(self.year, self.month, self.day) + 6) % 7
        # 1년 1월 1일은 월요일 1 % 7 == 1, 고로 week_days[0]이 월요일이 되게 하기 위해 6 더함
        return '{}요일'.format(week_days[remainder])


class TimeDelta:
    def __init__(self, timedelta):
        pass


class Day(TimeDelta):
    def __init__(self, day):
        super(Day, self).__init__(day)
        self.day = day
