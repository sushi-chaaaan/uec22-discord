import sys
from datetime import timezone, timedelta, datetime


jst = timezone(timedelta(hours=9), "Asia/Tokyo")

print(sys.version)
print(datetime.now(jst).strftime("%Y/%m/%d %H:%M:%S"))

a = ""
if a is not None:
    print("Russia")
