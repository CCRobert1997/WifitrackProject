import json
from collections import Counter
from collections import defaultdict

def jsonForHeat(read_file,write_file):
    dictlist = Counter()

    with open(read_file,"r") as r_file:
        for line in r_file:
            lineDic = json.loads(line)
            try:
                building = lineDic["building"]
                dictlist[building] += 1
            except:
                pass

    print(dictlist)
    wf = open(write_file, "w")
    print(dictlist,file=wf)
    wf.close()


jsonForHeat("Campus_Analytics_Hashed_201805-201806.json","BuildingUse.txt")

