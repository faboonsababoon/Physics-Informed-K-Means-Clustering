from sklearn import tree
import pandas as pd

from sklearn.datasets import make_blobs


from sklearn import tree
import pandas as pd
import math

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plot
#2000 2000 8 9 11
samples = 2000
iterations = 1000   
print("Samples = " + str(samples))
#10 8 11
#1 4 3 0.984 tie
#6 5 3 0.924
std =[0.5,0.5,0.5]
print("Std = [" + str(std[0]) + ", " + str(std[1]) + ", " + str(std[2])+ "]")
#20 18 15
X, y = make_blobs(n_samples = samples, n_features = 4, centers = 3, cluster_std=std, random_state = 42)
df = pd.DataFrame(X, columns = ["1","2","3","4"])
df["class"] = y
print(iterations)


def calculateCentroid(listE):

    total0=0
    total1=0
    total2=0
    total3=0
    for point in listE:
        total0+=point[0]
    for point in listE:
        total1+=point[1]            
    for point in listE:
        total2+=point[2]
    for point in listE:
        total3+=point[3]
    
    centroid = [float(total0/len(listE)), float(total1/len(listE)), float(total2/len(listE)), float(total3/len(listE))]
    if len(listE) == 0:
        return None
    else:
        return centroid


    

def calculateDistance(list1, list2):
    squaredValues = []
    for i in range(len(list1)):
        squaredValues.append((float(list1[i])-float(list2[i]))**2)
    total = 0
    
    for i in squaredValues:
        total += i
    return total ** 0.5

def calculateForces(center, points):
    forces = [0,0,0,0]

    for i in points:
        direction = []

        for j in range(4):
            direction.append(i[j]-center[j])
        
        tempDistance = calculateDistance(center, i)

        for k in range(len(direction)):
            direction[k] = direction[k]/(tempDistance**2 + 1)
        for m in range(len(forces)):
            forces[m] = forces[m] + direction[m]
    
    return forces


k = 3
trainingList = []

classList = []
for row in range(len(df)):
    tempList = []
    for col in df.columns:
        if col != "class":
            tempList.append(float(df.loc[row, col]))

        else:
            classList.append(df.loc[row, col])
    trainingList.append(tempList)


clusters = [trainingList[0], trainingList[1], trainingList[-1]]

clusterVelocities = [[0,0,0,0],[0,0,0,0],[0,0,0,0]] #initially stood still

clusterMasses = [1,1,1] #one point to start off since we chose 0 1 -1

counter = 0
overallGroupsOfPoints = []
for interation in range(iterations):
    firstCluster = []
    secondCluster = []
    thirdCluster = []


    for i in trainingList:
        a = calculateDistance(i, clusters[0])
        b = calculateDistance(i, clusters[1])
        c = calculateDistance(i, clusters[2])

        if min(a,b,c) == a:
            firstCluster.append(i)
        elif min(a,b,c) == b:
            secondCluster.append(i)
        else:
            thirdCluster.append(i)
    clustersPoints = [firstCluster, secondCluster, thirdCluster]
    clusterMasses = []

    for i in range(3):
        if len(clustersPoints[i]) > 3:
            clusterMasses.append(math.sqrt(len(clustersPoints[i])))
        else:
            clusterMasses.append(3)
    x = 1.2 - (interation/(2*iterations))
    for i in range(3):
        force = calculateForces(clusters[i], clustersPoints[i]) 
        for j in range(4):
            clusterVelocities[i][j] = clusterVelocities[i][j]*.95 + force[j]/clusterMasses[i]*.5
    centroidList = [calculateCentroid(firstCluster), calculateCentroid(secondCluster), calculateCentroid(thirdCluster)]

    
    for i in range(3):
        centroid = calculateCentroid(clustersPoints[i])
        for j in range(4):
            clusters[i][j] = (clusters[i][j] + clusterVelocities[i][j]) * 0.8 + 0.2*centroid[j]
    

predicted = []

for i in trainingList:
    a = calculateDistance(clusters[0], i)
    b = calculateDistance(clusters[1], i)
    c = calculateDistance(clusters[2], i)
    if min(a,b,c) == a:
        predicted.append(0)
    elif min(a,b,c) == b:
        predicted.append(1)
    else:
        predicted.append(2)

freqClasses0 = dict()
freqClasses1 = dict()
freqClasses2 = dict()

for i in range(len(predicted)):
    if predicted[i] == 0:
        if df.loc[i, "class"] not in freqClasses0:
            freqClasses0[df.loc[i, "class"]] = 1
        else:
            freqClasses0[df.loc[i, "class"]] += 1
    elif predicted[i] == 1:
        if df.loc[i, "class"] not in freqClasses1:
            freqClasses1[df.loc[i, "class"]] = 1
        else:
            freqClasses1[df.loc[i, "class"]] += 1
    else:
        if df.loc[i, "class"] not in freqClasses2:
            freqClasses2[df.loc[i, "class"]] = 1
        else:
            freqClasses2[df.loc[i, "class"]] += 1

correct = 0


correct = max(freqClasses0.values()) + max(freqClasses1.values()) + max(freqClasses2.values())
print("Accuracy = " + str(correct / samples))

plot.figure(figsize=(8, 8))
plot.scatter(X[:,0], X[:,1], c = y, cmap = "coolwarm", s = 20)

plot.show()


from sklearn.metrics import silhouette_score

def my_silhouette_score(X, labels):
    """
    X: list of points (same as trainingList)
    labels: list of cluster assignments (same length as X)
    """
    return silhouette_score(X, labels, metric="euclidean")

score = my_silhouette_score(trainingList, predicted)
print("Silhouette score =", score)

'''
def calculateCentroid(listE):

    total0=0
    total1=0
    total2=0
    total3=0
    for point in listE:
        total0+=point[0]
    for point in listE:
        total1+=point[1]            
    for point in listE:
        total2+=point[2]
    for point in listE:
        total3+=point[3]
    
    centroid = [float(total0/len(listE)), float(total1/len(listE)), float(total2/len(listE)), float(total3/len(listE))]

    return centroid


    

def calculateDistance(list1, list2):
    squaredValues = []
    for i in range(len(list1)):
        squaredValues.append((float(list1[i])-float(list2[i]))**2)
    total = 0
    
    for i in squaredValues:
        total += i
    return total ** 0.5

indexesClassSetosa = []
indexesClassVersicolor = []
indexesClassVirginica = []

for i in range(len(classList)):
    if classList[i] == "Iris-setosa":
        indexesClassSetosa.append(i)
    elif classList[i] == "Iris-virginica":
        indexesClassVirginica.append(i)
    else:
        indexesClassVersicolor.append(i)



listOfSetosa = []
listOfVirginica = []
listOfVersicolor = []

for i in indexesClassSetosa:
    listOfSetosa.append(trainingList[i])
for i in indexesClassVersicolor:
    listOfVersicolor.append(trainingList[i])
for i in indexesClassVirginica:
    listOfVirginica.append(trainingList[i])
print(listOfVirginica)
print(len(listOfVirginica))

setosaCentroid = calculateCentroid(listOfSetosa)
virginicaCentroid = calculateCentroid(listOfVirginica)
versicolorCentroid = calculateCentroid(listOfVersicolor)

print(setosaCentroid)
print(virginicaCentroid)
print(versicolorCentroid)
#print(calculateCentroid([[3,3,3,3], [3,3,3,4]]))
'''
'''

predictedValues = []
def calculateDistance(list1, list2):
    squaredValues = []
    for i in range(len(list1)):
        squaredValues.append((float(list1[i])-float(list2[i]))**2)
    total = 0
    
    for i in squaredValues:
        total += i
    return total ** 0.5

listOfValues = []
for u in range(len(df)):

    tempList = []
    for column in df.columns:
        if column != "class":
            tempList.append(df.loc[u, column])
    listOfValues.append(tempList)
for i in range(len(newdf)):
    listOfDistances = []

    extractedValues = []
    for j in newdf.columns:
        if j != "class":
            extractedValues.append(newdf.loc[i, j])

    count = 0


    for instance in listOfValues:
        listOfDistances.append((calculateDistance(instance, extractedValues), count))
        count+=1


    copyOfDistances = []
    for q in listOfDistances:
        copyOfDistances.append(q)

    listOfDistances.sort(key = lambda x: x[0])

    listOfIndexes = []

    for indexes in range(k):
        
        listOfIndexes.append(listOfDistances[indexes][1])

    listOfClasses = []

    for l in listOfIndexes:

        listOfClasses.append(df.loc[l, "class"])

    frequencyOfClasses = dict()

    for oi in listOfClasses:
        if oi not in frequencyOfClasses:
            frequencyOfClasses[oi] = 1
        else:
            frequencyOfClasses[oi] += 1
    selectedClass = max(frequencyOfClasses, key = frequencyOfClasses.get)
    predictedValues.append(selectedClass)
actualValues = []
for i in range(len(newdf)):
    actualValues.append(newdf.loc[i, "class"])

correctAmount = 0
incorrectAmount = 0

for i in range(len(predictedValues)):
    if predictedValues[i] == actualValues[i]:
        correctAmount +=1
    else:
        incorrectAmount+=1


print("Accuracy = " + str((correctAmount)/(correctAmount + incorrectAmount)))

'''


