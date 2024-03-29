import Circle
import FeatureSet
import FileAssistant
import pprint
import geopy.distance
import APICounter
import requests
import time


class NearbyFinder:
    outerRadius = 0
    locationsFound = []
    nearbyLocations = {}
    def __init__(self,circle, featureset,key,fileAssistant):
        self.circle = circle
        self.featureSet = featureset
        self.fileAssistant = fileAssistant
        self.key = key
        self.outerRadius = circle.radius * 2


    def searchAllPointsInOuterRadius(self,key, type , location):
        radius = self.outerRadius + 1000
        iteration = 1
        URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        while (iteration <= 5):
            print("Iteration for api call = ", iteration, end = " ")
            print("OuterRadius = ",radius)
            params = {'location':location , 'radius':radius, 'type':type, 'key':key}
            time.sleep(APICounter.SLEEP_TIME)
            response = requests.get(url = URL, params = params)
            APICounter.totalAPICalls += 1
            mResults = response.json()
            results = mResults.get('results')
            if (results is None or len(results) == 0):
                iteration += 1
                radius +=1000
            else:
                break
        if (results is not None ) and  (len(results) > 0):
            for x in range (len(results)):
                lat = results[x]['geometry']['location']['lat']
                lng = results[x]['geometry']['location']['lng']
                location = str(lat) +','+ str(lng)
                self.locationsFound.append(location)
        else:
            self.nearbyLocations.clear()
            self.locationsFound.clear()
            print("No results found in circle")

    def findStraightLineDistance(self, location, nearbypoint):
        lat,lng = location.split(",")
        lat2,lng2 = nearbypoint.split(",")
        return geopy.distance.geodesic((lat, lng), (lat2, lng2)).km

    def doNearbySearchForOneType(self,type):
         ##for population, origin is also part of population
         if len(self.locationsFound) > 0:
            for loc in self.circle.population:
                currentDistance = 1000
                for nearbyPoint in self.locationsFound:
                    distance = self.findStraightLineDistance(loc[1],nearbyPoint)
                    if distance < currentDistance:
                        currentDistance = distance
                self.nearbyLocations[loc[0]] = currentDistance
            if len(self.nearbyLocations) != 0:
                self.writeNearbyBackToFile(type)
            else:
                self.nearbyLocations.clear()
                self.locationsFound.clear()
                print("No results to be written back")


    def writeNearbyBackToFile(self,type):
        self.fileAssistant.insertValues(self.nearbyLocations,type)
        self.nearbyLocations.clear()
        self.locationsFound.clear()


    def start(self):
        for type in self.featureSet.features:
            print("Searching for type \"",type,"\"")
            if APICounter.totalAPICalls <= APICounter.API_LIMIT:
                self.searchAllPointsInOuterRadius(self.key,type,self.circle.origin)
                print("total Api calls = ", APICounter.totalAPICalls)
                print("Total Nearby Points for type " +str(type) + " = ", len(self.locationsFound), end = '\n\n')
                self.doNearbySearchForOneType(type)
            else:
                print("Total API Calls = ", APICounter.totalAPICalls)
                print("limit exceeded")
                APICounter.limitExceeded = True
                break










