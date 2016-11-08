import pandas as pd
import googlemaps
from pymongo import MongoClient
from bson.objectid import ObjectId
import time

client = MongoClient('localhost', 27017)
dbDatathon = client.datathon
collisionsCollection = dbDatathon.collisions

gmaps = googlemaps.Client(key='AIzaSyDKNhx9TK6PZpfefd3IfKMiRpI7W5DjDaM')
count = 0


def get_lat_lng(address):
    addressFormatted = ((address.replace(" / ", " & ")) + ", Surrey, BC").lower()
    geocode_result = gmaps.geocode(addressFormatted)
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    return (lat, lng)


for collision in collisionsCollection.find({'geolactionExists':{'$exists': False}}, no_cursor_timeout=True):
    collision_id = collision['_id']
    lat, lng = get_lat_lng(collision['HUNDRED_BLOCK'])
    collisionsCollection.find_one_and_update({'_id':ObjectId(collision_id)}, {'$set': {'LATITUDE':lat, 'LONGTITUDE':lng , 'geolactionExists':True}  })
    count += 1
    if count == 4995:
        count = 0
        time.sleep(25)
