import sys
from datetime import datetime, timedelta, timezone

jst = timezone(timedelta(hours=9), "Asia/Tokyo")

print(sys.version)
print(datetime.now(jst).strftime("%Y/%m/%d %H:%M:%S"))

a = ""
if a is not None:
    print("Russia")

dicts = [{"a": 1}, {"b": 2}]
print(len(dicts))
