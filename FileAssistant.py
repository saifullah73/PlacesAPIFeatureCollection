import csv
import pandas as pd


class FileAssistant:

    passedCircleOrigins = []


    def __init__(self,fileName):
        self.fileName = fileName


    def appendFeatureColumns(self,features):
        df = pd.read_csv(self.fileName, sep=',')
        df.set_index("id", inplace=True)
        for feature in features:
             df[feature] = "None"
        df.to_csv(self.fileName)

    def insertValues(self,values,columnName):
        df = pd.read_csv(self.fileName,sep = ',')
        df.set_index("id", inplace= True)
        for key in values:
            key = int(key)
            df.loc[key, columnName] = values.get(key)
        df.to_csv(self.fileName)

