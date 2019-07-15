from FileAssistant import *
from FeatureSet import *
from Circle import *
from NearbyFinder import  *
import pandas as pd


circleOrigins = []
API_KEY = None ##write APi key


def getCirlceOrigins():
    with open('x.csv','r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            if row[9] not in circleOrigins:
                circleOrigins.append(row[9])
        circleOrigins.pop(0)

def start():
    count = 0
    fileAssistant = FileAssistant.FileAssistant('x.csv')
    featureSet = FeatureSet.FeatureSet("hospital","restaurant")
    fileAssistant.appendFeatureColumns(featureSet.features)
    getCirlceOrigins()
    print("Total Circles = ", len(circleOrigins))
    df = pd.read_csv("x.csv", sep=',')
    for origin in circleOrigins:
        count+=1
        print("Circle no. " ,count)
        df1 = df[(df.Origin == origin)]
        population = []
        for x in df1.iterrows():
            population.append((x[1][0],x[1][8]))
        circle = Circle.Circle(1,origin,population)
        print("population = ",len(circle.population))
        nearbyFinder = NearbyFinder(circle,featureSet,API_KEY,fileAssistant)
        nearbyFinder.start()



start()

