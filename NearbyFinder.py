import Circle
import FeatureSet
import pprint
import requests


class NearbyFinder:
    outerRadius = 0
    locationsFound = []
    nearbyLocations = {}
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
        results = response.json()
        pprint.pprint(results)
        if len(results['results']) > 0:
            lat = results['results'][0]['geometry']['location']['lat']
            lng = results['results'][0]['geometry']['location']['lng']
            location = str(lat) +','+ str(lng)
            return  location
        else:
            return "none"

    def findStraightLineDistance(self, location, nearbypoint):
        ## need to implement
        print("no")

    def doNearbySearchForOneType(self):
        for loc in self.circle.population:
            if  self.nearbyLocations.get(loc) != None:
                self.nearbyLocations[loc][1]+=1  ## appending by 1 to indicate that multiple loc had same coordinates , so their nearbyPoint is same
            currentDistance = 0
            for neabyPoint in self.locationsFound:
                distance = self.findStraightLineDistance(loc,neabyPoint)
                if distance < currentDistance:
                    currentDistance = distance
            self.nearbyLocations[loc] = [currentDistance,1]
        self.writeNearbyBackToFile()

    def writeNearbyBackToFile(self):
         ## need to implement
        print("no")


    def start(self):
        for type in self.featureSet.features:
            self.searchAllPointsInOuterRadius(self.key,type,self.circle.origin)
            self.doNearbySearchForOneType()










