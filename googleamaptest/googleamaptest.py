from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import pandas as pd;
app = Flask(__name__)
GoogleMaps(app, key="AIzaSyCwc3ISug1xPFbSP7kL4f4xF_svNgAc2bc")

@app.route('/')
def plotPointsOnMap():
    rawTrafficSignal = pd.read_csv('DataCSVFiles/trafficsignals.csv')
    trafficCameras = pd.read_csv('DataCSVFiles/monthlytrafficcameras.csv')

    marker = [{} for _ in range(rawTrafficSignal.Latitude.size )]
    for i in range(int(rawTrafficSignal.Longitude.size)):
        dic = {
            'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
            'lat': rawTrafficSignal.Latitude[i],
            'lng': rawTrafficSignal.Longitude[i],
            'infobox': "<b>traffic signal</b>"+str(i)
        };
        marker[i] = dic

    marker2 = [{} for _ in range(trafficCameras.LATITUDE.size)]
    for i in range(int(trafficCameras.LATITUDE.size)):
        dic = {
            'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
            'lat': trafficCameras.LATITUDE[i],
            'lng': trafficCameras.LONGITUDE[i],
            'infobox': "<b>traffic camera</b>" + str(i)
        };
        marker2[i] = dic
    markers = marker + marker2
    sndmap = Map(
        identifier="sndmap",
        zoom= 7,
        lat=49.09401236,
        lng=-122.8180491,
        markers=markers
    )
    return render_template('mapthing.html', sndmap=sndmap)


if __name__ == '__main__':
    app.run()
