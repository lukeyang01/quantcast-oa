# quantcast-oa

With python installed, run with:
'python3 most_active_cookie.py [ INPUT_FILENAME ] -d [ DATE_STRING ]'

**SPECIFICATION:**
Given an input parameter date, the purpose of this program is to parse through a cookie log file in the following format:

```
cookie,timestamp
AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00
AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00
4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00
fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00
4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00
```

and return the cookie which is most active on that date.

For example, on ```2018-12-09``` would return:
```
AtY0laUfhglK3lC7
```

If multiple cookies meet that criteria, they are all returned.


**PARAMETERS**:

-INPUT_FILENAME: csv file to parse, (each line is in the format cookie,timestamp)

-DATE_STRING: date string in format 'YYYY-MM-DD'
