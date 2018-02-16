

def loadData(fileName):
    dataDict = {}
    with open(fileName, 'r') as file:
        file.readline()
        for line in file.readlines():
            splitLine = line.split(",")
            if splitLine[0] in dataDict:
                dataDict[splitLine[0]].append(splitLine[1])
            else:
                dataDict[splitLine[0]] = []
                dataDict[splitLine[0]].append(splitLine[1])

    return dataDict


def loadPixels(SegmentedNeucleas):
    words = SegmentedNeucleas.split()
    pixels = set()
    for i in range(0, (len(words)-1), 2):
        start = int(words[i].strip())
        end = start + int(words[i+1].strip())
        while start < end:
            pixels.add(start)
            start += 1

    return pixels


def calculatePrecision(predictedFileName, actualFileName, threshold=0.5):
    predictedDict = loadData(predictedFileName)
    actualDict = loadData(actualFileName)
    assert len(actualDict) == len(predictedDict)

    TP = 0
    FP = 0
    FN = 0
    for key, pValues in predictedDict.items():
        aValues = actualDict[key]
        perfectPrediction = 0
        for i in range(len(pValues)):
            pSet = loadPixels(SegmentedNeucleas=pValues[i])

            hasGroundTruth = False
            for j in range(len(aValues)):
                aSet = loadPixels(SegmentedNeucleas=aValues[j])
                iou = len(aSet.intersection(pSet)) / len(aSet.union(pSet))

                if iou > threshold:
                    TP += 1
                    hasGroundTruth = True
                    perfectPrediction += 1
                    break
            if not hasGroundTruth:
                FP += 1
            if perfectPrediction == len(aValues):
                    FN += len(aValues) - perfectPrediction

    precision = TP / (TP + FP + FN)

    return precision


def calculateAvgPrecision(predictedFileName, actualFileName):
    avg = 0
    t = 0.5
    thresholds = [0.5, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
    for t in thresholds:
        avg += calculatePrecision(predictedFileName, actualFileName, threshold=t)

    return avg/10


