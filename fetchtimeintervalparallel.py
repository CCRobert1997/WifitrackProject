import json
import calendar, time
import argparse

#parser = argparse.ArgumentParser(description='findTimeCut')
#parser.add_argument('--first_line_of_file', dest='first_line_of_file', default="""{"changedon":"1525097343","hmacaddress":"eca2f24d5a4654ae1be9f334874263353db78a59f32de6ae957407e578ba9ca8","hapmacaddress":"9060fdd62016410b2305ad04cc8ce9c2165fe504a55b101fa2e7f44992fcf749","campus":"Parkville Indoor","building":"101","floor":"Ground","dot11status":"UNKNOWN","rssi":"-87","confidencefactor":"264.0"}""", help='path of the building_name object dataset')
#
#args = parser.parse_args()
#
#first_line_of_file = args.first_line_of_file
#print(first_line_of_file)
#lindic = json.loads(first_line_of_file)
#print(int(lindic["changedon"]))
#print(time.strftime("%d %b %Y %H:%M:%S", time.localtime(int(lindic["changedon"]))))
#
#
#
#import os

#path = 'splitdata'
#
#dict_start_time_each_file = {}
#
#files = os.listdir(path)
#files.sort()
#for name in files:
#    with open('splitdata/'+name) as f:
#        first_line = f.readline()
#        #print(name)
#        lindic = json.loads(first_line)
#        #print(int(lindic["changedon"]))
#        dict_start_time_each_file[name] = int(lindic["changedon"])
#        readableTime = time.strftime("%d %b %Y %H:%M:%S", time.localtime(int(lindic["changedon"])))
#
#        #print(readableTime)
#        #print(calendar.timegm(time.strptime(readableTime,'%d %b %Y %H:%M:%S')))
#        #print(first_line)
#
##with open('splitdata') as f:
##    first_line = f.readline()
#
##print(calendar.timegm(time.strptime('2000-01-01 00:00:00','%Y-%m-%d %H:%M:%S')))
##print(dict_start_time_each_file)
#import pickle
#dict_start_time_each_filehandler = open('dict_start_time_each_file.obj', 'wb')
#pickle.dump(dict_start_time_each_file, dict_start_time_each_filehandler)


#load_dict_start_time_each_file = pickle.load(open( 'dict_start_time_each_file.obj', "rb" ))
#print(load_dict_start_time_each_file)





import pickle
from multiprocessing import Process, Manager



def fetch_instance_in_interval(interval, findjsondata, sorted_keys, from_timestamp, to_timestamp):
    doc_i = interval[0]
    print(interval)
    while (doc_i <= interval[1]):
            
        with open('splitdata/'+sorted_keys[doc_i]) as f:
            lines = f.readlines()
            len_lines = len(lines)
            currentline = 0
            lindic = json.loads(lines[currentline])
            timestampcompare = int(lindic["changedon"])
            while (currentline<(len_lines-1)):
                    
                currentline+=1
                
                lindic = json.loads(lines[currentline])
                
                try:
                    timestampcompare = int(lindic["changedon"])
                    if ((timestampcompare <= to_timestamp) and (timestampcompare >= from_timestamp)):
                        findjsondata.append(lindic)
                except:
                    
                    print(lindic)
            
            
        doc_i+=1
#print(findjsondata)


def fetch_instance_in_time(from_time, to_time, to_file, n_process):
    data = []
    load_dict_start_time_each_file = pickle.load(open( 'dict_start_time_each_file.obj', "rb" ))
    timekeys = load_dict_start_time_each_file.keys()
    sorted_keys = sorted(timekeys)
    
    from_timestamp = int(time.mktime(time.strptime(from_time,'%Y %m %d %H:%M:%S'))) - 36000
    to_timestamp = int(time.mktime(time.strptime(to_time,'%Y %m %d %H:%M:%S'))) - 36000
    print(from_timestamp)
    print(to_timestamp)
    fileranges = []
    lookingforstarttime = True
    filerange = ['', '']
    for i in range(len(sorted_keys)):
        
        
        if (lookingforstarttime == False):
            print(load_dict_start_time_each_file[sorted_keys[i]])
            if to_timestamp < load_dict_start_time_each_file[sorted_keys[i]][1]:
            
                lookingforstarttime = True
                
                filerange[1] = i
                print(filerange)
                fileranges.append(filerange)
                filerange = ['', '']

        if ((from_timestamp > load_dict_start_time_each_file[sorted_keys[i]][2]) and (from_timestamp < load_dict_start_time_each_file[sorted_keys[i]][3])):
            if (lookingforstarttime):
                lookingforstarttime = False
                filerange[0] = i
            #            if (i+1 < len(sorted_keys)):
            #                if from_timestamp < load_dict_start_time_each_file[sorted_keys[i+1]][0]:
            #                    if (lookingforstarttime):
            #                        lookingforstarttime = False
            #
            #                        filerange[0] = i
    findjsonjoined = []
    manager = Manager()
    
    findjsondata = manager.list()
    rangeid = 0
    while (rangeid < len(fileranges)):
        processlist = []
        for i in range(n_process):
            if ((rangeid + i) < len(fileranges)):
                processlist.append(Process(target=fetch_instance_in_interval, args=(fileranges[i + rangeid], findjsondata, sorted_keys, from_timestamp, to_timestamp)))
        for p in processlist:
            p.start()
        for p in processlist:
            p.join()
        rangeid = rangeid + n_process

        
    print(len(findjsondata))
    output = sorted(findjsondata, key = lambda i: int(i['changedon']))
    with open(to_file, 'w') as outfile:
        json.dump(output, outfile)
    print("data loaded.")



def bruteforce_search(from_time, to_time):
    from_timestamp = int(time.mktime(time.strptime(from_time,'%Y %m %d %H:%M:%S')))
    to_timestamp = int(time.mktime(time.strptime(to_time,'%Y %m %d %H:%M:%S')))
    lenfind = 0
    with open('Campus_Analytics_Hashed_201805-201806.json') as f:
        for line in f:
            lineread = json.loads(line)
            try:
                timestampcompare = int(lineread["changedon"])
                if ((timestampcompare <= to_timestamp) and (timestampcompare >= from_timestamp)):
                    lenfind+=1
            except:
                print(lineread)
    return lenfind





def main():
    start = time.clock()
    fetch_instance_in_time('2018 05 01 09:00:00', '2018 05 01 09:10:00', 'demoshort.json', 10)
    #print(bruteforce_search('2018 05 01 09:00:00', '2018 05 01 10:10:00'))
    end = time.clock()
    print("\nexecution time: ",end-start)
#Campus_Analytics_Hashed_201805-201806.json
if __name__ == "__main__":
    main()




#from multiprocessing import Process
#
#def f(name):
#    print('hello', name)
#
#if __name__ == '__main__':
#    p = Process(target=f, args=('bob',))
#    p.start()
#    p.join()

#data = {}
#data['people'] = []
#data['people'].append({
#                      'name': 'Scott',
#                      'website': 'stackabuse.com',
#                      'from': 'Nebraska'
#                      })
#data['people'].append({
#                      'name': 'Larry',
#                      'website': 'google.com',
#                      'from': 'Michigan'
#                      })
#data['people'].append({
#                      'name': 'Tim',
#                      'website': 'apple.com',
#                      'from': 'Alabama'
#                      })
#
#with open('data.txt', 'w') as outfile:
#    json.dump(data, outfile)

