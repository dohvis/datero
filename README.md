# Datero
I wanna have a datetime. Datero = date+nero

```python
>>> from datero import Date, Day, Week
>>> today = Date(2017, 4, 1)
>>> someday = today + Day(1)
>>> print(someday.weekday())
"일요일"
>>> someday2 = today + Day(3)
>>> print(someday2)
<Date [2017년 4월 4일]>
>>> someday3 = today - Day(1)
>>> print(someday3)
<Date [2017년 3월 31일]>
```
