import json
import calendar, time
import argparse
from fetchtimeintervalparallel import fetch_instance_in_time
from BuildingName import buildnamedict
import os
import pickle
from multiprocessing import Process, Manager

import json
from collections import Counter
from collections import defaultdict


def timeline(date, building, floor):
    pathdir = 'preprocess'
    list_of_files = os.listdir('preprocess') #list of files in the current directory
    list_of_files.sort()
    historydata = []
    TimeCon = Counter()
    user_add = defaultdict(list)
    User=[]
    InBuilding=[]
    PopuTime=[]
    date_start = '2018 ' + date[:2] + ' ' + date[2:] + ' 00:00:00'
    PreTime = int(time.mktime(time.strptime(date_start,'%Y %m %d %H:%M:%S')))
    recordstart =(PreTime+7200)*1000
    GetEveryThree=[]
    for each_file in list_of_files:
        if each_file.startswith(date):  #since its all type str you can simply use startswith
            read_file = pathdir + '/' + each_file
            print(read_file)
            dictlist = {}
            macaddredict = {}
            with open(read_file, "r") as r_file:
                datastore = json.load(r_file)
                for lineDic in datastore:
                    if lineDic["building"] == building and lineDic["floor"] == floor:
                        timeOfline = lineDic["changedon"]
                        t = int(timeOfline)+7200
                        mac = lineDic["hmacaddress"]
                        if mac not in InBuilding:
                            InBuilding.append(mac)
                        else:
                            CopyUser = User
                            for i in range(len(User)):
                                if User[i][1] == mac:
                                    del CopyUser[i]
                                    break
                            User = CopyUser
                        User.append([t,mac])
                        while User[0][0] < int(lineDic["changedon"]):
                            if User[0][1] in InBuilding:
                                InBuilding.remove(User[0][1])
                            del User[0]
                        if PreTime != timeOfline:
                            PreTime = timeOfline
                            # suit GMT
                            PopuTime.append([(int(PreTime)+36000)*1000,len(InBuilding)])
        
                    else:
                        if lineDic["hmacaddress"] in InBuilding:
                            InBuilding.remove(lineDic["hmacaddress"])
    i=0
    for record in PopuTime:
        # if i%5 == 0 and record[0] > recordstart:
        if record[0] > recordstart:
            GetEveryThree.append(record)
    return GetEveryThree
            

if __name__ == "__main__":
    timeline('0519', "115","Ground")


