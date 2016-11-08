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
    avgLat = 0
    avgLong = 0
    markerTrafficSignal = [{} for _ in range(rawTrafficSignal.Latitude.size)]
    for i in range(int(rawTrafficSignal.Longitude.size)):
        avgLat += rawTrafficSignal.Latitude[i]
        avgLong += rawTrafficSignal.Longitude[i]
        dic = {
            'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
            'lat': rawTrafficSignal.Latitude[i],
            'lng': rawTrafficSignal.Longitude[i],
            'infobox': "<b>traffic signal</b>" + str(rawTrafficSignal.Latitude[i]) + "," + str(rawTrafficSignal.Longitude[i])
        };
        markerTrafficSignal[i] = dic

    markerTrafficCamera = [{} for _ in range(trafficCameras.LATITUDE.size)]
    for i in range(int(trafficCameras.LATITUDE.size)):
        avgLat += trafficCameras.LATITUDE[i]
        avgLong += trafficCameras.LONGITUDE[i]
        dic = {
            'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
            'lat': trafficCameras.LATITUDE[i],
            'lng': trafficCameras.LONGITUDE[i],
            'infobox': "<b>traffic camera</b>" + str(trafficCameras.LATITUDE[i]) + "," + str(trafficCameras.LONGITUDE[i])
        };
        markerTrafficCamera[i] = dic
    markers = markerTrafficSignal + markerTrafficCamera
    avgLat = avgLat/(trafficCameras.LATITUDE.size + rawTrafficSignal.Latitude.size)
    avgLong = avgLong/(trafficCameras.LATITUDE.size + rawTrafficSignal.Latitude.size)
    print(avgLat)
    print(avgLong)
    sndmap = Map(
        identifier="sndmap",
        zoom= 11,
        lat=avgLat,
        lng=avgLong,
        markers=markers
    )
    return render_template('mapthing.html', sndmap=sndmap)


if __name__ == '__main__':
    app.run()
