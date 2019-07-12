import csv


class FileAssistant:
    def __init__(self,outputFile,inputFile):
        self.outputFile = outputFile
        self.inputFile = inputFile


    def initializeNewFileWithFeatureRow(self,features):
        with open(self.outputFile) as output:
            writer = csv.writer(output)
            features.insert(0,'origin')
            writer.writeRow(features)
        output.close()


    def writeBackToFile(self,nearbyLocations):
         with open(self.outputFile, 'a') as output:
            writer = csv.writer(output)
            for items in nearbyLocations.items():
                count = items[1][1]
                while (count > 0):
                    row = [items[0],items[1][0]]
                    writer.writeRow(row)
                    count -= 1



