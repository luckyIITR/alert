import calendar
from datetime import datetime

dd = datetime.now().date().weekday()
if calendar.day_name[dd] in ['Saturday', 'Sunday']:
    exit()

while True:
    print("hello world")