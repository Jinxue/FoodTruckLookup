'''
Created on Dec 15, 2015

@author: Jinxue Zhang

Access the Mobile Food Facility Permit in San Francisco area.
This web service takes the location and radius as the input to obtain the types of food truck.
'''

import pandas as pd
from constants import *
import time
import urllib2
from math import radians, cos, sin, asin, sqrt

class FoodTruckLoopup(object):
    def __init__(self, centerLat, centerLon, maxRadius, expirationDays= 1):
        # The last time we access the server to dump the whole data
        self.lasttime = time.time()
        
        # The center and the maximum radius for this area to cache the whole data
        self.centerLat, self.centerLon, self.maxRadius = centerLat, centerLon, maxRadius
        
        # The expiration days for the cache of server data
        self.expirationDays = expirationDays
        
        # The last json object
        self.json, self.start = None, True
        
    def obtainFoodTruckOnTheFly(self, lat, lon, radius):
        '''
        In the case when we need the real-time data in each invoking, we access the server on the fly.
        
        Find the records according to the (lat, log, radius (meters)).
        We only returned the record with "FacilityType=Truck" and "Status=Approved".
        
        We can also filter out the records expired. 
        Unfortunately, the web service seems not support the SoQL for between...and...'''
        
        query = (SERVERURL + "?" +
            "$$app_token=" + APPTOKEN +
            "&facilitytype=Truck" +
            "&status=APPROVED" +
            "&$where=within_circle(location%2C%20" + str(lat) + "%2C%20" + str(lon) + "%2C%20" + str(radius) + ")"
            )
        try:
            raw_data = pd.read_json(query, typ = "series")
            
            # Then output the useful information
            res = [(x["location"], x["address"], x["applicant"], x["fooditems"]) for x in raw_data]
            #print res
            new_data = pd.DataFrame(res)
            return len(res), new_data.to_json()
        except  urllib2.HTTPError, e:
            print e.read()
            return "ERROR"

    def within_circle(self, lat1, lon1, lat2, lon2, r):
        '''
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees), and check whether they are within r
        '''
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2.0 * asin(sqrt(a)) 
        km = 6367.0 * c
        return (km * 1000) < r
    
    def obtainFoodTruckOnWithCache(self, lat, lon, radius):
        '''
        In the case when the server data is slow to change, we can cache it in local.
        
        Implement the service with cache:  we first dump all the records by setting the maximum radius and 
        store it in the memory or local disk, and directly access it in the following accesses.
        
        There are two cases we need to diable the cache:
        1. The last fetching is one day ago (by default)
        2. The current query radius in out of the (self.centerLat, self.centerLon, self.maxRadius)
        
        '''
        if self.start or ((time.time() - self.lasttime) > self.expirationDays * 24 * 3600) or \
        (self.within_circle(self.centerLat, self.centerLon, lat, lon, self.maxRadius) == False):
            query = (SERVERURL + "?" + "$$app_token=" + APPTOKEN +
                     "&facilitytype=Truck" +
                     "&status=APPROVED" +
                     "&$where=within_circle(location%2C%20" + 
                        str(self.centerLat) + "%2C%20" + str(self.centerLon) + "%2C%20" + str(self.maxRadius) + ")")
            try:
                self.json = pd.read_json(query, typ = "series")
            except  urllib2.HTTPError, e:
                print e.read()
                return "ERROR"
            self.start, self.lasttime = False, time.time()
        
        if not self.within_circle(self.centerLat, self.centerLon, lat, lon, self.maxRadius):
            self.centerLat, self.centerLon, self.maxRadius = lat, lon, radius 
            
        # Then output the useful information
        res = [(x["location"], x["address"], x["applicant"], x["fooditems"]) for x in self.json \
                    if self.within_circle(lat, lon, float(x["latitude"]), float(x["longitude"]), radius)]

        new_data = pd.DataFrame(res)
        return len(res), new_data.to_json()

#ft = FoodTruckLoopup(37.73, -122.40, 100000)
#print ft.obtainFoodTruckOnWithCache(37.73, -122.40, 1000)
#print ft.obtainFoodTruckOnTheFly(37.73, -122.40, 1000)
