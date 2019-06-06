import json
import calendar, time
import argparse
from fetchtimeintervalparallel import fetch_instance_in_time


import pickle
from multiprocessing import Process, Manager



yearmonth = '2018 05 '
time = ''
for i in range(17):
    day = str(15 + i)
    if (len(day) < 2):
        day = '0' + day
    else:
        day = day
    time = yearmonth + day + ' '
    for j in range(24):
        hourstr = str(j)
        if (len(hourstr) < 2):
            hourstr = '0' + hourstr
        else:
            hourstr = hourstr

        timefrom = time + hourstr + ':' + '00:00'
        timeto = time + hourstr + ':' + '59:59'
        print(timefrom, timeto)
        filename = '05'+day+hourstr+'.json'
        fetch_instance_in_time(timefrom, timeto, 'preprocess2/' + filename, 30)



yearmonth = '2018 06 '
time = ''
for i in range(17):
    day = str(1 + i)
    if (len(day) < 2):
        day = '0' + day
    else:
        day = day
    time = yearmonth + day + ' '
    for j in range(24):
        hourstr = str(j)
        if (len(hourstr) < 2):
            hourstr = '0' + hourstr
        else:
            hourstr = hourstr
        timefrom = time + hourstr + ':' + '00:00'
        timeto = time + hourstr + ':' + '59:59'
        print(timefrom, timeto)
        filename = '06'+day+hourstr+'.json'
        fetch_instance_in_time(timefrom, timeto, 'preprocess2/' + filename, 30)
