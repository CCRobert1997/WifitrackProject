import json
import calendar, time
import argparse
import subprocess

parser = argparse.ArgumentParser(description='findTimeCut')
parser.add_argument('--first_line_of_file', dest='first_line_of_file', default="""{"changedon":"1525097343","hmacaddress":"eca2f24d5a4654ae1be9f334874263353db78a59f32de6ae957407e578ba9ca8","hapmacaddress":"9060fdd62016410b2305ad04cc8ce9c2165fe504a55b101fa2e7f44992fcf749","campus":"Parkville Indoor","building":"101","floor":"Ground","dot11status":"UNKNOWN","rssi":"-87","confidencefactor":"264.0"}""", help='path of the building_name object dataset')

args = parser.parse_args()

first_line_of_file = args.first_line_of_file
print(first_line_of_file)
lindic = json.loads(first_line_of_file)
print(int(lindic["changedon"]))
print(time.strftime("%d %b %Y %H:%M:%S", time.localtime(int(lindic["changedon"]))))



import os

path = 'splitdata'

dict_start_time_each_file = {}

files = os.listdir(path)
print(files)
files.sort()
print(files)
for name in files:
    with open('splitdata/'+name) as f:
        lines = f.readlines()
        #lindic = json.loads(lines[0])
        #print(json.loads(max(lines, key=lambda x:int(json.loads(x)["changedon"])))["changedon"])
        changedon_list = []
        for x in lines:
            try:
                changedon_list.append(int(json.loads(x)["changedon"]))
            except:
                pass
        
        #dict_start_time_each_file[name] = (int(lindic["changedon"]), max(changedon_list), min(changedon_list))
        dict_start_time_each_file[name] = (changedon_list[0], max(changedon_list), min(changedon_list), changedon_list[-1])
        print(dict_start_time_each_file[name])
        
        
        
#        first_line = f.readline()
#
#        lindic = json.loads(first_line)
#        lastline = subprocess.check_output(['tail', '-1', 'splitdata/'+name]).decode('UTF-8')
#
#        lastlindic = json.loads(lastline)
#
#        dict_start_time_each_file[name] = (int(lindic["changedon"]), int(lastlindic["changedon"]))
#
#        readableTime = time.strftime("%d %b %Y %H:%M:%S", time.localtime(int(lindic["changedon"])))

        #print(readableTime)
        #print(calendar.timegm(time.strptime(readableTime,'%d %b %Y %H:%M:%S')))
        #print(first_line)


#with open('splitdata') as f:
#    first_line = f.readline()

#print(calendar.timegm(time.strptime('2000-01-01 00:00:00','%Y-%m-%d %H:%M:%S')))
#print(dict_start_time_each_file)
import pickle
dict_start_time_each_filehandler = open('dict_start_time_each_file.obj', 'wb')
pickle.dump(dict_start_time_each_file, dict_start_time_each_filehandler)


load_dict_start_time_each_file = pickle.load(open( 'dict_start_time_each_file.obj', "rb" ))
print(load_dict_start_time_each_file)



