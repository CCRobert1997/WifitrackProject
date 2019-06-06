import json
import time
import calendar
from returnLLlocation import buildlocationdict
from BuildingName import buildnamedict
import sortpreprocessname
from DPlaplace import laplace


def searchbuiding(dictlist, attr, value):
    dictlen = len(dictlist)
    if (dictlen > 0):
        for p in range(dictlen):
            if dictlist[p][attr] == value:
                return p, 1 #exist in dictlist

    return 0, 0 #not exist in dictlist



def searchperson(dictlist, attr, value):
    dictlen = len(dictlist)
    if (dictlen > 0):
        for p in range(dictlen):
            if (value in dictlist[p][attr]):
                
                return p, 1 #exist in dictlist

    return 0, 0 #not exist in dictlist







def t2s(t):
    h,m,s = t.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


from collections import defaultdict








def macaddressInBuildingAtTime(before_time, building):
    filetime = sortpreprocessname.nameoreder[sortpreprocessname.nameoreder.index(before_time) - 1]
    time_interval_file = 'preprocess/'+filetime+'.json'
    
    visitor_ids = []
    with open(time_interval_file) as t_f:
        f_read = t_f.read()
        json_read = json.loads(f_read)
        for record in json_read:
            #print(record['hapmacaddress'])
            if (record['building'] == building):
                visitor_ids.append(record['hmacaddress'])
    visitor_ids_set = list(set(visitor_ids))
    nexttime = sortpreprocessname.nameoreder[sortpreprocessname.nameoreder.index(before_time) + 1]
    return (nexttime, visitor_ids_set)

def visitorIdsNextHour(before_time, visitor_ids_set):
    #visitor_ids_set = list(set(visitor_ids_set))
    filetime = sortpreprocessname.nameoreder[sortpreprocessname.nameoreder.index(before_time) - 1]
    time_interval_file = 'preprocess/'+filetime+'.json'
    resultdict = {}
    macaddredict = {}
    with open(time_interval_file) as v_f:
        vf_read = v_f.read()
        json_v_read = json.loads(vf_read)
        for record in json_v_read:
            if (record["hmacaddress"] in visitor_ids_set):
                #resultdict[record['building']] = resultdict.get(record['building'], 0) + 1
                macaddredict[record['building']] = macaddredict.get(record['building'], [])
                macaddredict[record['building']].append(record["hmacaddress"])
    
    for key in macaddredict.keys():
        try:
            
            macaddredict[key] = list(set(macaddredict[key]))
            resultdict[buildnamedict[key]] = len(macaddredict[key])
        
        except:
            print('key')
    resultdictitems = list(resultdict.items())
    dpresult = laplace([x[1] for x in resultdictitems], 2, 0.2)
    for item in range(len(resultdictitems)):
        resultdict[resultdictitems[item][0]] = int(max(0,dpresult[item]))

    nexttime = sortpreprocessname.nameoreder[sortpreprocessname.nameoreder.index(before_time) + 1]
    return (resultdict, macaddredict, nexttime)











def main():
    nexttime, visiId = macaddressInBuildingAtTime('052414', '115')
    
    resultdict, macaddredict, nexttime = visitorIdsNextHour(nexttime, visiId)
    print(resultdict)
    print(macaddredict)
    print(nexttime)
    #piechart('2018 05 03 15:00:00', '2018 05 03 15:03:00', 'time_in.json', "115", '01:00:00', 'visitorflowfile.json', 20)
    #piechart_from_file('time_in.json', 'visitorflowfile.json', "130")
#Campus_Analytics_Hashed_201805-201806.json
if __name__ == "__main__":
    main()



