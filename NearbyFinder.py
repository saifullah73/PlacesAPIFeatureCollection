import Circle
import FeatureSet
import pprint
import requests


class NearbyFinder:
    outerRadius = 0
    locationsFound = []
    nearbyLocations = {}
    totalAPICalls = 0
    def __init__(self,circle, featureset,key):
        self.circle = circle
        self.featureSet = featureset
        self.key = key
        self.outerRadius = circle.radius * 2


    def searchAllPointsInOuterRadius(self,key, type , location):
        URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        params = {'location':location , 'radius':self.outerRadius, 'type':type, 'key':key}
        response = requests.get(url = URL, params = params)
        # gmaps = googlemaps.Client(key = key)
        # response = gplaces.places_nearby(gmaps, location=location, type=type,rank_by='distance')
        mResults = response.json()
        pprint.pprint(mResults)
        results = mResults.get('results')
        if (results is not None ) and  (len(results) > 0):
            for x in range (len(results)):
                lat = results[x]['geometry']['location']['lat']
                lng = results[x]['geometry']['location']['lng']
                location = str(lat) +','+ str(lng)
                self.locationsFound.append(location)
        else:
            self.locationsFound.clear()
            print("No results found in circle")

    def findStraightLineDistance(self, location, nearbypoint):
        ## need to implement
        print("no")

    def doNearbySearchForOneType(self):
        ## for origin
        currentDistance = 0
        for nearbyPoint in self.locationsFound:
            distance = self.findStraightLineDistance(self.circle.origin, nearbyPoint)
            if distance < currentDistance:
                currentDistance = distance
        self.nearbyLocations[self.circle.origin] = [currentDistance, 1]
         ##for population
        for loc in self.circle.population:
            if  self.nearbyLocations.get(loc) != None:
                self.nearbyLocations[loc][1] +=1  ## appending by 1 to indicate that multiple loc had same coordinates , so their nearbyPoint is same
                continue
            currentDistance = 0
            for nearbyPoint in self.locationsFound:
                distance = self.findStraightLineDistance(loc,nearbyPoint)
                if distance < currentDistance:
                    currentDistance = distance
            self.nearbyLocations[loc] = [currentDistance,1]
        self.writeNearbyBackToFile()

    def writeNearbyBackToFile(self):
         ## need to implement
        print("no")


    def start(self):
        for type in self.featureSet.features:
            if self.totalAPICalls <= 200:
                self.searchAllPointsInOuterRadius(self.key,type,self.circle.origin)
                self.totalAPICalls +=1
                self.doNearbySearchForOneType()
            else:
                print("limit exceeded")










