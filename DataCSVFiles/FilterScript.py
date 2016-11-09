import pandas as pd;
import requests;


def createFilteredCsv():
    df2011 = pd.read_csv('CrimesData/monthlycrime2011.csv')
    df2012 = pd.read_csv('CrimesData/monthlycrime2012.csv')
    df2013 = pd.read_csv('CrimesData/monthlycrime2013.csv')
    df2015 = pd.read_csv('CrimesData/nevercrime2015.csv')
    df2016 = pd.read_csv('CrimesData/monthlycrime2016.csv')

    data = [df2011,df2012,df2013,df2015,df2016]
    for index in range(len(data)):
        tmp = data[index][data[index]["INCIDENT_TYPE"] == "Fatal/Injury Collision"]
        realindex = index+1
        if (realindex >= 4):
            realindex +=1
        tmp.to_csv("FilteredCrimeData/filtered201" + str(realindex) + ".csv", encoding='utf-8')

def createCombinedFilter():
    df2011 = pd.read_csv('FilteredCrimeData/filtered2011.csv')
    df2012 = pd.read_csv('FilteredCrimeData/filtered2012.csv')
    df2013 = pd.read_csv('FilteredCrimeData/filtered2013.csv')
    df2015 = pd.read_csv('FilteredCrimeData/filtered2015.csv')
    df2016 = pd.read_csv('FilteredCrimeData/filtered2016.csv')

    frames = [df2011, df2012, df2013, df2015, df2016]
    result = pd.concat(frames)
    result.to_csv("FilteredCrimeData/FilteredCombined.csv", encoding='utf-8')


def addCommasToStreet(block):
    if " / " in block:
        block = block.replace(' ', '').replace('/',',')
        rtnValue = block
        return rtnValue+",Surrey,BC"
    else:
        block = block.replace(' ', ',')
        block += ",Surrey,BC"
        return  block

def getLatLon(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + address + \
          "&key=AIzaSyCwc3ISug1xPFbSP7kL4f4xF_svNgAc2bc"
    request = requests.get(url);
    json = request.json()
    lat = json.get("results")[0]['geometry']['location']['lat']
    lng = (json.get("results")[0]['geometry']['location']['lng'])

    return {"lat":lat, "lng": lng}

def createDataFrameForLatLong():
    dfLatLong = pd.DataFrame()
    df = pd.read_csv('CrimesData/monthlycrime2016.csv')
    df = df[df["INCIDENT_TYPE"] == "Fatal/Injury Collision"]
    df.to_csv('FilteredCrimeData/filtered2016.csv', encoding='utf-8')
    result = pd.read_csv('FilteredCrimeData/filtered2016.csv')
    size = result.HUNDRED_BLOCK.size

    for index in range(size):
        addressInFormat = addCommasToStreet(result.HUNDRED_BLOCK[index])
        print(addressInFormat)
        dfLatLong = dfLatLong.append(getLatLon(addressInFormat), ignore_index=True)

    return dfLatLong



def createFilteredDFWithLatLong():
    dfLatLong = createDataFrameForLatLong()
    filteredCombineddf = pd.read_csv("FilteredCrimeData/FilteredCombined.csv")
    filteredCombineddf["lat"] = dfLatLong["lat"]
    filteredCombineddf["lng"] = dfLatLong["lng"]
    filteredCombineddf.to_csv("FilteredCrimeData/FilteredCombinedWithLatLong.csv", encoding='utf-8')