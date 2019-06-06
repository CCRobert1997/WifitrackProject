from flask import Flask, render_template,request
from ori2heatOnebuildingOnetimePreprocess import generateTimeIntervalAndHeatData
from piechartpathpreprocess import *
from BuildingName import buildnamedict
from dynamicHeatColumnOneday import heatmapdate
from timelineonebuildingoneday import timeline


def buildingNameToID(name):
    for key in buildnamedict.keys():
        if (buildnamedict[key] == name):
            return key
    return "error"

app = Flask(__name__)
 
 
@app.route('/', methods = ['GET','POST'])
def showIndex1():
    
    # if request.method == 'POST':
    #    buildings = request.form.get('BuildingNo')
        #对用户输入的buildingNo，调用python方法进行处理
        #return #？？？？
    
    return render_template('index1.html')

macaddress={}
nextDate = ""
 

@app.route('/InputBuilding', methods = ['GET','POST'])
def InputBuilding():
    try:
        global macaddress
        global nextDate
        monthData = request.form.get("month")
        if len(monthData) == 1:
            monthData = "0"+monthData
        dateData = request.form.get("date")
        if len(dateData) == 1:
            dateData = "0"+dateData
        hourData = request.form.get("hour")
        if len(hourData) == 1:
            hourData = "0"+hourData
        HeatDate = monthData+dateData+hourData

        if request.form.get("type") == "heatmap":
            HeatList = generateTimeIntervalAndHeatData(HeatDate)
            return render_template('HeatMapDemo.html',data=HeatList)

        elif request.form.get("type") == "dynamic":
            HeatDate = monthData+dateData
            History = heatmapdate(HeatDate)
            title = "Number of mac addresses in each building on "+dateData+" "+monthData+", 2018"
            return render_template('dynamicheatmap.html',data=History,title=[title])

        elif request.form.get("type") == "piechart":
            building = request.form.get("piechartbuilding")
            builId = buildingNameToID(building)
            if builId == "error":
                return render_template('index1.html',error="Error: Invalid building name")
            else:
                title = ["The distribution of people who were in "+building+" at "+hourData+":00, "+dateData+" "+monthData+", 2018"]
                nexttime, visiId = macaddressInBuildingAtTime(HeatDate, builId)
                resultdict, macaddredict, nexttime = visitorIdsNextHour(nexttime, visiId)
                if len(resultdict) == 0:
                    return render_template('index1.html',error="Error: No Record Found")
                nextDate = nexttime
                macaddress = macaddredict
                proRes = []
                countPeople = sum(resultdict.values())
                for key,value in resultdict.items():
                    proRes.append(key)
                    proRes.append(float(value)/countPeople*100)
                return render_template('wherePeopleGo.html',data=proRes,title=title)

        else:
            building = request.form.get("linechartbuilding")
            builId = buildingNameToID(building)
            floor = request.form.get("linechartfloor")
            if builId == "error":
                return render_template('index1.html',error="Error: Invalid building name")
            else:
                HeatDate = monthData+dateData
                # title = ["The distribution of people who were in "+building+" at "+hourData+":00, "+dateData+" "+monthData+", 2018"]
                title = "The change of the number of people on "+building+" "+floor+" on "+dateData+" "+monthData+", 2018"
                changeData = timeline(HeatDate, builId, floor)
                return render_template('BuildingPopulation.html',data=changeData,title=[building+" "+floor,title])
    except:
        return render_template('index1.html',error="Error: No Record Found")



@app.route('/GetNextPie', methods = ['GET','POST'])
def GetNextPie():
    try:
        global macaddress
        global nextDate
        nexttime=nextDate
        macaddredict=macaddress
        building = request.form.get("building")
        builId = buildingNameToID(building)
        if builId == "error":
            return render_template('index1.html',error="Error: Invalid building name")
        else:
            hourtime = (int(nexttime[4:])-1) % 24
            title = ["The distribution of people who were in "+building+" at "+str(hourtime)+":00, "+nexttime[2:4]+" "+nexttime[:2]+", 2018"]
            resultdict, macaddredict, nexttime = visitorIdsNextHour(nexttime, macaddredict[builId])
            if len(resultdict) == 0:
                    return render_template('index1.html',error="Error: No Record Found")
            nextDate = nexttime
            macaddress = macaddredict
            proRes = []
            countPeople = sum(resultdict.values())
            for key,value in resultdict.items():
                proRes.append(key)
                proRes.append(float(value)/countPeople*100)
            return render_template('wherePeopleGo.html',data=proRes,title=title)
    except:
        return render_template('index1.html',error="Error: No Record Found")



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)

