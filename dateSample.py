import datetime
import itertools

date_generator = (datetime.datetime.today() - datetime.timedelta(days=i) for i in itertools.count())
dates = list(itertools.islice(date_generator, 30))

for i in range(0, len(dates)):
    print dates[i]