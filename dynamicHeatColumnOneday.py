import json
import calendar, time
import argparse
from fetchtimeintervalparallel import fetch_instance_in_time
from BuildingName import buildnamedict
import os
import pickle
from multiprocessing import Process, Manager

def heatmapdate(date):
    pathdir = 'preprocess'
    list_of_files = os.listdir('preprocess') #list of files in the current directory
    list_of_files.sort()
    historydata = []
    
    for each_file in list_of_files:
        if each_file.startswith(date):  #since its all type str you can simply use startswith
            read_file = pathdir + '/' + each_file
            print(read_file)
            dictlist = {}
            macaddredict = {}
            with open(read_file, "r") as r_file:
                datastore = json.load(r_file)
                for lineDic in datastore:
                    try:
                        macaddredict[lineDic[u'building']] = macaddredict.get(lineDic[u'building'], [])
                        macaddredict[lineDic[u'building']].append(lineDic[u'hmacaddress'])
                        #dictlist[lineDic[u'building']] = dictlist.get(lineDic[u'building'],0)
                        #dictlist[lineDic[u'building']] += 1
                    
                    except:
                        pass
            for key in macaddredict.keys():
                try:
                    
                    dictlist[buildnamedict[key]] = len(list(set(macaddredict[key])))
                                                                          
                except:
                    pass
            top20dict = sorted(dictlist.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
            top20js = [{'y': v[1], 'label': v[0]} for v in top20dict[1:20]]
            historydata.append(top20js)
    return historydata


if __name__ == "__main__":
    print(heatmapdate('0519'))


