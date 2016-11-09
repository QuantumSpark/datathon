"""
This script clusters signals and cameras to determine intersections.
"""

import pandas as pd
import numpy as np
from math import sqrt

class Camera(object):
    def __init__(self, row):
        self.location = row[0]
        self.image = row[1]
        self.rotation = row[2]
        self.lng = row[3]
        self.lat = row[4]

    def __str__(self):
        return '<Camera @ {0}>'.format(self.location)

class Signal(object):
    def __init__(self, row):
        self.signal_type = row[0]
        self.signal_type2 = row[1]
        self.signal_id = row[4]
        self.construction_status = row[5]
        self.radio_control = row[6]
        self.opticom = row[7]
        self.rotation = row[8]
        self.status = row[9]
        self.year = row[11]
        self.location = row[13]
        self.mod_date = row[22]
        self.lat = row[23]
        self.lng = row[24]

    def __str__(self):
        return '<Signal @ {0}>'.format(self.location)

class Intersection(object):
    def __init__(self, sig, cams):
        self.signal = sig
        self.cameras = cams

INTERSION_RADIUS = 0.0005
CAM_PATH = 'data/traffic-cameras.csv'
SIG_PATH = 'data/traffic-signals.csv'

def run():
    cams = map(lambda row: Camera(row), pd.read_csv(CAM_PATH).values)
    sigs = map(lambda row: Signal(row), pd.read_csv(SIG_PATH).values)
    print len(cams), len(sigs)
    print cams[0], sigs[0]

    intersections = []
    for sig in sigs:
        int_cams = []
        for cam in cams:
            if dist(cam, sig) < INTERSION_RADIUS:
                int_cams.append(cam)
        intersections.append(Intersection(sig, int_cams))
        for cam in int_cams:
            cams.remove(cam)

    print len(intersections)
    print len(filter(lambda i: len(i.cameras) > 0, intersections))
    print len(cams)

def dist(p1, p2):
    return sqrt((p1.lat - p2.lat) ** 2 + (p1.lng - p2.lng) ** 2)

run()
