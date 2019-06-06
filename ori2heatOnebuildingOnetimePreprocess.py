import json
import time
from returnLLlocation import buildlocationdict
from BuildingName import buildnamedict
import sortpreprocessname
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


def jsonForHeat(read_file):#, write_file):
    dictrecodes = {}
    dictlist = {}
    #for item in buildlocationdict.items():
        
    #    dictlist[item[0]] = 0
    with open(read_file, "r") as r_file:
        datastore = json.load(r_file)
        for lineDic in datastore:
            try:
                dictrecodes[lineDic[u'building']] = dictrecodes.get(lineDic[u'building'], [])
                
                dictrecodes[lineDic[u'building']].append(lineDic[u'hmacaddress'])
            
                #dictlist[lineDic[u'building']] += 1
            except:
                pass
    
    for key in dictrecodes.keys():
        
        dictlist[key] = len(list(set(dictrecodes[key])))
    
    
    
    output = []

    #outputstring = "["
    for data in dictlist.items():
        try:
            loc = [float(x) for x in buildlocationdict[data[0]].split(', ')]
            output.append({'lat': loc[0], 'lng': loc[1], 'weight': max(3, data[1]), 'buildingname': buildnamedict[data[0]]})
            
            
        except:
            pass

    #outputstring = outputstring[:-2] + "]"
    #return(outputstring)
    return (output)





def generateTimeIntervalAndHeatData(before_time):
    filetime = sortpreprocessname.nameoreder[sortpreprocessname.nameoreder.index(before_time) - 1]
    #fetch_instance_in_time(from_time, to_time, to_file, n_process)
    return jsonForHeat('preprocess/'+filetime+'.json')
def main():
    print(generateTimeIntervalAndHeatData('052414'))

#Campus_Analytics_Hashed_201805-201806.json
if __name__ == "__main__":
    main()



